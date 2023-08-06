import os
from prometheus_api_client import *
from kubernetes import client, config
import sys
import datetime
import pandas
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

# To be able to start the dataframe merge, we need this global variable
initialDF = pandas.DataFrame()
masterDF = pandas.DataFrame()
nodeDetails={}

def setNodeDetails(details) :
    
    nodeDetails['numNodes']=details['numNodes']
    nodeDetails['numMasterNodes']=details['numMasterNodes']
    nodeDetails['numWorkerNodes']=details['numWorkerNodes']
    nodeDetails['compact']=details['compact']
    nodeDetails['sumCPUVCoreMaster']=details['sumCPUVCoreMaster']
    nodeDetails['sumCPUVCoreWorker']=details['sumCPUVCoreWorker']
    nodeDetails['sumMemoryGiBMaster']=details['sumMemoryGiBMaster']
    nodeDetails['sumMemoryGiBWorker']=details['sumMemoryGiBWorker']





def promConnect():

    tsdb = sys.argv[1]
    #print(f"Arguments of the script : ", tsdb)

    try:
        if tsdb == "prom" :
            # Get the Prometheus URL from the Route object.
            custom_object_api = client.CustomObjectsApi()
            promRoute = custom_object_api.get_namespaced_custom_object(
                "route.openshift.io", "v1", "openshift-monitoring", "routes", "thanos-querier")
            prom_url = "https://{}".format(promRoute['spec']['host'])
            print("Connecting to ACM Hub at URL: ",prom_url)
        else:
            # Get the Prometheus URL from the Route object.
            custom_object_api = client.CustomObjectsApi()
            promRoute = custom_object_api.get_namespaced_custom_object(
                "route.openshift.io", "v1", "open-cluster-management-observability", "routes", "rbac-query-proxy")
            #if using observability, use below
            prom_url = "https://{}/".format(promRoute['spec']['host'])
            print("Connecting to ACM Hub at URL: ",prom_url)    

        # Get Kubernetes API token.
        c = client.Configuration()
        config.load_config(client_configuration = c)
        api_token = c.api_key['authorization']
        for k,v in c.api_key.items():
            print(k,v)

        #connects to prometheus
        pc = PrometheusConnect(url=prom_url, headers={"Authorization": "{}".format(api_token)}, disable_ssl=True)
    
    except Exception as e:
        print("Failure: ",e) 
        sys.exit("Is PROM_URL, API_TOKEN env variables defined or are they accurate")       
    
    return pc

def helperTime():
    start_time=(datetime.datetime.now() - datetime.timedelta(minutes=2880))
    end_time=datetime.datetime.now()
    step='1m'
    return start_time, end_time,step  

def saveCSV(df, filename, merge = False):
    try:
        if merge == True:
            global masterDF
            df.to_csv('../../output/'+filename+'.csv', index = True, header=True)

            if masterDF.empty:
                #masterDF = pandas.merge(initialDF, df, how ='inner', on ='timestamp')
                masterDF = initialDF
                # print("-----------------------------------")
                # print(initialDF)
                # print("-----------------------------------")
                # print(df)
                # print("-----------------------------------")
                # print(masterDF)
                # print("-----------------------------------")
            else:
                masterDF=pandas.merge(masterDF, df, how ='inner', on ='timestamp')
            #print(masterDF)
        else:
            df.to_csv('../../output/breakdown/'+filename+'.csv', index = True, header=True)
    except Exception as e:
        print(Fore.RED+"Failure in saving to CSV: ",e) 
        print(Style.RESET_ALL)    

def setInitialDF(df): 
    global initialDF
    try:
        initialDF = df
    except Exception as e:
        print("Failure in setting masterDF: ",e)

    print("MasterDF set..")
    print(initialDF)


