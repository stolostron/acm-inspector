from prometheus_api_client import *
import datetime
import sys
import numpy as np
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

def checkCPUUsage(startTime, endTime, step):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Checking CPU Usage across the cluster")
    pc=promConnect()
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True

    status=clusterCPUCoreUsed(pc,startTime, endTime, step)
    status=clusterCPUPctUsed(pc,startTime, endTime, step)
    status=clusterCPUUsage(pc,startTime, endTime, step)
    status=nodeCPUUsage(pc,startTime, endTime, step)
    status=kubeAPICPUUsage(pc,startTime, endTime, step)
    status=ACMCPUUsage(pc,startTime, endTime, step)
    status=ACMDetailCPUUsage(pc,startTime, endTime, step)
    

    
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("CPU Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    return status
     
def clusterCPUCoreUsed(pc,startTime, endTime, step):

    print("Total Cluster CPU Core usage")

    try:
        node_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster=""})')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "CPUCoreUsage"}, inplace = True)
        print(node_cpu_df[['CPUCoreUsage']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{cluster=""})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.plot(title="Cluster CPU Core usage")
        plt.savefig('../../output/cluster-cpu-core-usage.png')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu core for cluster: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status

def clusterCPUPctUsed(pc,startTime, endTime, step):

    print("Total Cluster CPU Pct usage")

    try:
        node_cpu = pc.custom_query('(1 - sum(avg by (mode) (rate(node_cpu_seconds_total{job="node-exporter", mode=~"idle|iowait|steal", cluster=""}[5m]))))*100')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "CPUCoreUsage"}, inplace = True)
        print(node_cpu_df[['CPUCoreUsage']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='(1 - sum(avg by (mode) (rate(node_cpu_seconds_total{job="node-exporter", mode=~"idle|iowait|steal", cluster=""}[5m]))))*100',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.plot(title="Cluster CPU Pct usage")
        plt.savefig('../../output/cluster-cpu-pct-usage.png')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu pct for cluster: ",e) 
        print(Style.RESET_ALL)   
    print("=============================================")
   
    status=True
    return status


def clusterCPUUsage(pc,startTime, endTime, step):

    print("Total Cluster CPU usage")

    try:
        node_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate)')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "CPUUsage"}, inplace = True)
        print(node_cpu_df[['CPUUsage']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.plot(title="Cluster CPU usage")
        plt.savefig('../../output/cluster-cpu-usage.png')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu for cluster: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status  

def nodeCPUUsage(pc,startTime, endTime, step):

    print("CPU Usage across Nodes")

    try:
        node_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate) by (node)')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "CPUUsage"}, inplace = True)
        print(node_cpu_df[['node','CPUUsage']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate) by (node)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.plot(title="CPU Usage across Nodes")
        plt.savefig('../../output/node-cpu-usage.png')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu usage across Nodes: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status   

def kubeAPICPUUsage(pc,startTime, endTime, step):

    print("Total Kube API Server CPU usage")

    try:
        kubeapi_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace="openshift-kube-apiserver"})')

        kubeapi_cpu_df = MetricSnapshotDataFrame(kubeapi_cpu)
        kubeapi_cpu_df["value"]=kubeapi_cpu_df["value"].astype(float)
        kubeapi_cpu_df.rename(columns={"value": "CPUUsage"}, inplace = True)
        print(kubeapi_cpu_df[['CPUUsage']].to_markdown())

        kubeapi_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate) by (node)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        kubeapi_cpu_trend_df = MetricRangeDataFrame(kubeapi_cpu_trend)
        kubeapi_cpu_trend_df["value"]=kubeapi_cpu_trend_df["value"].astype(float)
        kubeapi_cpu_trend_df.index= pandas.to_datetime(kubeapi_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        kubeapi_cpu_trend_df.plot(title="Kube API Server CPU usage")
        plt.savefig('../../output/kubeapi-cpu-usage.png')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu for Kube API Server: ",e) 
        print(Style.RESET_ALL)   
    print("=============================================")
   
    status=True
    return status  

def ACMCPUUsage(pc,startTime, endTime, step):

    print("Total ACM CPU usage")

    try:
        acm_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-.+"})')

        acm_cpu_df = MetricSnapshotDataFrame(acm_cpu)
        acm_cpu_df["value"]=acm_cpu_df["value"].astype(float)
        acm_cpu_df.rename(columns={"value": "CPUUsage"}, inplace = True)
        print(acm_cpu_df[['CPUUsage']].to_markdown())

        acm_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-.+"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        acm_cpu_trend_df = MetricRangeDataFrame(acm_cpu_trend)
        acm_cpu_trend_df["value"]=acm_cpu_trend_df["value"].astype(float)
        acm_cpu_trend_df.index= pandas.to_datetime(acm_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        acm_cpu_trend_df.plot(title="ACM CPU usage")
        plt.savefig('../../output/acm-cpu-usage.png')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu for ACM: ",e)  
        print(Style.RESET_ALL)  
    print("=============================================")
   
    status=True
    return status

def ACMDetailCPUUsage(pc,startTime, endTime, step):

    print("Detailed ACM CPU usage")

    try:
        acm_detail_cpu = pc.custom_query('sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-.+"}) by (namespace)')

        acm_detail_cpu_df = MetricSnapshotDataFrame(acm_detail_cpu)
        acm_detail_cpu_df["value"]=acm_detail_cpu_df["value"].astype(float)
        acm_detail_cpu_df.rename(columns={"value": "CPUUsage"}, inplace = True)
        print(acm_detail_cpu_df[['namespace','CPUUsage']].to_markdown())

        acm_detail_cpu_trend = pc.custom_query_range(
        query='sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace=~"multicluster-engine|open-cluster-.+"}) by (namespace)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        acm_detail_cpu_trend_df = MetricRangeDataFrame(acm_detail_cpu_trend)
        acm_detail_cpu_trend_df["value"]=acm_detail_cpu_trend_df["value"].astype(float)
        acm_detail_cpu_trend_df.index= pandas.to_datetime(acm_detail_cpu_trend_df.index, unit="s")
        acm_detail_cpu_trend_df =  acm_detail_cpu_trend_df.pivot( columns='namespace',values='value')
        acm_detail_cpu_trend_df.plot(title="ACM Detailed CPU usage")
        plt.savefig('../../output/acm-detail-cpu-usage.png')

    except Exception as e:
        print(Fore.RED+"Error in getting cpu details for ACM: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status