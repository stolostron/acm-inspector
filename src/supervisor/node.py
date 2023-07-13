from kubernetes import client, config
from colorama import Fore, Back, Style
import sys
from utility import *

import pandas

def checkNodeStatus(debug=False):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Node Health Check")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True
    

    

    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CoreV1Api()
    # print("Listing pods with their IPs:")
    # ret = v1.list_pod_for_all_namespaces(watch=False)
    # for i in ret.items:
    #     print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

    try:
        nodes=v1.list_node(_request_timeout=1) 
        nodeDetailsList=[] 
        node_df = pandas.DataFrame()
        for node in nodes.items:
            nodeDetails={}
            #print(node.metadata.name)
            #print(node.spec)
            nodeDetails['name']=node.metadata.name
            #nodeList['spec']=node.spec
            #print(node.status.conditions)
            for mc in node.status.conditions:
                #print(mc.type,"::",mc.status )
                nodeDetails[mc.type]=mc.status
            if debug: nodeDetails['spec']=node.spec
            #print(nodeDetails) 
            nodeDetailsList.append(nodeDetails)
        
        node_df = pandas.DataFrame.from_records(nodeDetailsList)  
        print(node_df.to_markdown()) 
        node_df["Ready"]=node_df["Ready"].astype(bool)
        
        if False in node_df["Ready"].values :
            print("Problematic Nodes")
            print(node_df[node_df["Ready"] == False])
            status= False

        saveCSV( node_df, "node-list")
        print(Back.LIGHTYELLOW_EX+"")
        print("************************************************************************************************")
        print(" Node Health Check passed ============ ", status)
        print("************************************************************************************************")
        print(Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED+"Failure: ",e)
        sys.exit("Cluster may be down, or credentials may be wrong, or simply not connected")
        print(Style.RESET_ALL)
    return status