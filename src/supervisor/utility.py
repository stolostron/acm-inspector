import os
from prometheus_api_client import *
from kubernetes import client, config
import sys
import datetime

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