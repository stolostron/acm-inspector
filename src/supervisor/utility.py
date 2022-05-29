import os
from prometheus_api_client import *
import sys
import datetime

def promConnect():
    try:
        prom_url = os.getenv('PROM_URL')
        api_token = os.getenv('API_TOKEN')

        #connects to prometheus
        pc = PrometheusConnect(url=prom_url, headers={"Authorization": "Bearer {}".format(api_token)}, disable_ssl=True)
    
    except Exception as e:
        print("Failure: ",e) 
        sys.exit("Is PROM_URL, API_TOKEN env variables defined or are they accurate")       
    
    return pc

def helperTime():
    start_time=(datetime.datetime.now() - datetime.timedelta(minutes=2880))
    end_time=datetime.datetime.now()
    step='1m'
    return start_time, end_time,step    