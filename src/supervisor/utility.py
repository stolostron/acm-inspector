import os
from prometheus_api_client import *
from kubernetes import client, config
import sys
import datetime

def promConnect():
    try:
        # Get the Prometheus URL from the Route object.
        custom_object_api = client.CustomObjectsApi()
        promRoute = custom_object_api.get_namespaced_custom_object(
             "route.openshift.io", "v1", "openshift-monitoring", "routes", "prometheus-k8s")
        prom_url = "https://{}/".format(promRoute['spec']['host'])

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