def saveMasterDF(): 
    try:
        masterDF.to_csv('../../output/master.csv', index = True, header=True)  
        print("MasterDF saved..")
    except Exception as e:
        print(Fore.RED+"Failure in saving masterDF: ",e)  
        print(Style.RESET_ALL)  
    try:       
        # print("Testing Global Node details - compact ---------:", nodeDetails["compact"])
        # print("Testing Global Node details - numMasterNodes ---------:", nodeDetails["numMasterNodes"])
        # print("Testing Global Node details - numWorkerNodes ---------:", nodeDetails["numWorkerNodes"])
        # print("Testing Global Node details - numNodes ---------:", nodeDetails["numNodes"])
        # print("Testing Global Node details - sumCPUVCoreMaster ---------:", nodeDetails["sumCPUVCoreMaster"])
        # print("Testing Global Node details - sumCPUVCoreWorker ---------:", nodeDetails["sumCPUVCoreWorker"])
        # print("Testing Global Node details - sumMemoryGiBMaster ---------:", nodeDetails["sumMemoryGiBMaster"])
        # print("Testing Global Node details - sumMemoryGiBWorker ---------:", nodeDetails["sumMemoryGiBWorker"])

        # if it a 3 node cluster - we do not need to worry about 
        # Master Node capacity and Worker Nodes capacity
        if nodeDetails["compact"]:
            # masterDF.plot(y=["ManagedClusterCount", "ClusterCPUCoreUsage","ClusterCPUCoreCap","KubeAPICPUCoreUsage","ACMCPUCoreUsage"],
            #             title="Combined Master CPU chart", kind="line", figsize=(30, 15))
            
            fig, ax = plt.subplots(figsize=(30,15)) 

            masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
            masterDF.plot(y=["ClusterCPUCoreUsage","ClusterCPUCoreCap","KubeAPICPUCoreUsage","ACMCPUCoreUsage","OtherCPUCoreUsage"], ax = ax, secondary_y = True)
            plt.title("Combined Master CPU chart")
            plt.savefig('../../output/master-cpu.png')

        # if it non-3 node cluster - we do need to separately deal with
        # Master Node capacity and Worker Nodes capacity
        else :
            #masterDF.plot(y=["ManagedClusterCount", "ClusterCPUCoreUsage","ClusterCPUCoreCap","KubeAPICPUCoreUsage","ACMCPUCoreUsage"],
            #            title="Combined Master CPU chart", kind="line", figsize=(30, 15))
            
            fig, ax = plt.subplots(figsize=(30,15)) 

            masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
            masterDF.plot(y=["ClusterCPUCoreUsage","ClusterCPUCoreCap","KubeAPICPUCoreUsage","ACMCPUCoreUsage","OtherCPUCoreUsage"], ax = ax, secondary_y = True)
            
            plt.axhline(y = nodeDetails["sumCPUVCoreMaster"], linestyle = 'dashed', label = "Master Node Capacity") 
            plt.axhline(y = nodeDetails["sumCPUVCoreWorker"], linestyle = 'dashed', label = "Worker Node Capacity")
            #plt.legend()
            plt.title("Combined Master CPU chart")
            plt.savefig('../../output/master-cpu.png')
        
            # masterDF.plot(y=["ManagedClusterCount", "KubeAPICPUCoreUsage"],
            #             title="Combined Master Master Node CPU chart", kind="line", figsize=(30, 15))
            
            fig, ax = plt.subplots(figsize=(30,15))
            masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
            masterDF.plot(y=["KubeAPICPUCoreUsage"], ax = ax, secondary_y = True)            
            
            plt.axhline(y = nodeDetails["sumCPUVCoreMaster"], linestyle = 'dashed', label = "Master Node Capacity") 
            #plt.legend()
            plt.title("Combined Master Master Node CPU chart")
            plt.savefig('../../output/master-masternode-cpu.png')

            # masterDF.plot(y=["ManagedClusterCount", "ACMCPUCoreUsage"],
            #             title="Combined Master Worker Node CPU chart", kind="line", figsize=(30, 15))
            
            fig, ax = plt.subplots(figsize=(30,15))
            masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
            masterDF.plot(y=["ACMCPUCoreUsage"], ax = ax, secondary_y = True) 
            
            plt.axhline(y = nodeDetails["sumCPUVCoreWorker"], linestyle = 'dashed', label = "Worker Node Capacity") 
            #plt.legend()
            plt.title("Combined Master Worker Node CPU chart")
            plt.savefig('../../output/master-workernode-cpu.png')            
    except Exception as e:
        print(Fore.RED+"Failure in drawing graph Combined Master CPU chart - probably metrics are missing: ",e)  
        print(Style.RESET_ALL)  
    try:      
        # if it a 3 node cluster - we do not need to worry about 
        # Master Node capacity and Worker Nodes capacity
        if nodeDetails["compact"]:      
            # masterDF.plot(y=["ManagedClusterCount", "ClusterMemUsageGB","ClusterMemCapacityGB","KubeAPIMemUsageGB","ACMMemUsageGB"],
            #             title="Combined Master Master Node Memory chart", kind="line", figsize=(30, 15))
            fig, ax = plt.subplots(figsize=(30,15)) 

            masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
            masterDF.plot(y=["ClusterMemUsageGB","ClusterMemCapacityGB","KubeAPIMemUsageGB","ACMMemUsageGB","OtherMemUsageGB"], ax = ax, secondary_y = True)
            plt.title("Combined Master Master Node Memory chart")
            plt.savefig('../../output/master-memory.png')
        
        # if it non-3 node cluster - we do need to separately deal with
        # Master Node capacity and Worker Nodes capacity
        else :
            # masterDF.plot(y=["ManagedClusterCount", "ClusterMemUsageGB","ClusterMemCapacityGB","KubeAPIMemUsageGB","ACMMemUsageGB"],
            #             title="Combined Master Master Node Memory chart", kind="line", figsize=(30, 15))
            fig, ax = plt.subplots(figsize=(30,15))
            masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
            masterDF.plot(y=["ClusterMemUsageGB","ClusterMemCapacityGB","KubeAPIMemUsageGB","ACMMemUsageGB","OtherMemUsageGB"], ax = ax, secondary_y = True) 

            plt.axhline(y = nodeDetails["sumMemoryGiBMaster"], linestyle = 'dashed', label = "Master Node Capacity") 
            plt.axhline(y = nodeDetails["sumMemoryGiBWorker"], linestyle = 'dashed', label = "Worker Node Capacity") 
            #plt.legend()
            plt.title("Combined Master Master Node Memory chart")
            plt.savefig('../../output/master-memory.png')
        
            # masterDF.plot(y=["ManagedClusterCount", "KubeAPIMemUsageGB"],
            #             title="Combined Master Worker Node Memory chart", kind="line", figsize=(30, 15))
            fig, ax = plt.subplots(figsize=(30,15))
            masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
            masterDF.plot(y=["KubeAPIMemUsageGB"], ax = ax, secondary_y = True)             
            plt.axhline(y = nodeDetails["sumMemoryGiBMaster"], linestyle = 'dashed', label = "Master Node Capacity") 
            #plt.legend()
            plt.title("Combined Master Worker Node Memory chart")
            plt.savefig('../../output/master-masternode-memory.png')

            # masterDF.plot(y=["ManagedClusterCount","ACMMemUsageGB"],
            #             title="Combined Master Memory chart", kind="line", figsize=(30, 15))
            fig, ax = plt.subplots(figsize=(30,15))
            masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
            masterDF.plot(y=["ACMMemUsageGB"], ax = ax, secondary_y = True)             
            plt.axhline(y = nodeDetails["sumMemoryGiBWorker"], linestyle = 'dashed', label = "Worker Node Capacity") 
            #plt.legend()
            plt.title("Combined Master Memory chart")
            plt.savefig('../../output/master-workernode-memory.png')
    except Exception as e:
        print(Fore.RED+"Failure in drawing graph Combined Master Memory chart - probably metrics are missing: ",e)  
        print(Style.RESET_ALL)  
    try:            
        #masterDF.plot(y=["ManagedClusterCount", "etcdDBLeaderElection","etcdDBSizeUsedMB","etcdDBSizeMB"],
        #              title="Combined Master API-ETCD chart", kind="line", figsize=(30, 15))

        fig, ax = plt.subplots(figsize=(30,15))  

        masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
        masterDF.plot(y=["etcdDBLeaderElection","etcdDBSizeUsedMB","etcdDBSizeMB"], ax = ax, secondary_y = True) 
        plt.title("Combined Master API-ETCD chart") 
        plt.savefig('../../output/master-api-etcd.png')
    except Exception as e:
        print(Fore.RED+"Failure in drawing graph Combined Master API-ETCD chart - probably metrics are missing: ",e)  
        print(Style.RESET_ALL)  
    try:            

        fig, ax = plt.subplots(figsize=(30,15))  

        masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
        masterDF.plot(y=["etcdBackendCommitDuration","etcdWalSyncDuration","etcdNetWorkPeerRoundTripDuration","etcdCPUIOWaitDuration"], ax = ax, secondary_y = True) 
        plt.title("Combined Master ETCD Timing chart") 
        plt.savefig('../../output/master-etcd-timing.png')
    except Exception as e:
        print(Fore.RED+"Failure in drawing graph Combined Master API-ETCD chart - probably metrics are missing: ",e)  
        print(Style.RESET_ALL)      

    try:
        # the column names can be derived dynamically from the dataframe or apiServerObjects.py module
        # masterDF.plot(y=["ManagedClusterCount", "APIServersecretsCount","APIServerconfigmapsCount","APIServerserviceaccountsCount",
        #                  'APIServerclusterrolebindings.rbac.authorization.k8s.ioCount','APIServerrolebindings.rbac.authorization.k8s.ioCount',
        #                  'APIServerclusterroles.rbac.authorization.k8s.ioCount','APIServerroles.rbac.authorization.k8s.ioCount',
        #                  'APIServerleases.coordination.k8s.ioCount','APIServerconfigurationpolicies.policy.open-cluster-management.ioCount',
        #                  'APIServermanifestworks.work.open-cluster-management.ioCount','APIServerplacements.cluster.open-cluster-management.ioCount',
        #                  'APIServersubscriptions.apps.open-cluster-management.ioCount','APIServerapplications.app.k8s.ioCount',
        #                  'APIServerapplications.argoproj.ioCount','APIServerapplicationsets.argoproj.ioCount'],
        #               title="Combined Master API Server Object Count", kind="line", figsize=(30, 15))
        
        fig, ax = plt.subplots(figsize=(30,15)) 

        masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
        masterDF.plot(y=["APIServersecretsCount","APIServerconfigmapsCount","APIServerserviceaccountsCount",
                         'APIServerclusterrolebindings.rbac.authorization.k8s.ioCount','APIServerrolebindings.rbac.authorization.k8s.ioCount',
                         'APIServerclusterroles.rbac.authorization.k8s.ioCount','APIServerroles.rbac.authorization.k8s.ioCount',
                         'APIServerleases.coordination.k8s.ioCount','APIServerconfigurationpolicies.policy.open-cluster-management.ioCount',
                         'APIServermanifestworks.work.open-cluster-management.ioCount','APIServerplacements.cluster.open-cluster-management.ioCount',
                         'APIServersubscriptions.apps.open-cluster-management.ioCount','APIServerapplications.app.k8s.ioCount',
                         'APIServerapplications.argoproj.ioCount','APIServerapplicationsets.argoproj.ioCount'], ax = ax, secondary_y = True)  
        plt.title("Combined Master API Server Object Count")       
        plt.savefig('../../output/master-apiServerObjCount.png')
    except Exception as e:
        print(Fore.RED+"Failure in drawing graph Combined Master API Server Object Count - probably metrics are missing: ",e)  
        print(Style.RESET_ALL)  
    try:    
        # masterDF.plot(y=["ManagedClusterCount", 'APIServerconfigurationpolicies.policy.open-cluster-management.ioCount',
        #                  'APIServermanifestworks.work.open-cluster-management.ioCount','APIServerplacements.cluster.open-cluster-management.ioCount',
        #                  'APIServersubscriptions.apps.open-cluster-management.ioCount','APIServerapplications.app.k8s.ioCount',
        #                  'APIServerapplications.argoproj.ioCount','APIServerapplicationsets.argoproj.ioCount'],
        #               title="Combined ACM Resources", kind="line", figsize=(30, 15))
        
        fig, ax = plt.subplots(figsize=(30,15)) 

        masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
        masterDF.plot(y=['APIServerconfigurationpolicies.policy.open-cluster-management.ioCount',
                          'APIServermanifestworks.work.open-cluster-management.ioCount','APIServerplacements.cluster.open-cluster-management.ioCount',
                          'APIServersubscriptions.apps.open-cluster-management.ioCount','APIServerapplications.app.k8s.ioCount',
                          'APIServerapplications.argoproj.ioCount','APIServerapplicationsets.argoproj.ioCount'], ax = ax, secondary_y = True)
        plt.title("Combined ACM Resources")
        plt.savefig('../../output/master-ACMResources.png')
    except Exception as e:
        print(Fore.RED+"Failure in drawing graph Combined ACM Resources - probably metrics are missing: ",e)  
        print(Style.RESET_ALL)  
    try:    
        #this will not work if Obs. is not installed. So we will need special processing
        # masterDF.plot(y=["ManagedClusterCount", "CompactorHalted","recvsync90","recvsync95","recvsync99"],
        #              title="Combined Master Thanos chart", kind="line", figsize=(30, 15))
        
        fig, ax = plt.subplots(figsize=(30,15)) 

        masterDF.plot(y=["ManagedClusterCount"], ax = ax) 
        masterDF.plot(y=["CompactorHalted","recvsync90","recvsync95","recvsync99"], ax = ax, secondary_y = True) 
        plt.title("Combined Master Thanos chart")
        plt.savefig('../../output/master-thanos.png')
    except Exception as e:
        print(Fore.RED+"Failure in drawing graph Combined Master Thanos chart - probably ACM Obs is not installed: ",e)  
        print(Style.RESET_ALL)        