
from kubernetes import client, config
from colorama import Fore, Back, Style
import sys
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import utility

def checkMCHStatus(debug=False):
    
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("MCH Operator Health Check")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True
    mch={}
    
    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CustomObjectsApi()
    try:
        mcs = v1.list_namespaced_custom_object(group="operator.open-cluster-management.io", version="v1", plural="multiclusterhubs", namespace="", _request_timeout=10)

        for mc in mcs.get('items', []):
            #print("\n")
            if debug: print(mc['metadata']['name'])
            if debug: print("Current Version: ",mc['status']['currentVersion'])
            if debug: print("Desired Version: ",mc['status']['desiredVersion'])
            if debug: print("Phase: ",mc['status']['phase'])
            utility.acmNamespace = mc['metadata']['namespace']
            mch['name']=mc['metadata']['name']
            mch['CurrentVersion']=mc['status']['currentVersion']
            mch['DesiredVersion']=mc['status']['desiredVersion']
            mch['Phase']=mc['status']['phase']
            for x in mc['status']['conditions']:
                for k,v in x.items():
                    if (k=="reason" or k=="status"):
                        if debug: print(k," : ",v)
                        if k=="status":
                            if v=="True":
                                status = status & True
                            else:
                                status = status & False    
            #print("\n")
            mch['Health']=status
            print(mch)
        
        print(Back.LIGHTYELLOW_EX+"")
        print("************************************************************************************************")
        print("MCH Operator Health Check = ", status)  
        print("************************************************************************************************") 
        print(Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED+"Failure: ",e) 
        sys.exit("Cluster may be down, or credentials may be wrong, or simply not connected")
        print(Style.RESET_ALL)

    return status

def checkMCEStatus(debug=False):

    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Multicluster Engine Operator Health Check")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True
    mce={}

    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CustomObjectsApi()
    try:
        mcs = v1.list_cluster_custom_object(group="multicluster.openshift.io", version="v1", plural="multiclusterengines", _request_timeout=10)

        for mc in mcs.get('items', []):
            #print("\n")
            if debug: print(mc['metadata']['name'])
            if debug: print("Current Version: ",mc['status']['currentVersion'])
            if debug: print("Desired Version: ",mc['status']['desiredVersion'])
            if debug: print("Phase: ",mc['status']['phase'])
            utility.mceNamespace = mc['spec']['targetNamespace']
            mce['name']=mc['metadata']['name']
            mce['CurrentVersion']=mc['status']['currentVersion']
            mce['DesiredVersion']=mc['status']['desiredVersion']
            mce['Phase']=mc['status']['phase']
            for x in mc['status']['conditions']:
                for k,v in x.items():
                    if (k=="reason" or k=="status"):
                        if debug: print(k," : ",v)
                        if k=="status":
                            if v=="True":
                                status = status & True
                            else:
                                status = status & False
            #print("\n")
            mce['Health']=status
            print(mce)

        print(Back.LIGHTYELLOW_EX+"")
        print("************************************************************************************************")
        print("Multicluster Engine Operator Health Check = ", status)
        print("************************************************************************************************")
        print(Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED+"Failure: ",e)
        sys.exit("Cluster may be down, or credentials may be wrong, or simply not connected")
        print(Style.RESET_ALL)

    return status

