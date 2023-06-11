from ast import And
from kubernetes import client, config
from colorama import Fore, Back, Style
import sys

def checkManagedClusterStatus(debug=False):
    
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Managed Cluster Health Check")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True
    mclusters=[]
    summaryStatus= True

    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CustomObjectsApi()
    try:
        mcs = v1.list_cluster_custom_object(group="cluster.open-cluster-management.io", version="v1", plural="managedclusters",_request_timeout=1)
        ###acluster={}
        # print(type(mcs))
        # print("++++++++++++++++++++++++++++++++++++++++++++++")
        # for mc in mcs.get('items', []):
        #     print(type(mc))
        #     print(len(mc))
        #     for x in range(len(mc)):
        #         #print(k,":::==++===",v)
        #         print(type(mc))
        #         print(x)
                #print(x['metadata']['name'])
        #for mc in mcs.items:     
            #print(mc)
            ##print("++++++++++++++++++++++++++++++++++++++++++++++")
            #for x in mc:
            #    print(x)
            #    print("++++++++++++++++++++++++++++++++++++++++++++++")
        for mc in mcs.get('items', []):  
            acluster={}  
            #print("\n")
            #print(mc['metadata']['name'])
            #mclusters.append(mc['metadata']['name'])
            #print (mclusters,"::",mc['metadata']['creationTimestamp'])
            #print(mc['metadata']['creationTimestamp'])
            acluster['managedName']=mc['metadata']['name']
            acluster['creationTimestamp']=mc['metadata']['creationTimestamp']

            #print(mc['status']['conditions'])

            for x in mc['status']['conditions']:
                ###### do we need this?
                status=True
                for k,v in x.items():
                    #status=True
                    if (k=="reason" or k=="status"):
                        if debug: print(k," : ",v)
                        if k=="status":
                            if v=="True":
                                status = status and True
                            else:
                                status = False
                                summaryStatus = False    
                        acluster['health']=status        
            #print("\n")

            mclusters.append(acluster)
            if debug: print(acluster)
            #print("++++++++++++++++++++++++++++++++++++++++++++++")
        print(mclusters)
        print(Back.LIGHTYELLOW_EX+"")
        print("************************************************************************************************")
        print("Managed Cluster Health Check passed ============ ", summaryStatus)
        print("************************************************************************************************")
        print(Style.RESET_ALL)

        #for x in mclusters:
        #    checkManagedClusterAddonStatus(x)
        for x in mclusters:
            for k,v in x.items():
                if (k=="managedName") :
                    checkManagedClusterAddonStatus(v,debug)
    
    except Exception as e:
        print(Fore.RED+"Failure: ",e) 
        sys.exit("Cluster may be down, or credentials may be wrong, or simply not connected")   
        print(Style.RESET_ALL)
    return status


def checkManagedClusterAddonStatus(managedCluster, debug=False): 

    status = True
    summaryStatus = True
    print("Checking Addon Health of ",managedCluster) 
    addonCluster={}
    addonCluster['managedName']=managedCluster
    
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    try:

        v1 = client.CustomObjectsApi()
        mcs = v1.list_namespaced_custom_object(group="addon.open-cluster-management.io", version="v1alpha1", plural="managedclusteraddons", namespace=managedCluster,_request_timeout=1)
        for mc in mcs.get('items', []):
            #print("\n")
            if debug: print(mc['metadata']['name'])
            #print(mc['metadata']['creationTimestamp'])
            status=True
            for x in mc['status']['conditions']:
                #### do we need this
                #status=True
                for k,v in x.items():
                    if (k=="reason" or k=="status"):
                        if debug: print(k," : ",v)
                        if k=="status":
                            if v=="True":
                                status = status and True
                                #print(status)
                            else:
                                status = False 
                                summaryStatus = False
                                #print(status)   
            #print("\n")
                            addonCluster[mc['metadata']['name']]=status
            
            
    except Exception as e:
        print(Fore.RED+"Failure: ",e)
        sys.exit("Cluster may be down, or credentials may be wrong, or simply not connected")
        print(Style.RESET_ALL)
    print(addonCluster)
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print(" Managed Cluster Addon Health Check passed ============ ", summaryStatus)
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    return status