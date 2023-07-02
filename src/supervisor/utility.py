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
        masterDF.plot(y=["ManagedClusterCount", "ClusterCPUCoreUsage","ClusterCPUCoreCap","KubeAPICPUCoreUsage","ACMCPUCoreUsage"],
                      title="Combined Master CPU chart", kind="line", figsize=(30, 15))
        #masterDF.plot(title="Combined Master CPU chart", kind="line", figsize=(30, 15))
        plt.savefig('../../output/master-cpu.png')
        masterDF.plot(y=["ManagedClusterCount", "ClusterMemUsageGB","ClusterMemCapacityGB","KubeAPIMemUsageGB","ACMMemUsageGB"],
                      title="Combined Master Memory chart", kind="line", figsize=(30, 15))
        plt.savefig('../../output/master-memory.png')
        masterDF.plot(y=["ManagedClusterCount", "etcdDBLeaderElection","etcdDBSizeUsedMB","etcdDBSizeMB"],
                      title="Combined Master API-ETCD chart", kind="line", figsize=(30, 15))
        plt.savefig('../../output/master-api-etcd.png')
        masterDF.plot(y=["ManagedClusterCount", "CompactorHalted","recvsync90","recvsync95","recvsync99"],
                      title="Combined Master Thanos chart", kind="line", figsize=(30, 15))
        plt.savefig('../../output/master-thanos.png')
        # the column names can be derived dynamically from the dataframe or apiServerObjects.py module
        masterDF.plot(y=["ManagedClusterCount", "APIServersecretsCount","APIServerconfigmapsCount","APIServerserviceaccountsCount",
                         'APIServerclusterrolebindings.rbac.authorization.k8s.ioCount','APIServerrolebindings.rbac.authorization.k8s.ioCount',
                         'APIServerclusterroles.rbac.authorization.k8s.ioCount','APIServerroles.rbac.authorization.k8s.ioCount',
                         'APIServerleases.coordination.k8s.ioCount','APIServerconfigurationpolicies.policy.open-cluster-management.ioCount',
                         'APIServermanifestworks.work.open-cluster-management.ioCount'],
                      title="Combined Master Thanos chart", kind="line", figsize=(30, 15))
        plt.savefig('../../output/master-apiServerObjCount.png')
    except Exception as e:
        print(Fore.RED+"Failure in saving masterDF: ",e)  
        print(Style.RESET_ALL)        