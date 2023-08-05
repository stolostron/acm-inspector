from prometheus_api_client import *
import datetime
import sys
import numpy as np
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

def checkMemoryUsage(startTime, endTime, step):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Checking Memory Usage across the cluster")
    pc=promConnect()
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True

    status=clusterMemCapacity(pc,startTime, endTime, step)
    status=clusterMemUsed(pc,startTime, endTime, step)
    status=clusterMemPctUsed(pc,startTime, endTime, step)
    #status=clusterMemUsage(pc,startTime, endTime, step)
    status=nodeMemUsage(pc,startTime, endTime, step)
    status=kubeAPIMemUsage(pc,startTime, endTime, step)
    status=ACMMemUsage(pc,startTime, endTime, step)
    status=ACMDetailMemUsage(pc,startTime, endTime, step)
    status=OtherMemUsage(pc,startTime, endTime, step)
    

    
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Memory Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    return status
     
def clusterMemCapacity(pc,startTime, endTime, step):

    print("Total Cluster Memory Capacity GB")

    try:
        node_cpu = pc.custom_query('sum(node_memory_MemTotal_bytes{job="node-exporter",cluster=""})/(1024*1024*1024)')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "ClusterMemCapacityGB"}, inplace = True)
        print(node_cpu_df[['ClusterMemCapacityGB']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(node_memory_MemTotal_bytes{job="node-exporter",cluster=""})/(1024*1024*1024)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "ClusterMemCapacityGB"}, inplace = True)
        node_cpu_trend_df.plot(title="Cluster Memory Capacity GB",figsize=(30, 15))
        plt.savefig('../../output/cluster-mem-capacity.png')
        saveCSV(node_cpu_trend_df,"cluster-mem-capacity",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting memory Capacity for cluster: ",e)  
        print(Style.RESET_ALL)  
    print("=============================================")
   
    status=True
    return status

def clusterMemUsed(pc,startTime, endTime, step):

    print("Total Cluster Memory usage GB")

    try:
        node_cpu = pc.custom_query('sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!=""})/(1024*1024*1024)')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "ClusterMemUsageGB"}, inplace = True)
        print(node_cpu_df[['ClusterMemUsageGB']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!=""})/(1024*1024*1024)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "ClusterMemUsageGB"}, inplace = True)
        node_cpu_trend_df.plot(title="Cluster Memory usage GB",figsize=(30, 15))
        plt.savefig('../../output/cluster-mem-usage.png')
        saveCSV(node_cpu_trend_df,"cluster-mem-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting memory for cluster: ",e)  
        print(Style.RESET_ALL)  
    print("=============================================")
   
    status=True
    return status

def clusterMemPctUsed(pc,startTime, endTime, step):

    print("Total Cluster Memory Pct usage")

    try:
        node_cpu = pc.custom_query('(1 - sum(:node_memory_MemAvailable_bytes:sum{cluster=""}) / sum(node_memory_MemTotal_bytes{job="node-exporter",cluster=""}))*100')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "ClusterMemUsagePct"}, inplace = True)
        print(node_cpu_df[['ClusterMemUsagePct']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='(1 - sum(:node_memory_MemAvailable_bytes:sum{cluster=""}) / sum(node_memory_MemTotal_bytes{job="node-exporter",cluster=""}))*100',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "ClusterMemUsagePct"}, inplace = True)
        node_cpu_trend_df.plot(title="Cluster Memory Pct usage",figsize=(30, 15))
        plt.savefig('../../output/cluster-mem-pct-usage.png')
        saveCSV(node_cpu_trend_df,"cluster-mem-pct-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting memory pct for cluster: ",e)    
        print(Style.RESET_ALL)
    print("=============================================")
   
    status=True
    return status


def nodeMemUsage(pc,startTime, endTime, step):

    print("Memory Usage across Nodes GB")

    try:
        node_cpu = pc.custom_query('(sum(container_memory_rss{job="kubelet",metrics_path="/metrics/cadvisor", cluster="", container!=""}) by (node))/(1024*1024*1024)')

        node_cpu_df = MetricSnapshotDataFrame(node_cpu)
        node_cpu_df["value"]=node_cpu_df["value"].astype(float)
        node_cpu_df.rename(columns={"value": "NodeMemUsageGB"}, inplace = True)
        print(node_cpu_df[['node','NodeMemUsageGB']].to_markdown())

        node_cpu_trend = pc.custom_query_range(
        query='(sum(container_memory_rss{job="kubelet",metrics_path="/metrics/cadvisor", cluster="", container!=""}) by (node))/(1024*1024*1024)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        node_cpu_trend_df = MetricRangeDataFrame(node_cpu_trend)
        node_cpu_trend_df["value"]=node_cpu_trend_df["value"].astype(float)
        node_cpu_trend_df.index= pandas.to_datetime(node_cpu_trend_df.index, unit="s")
        node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        node_cpu_trend_df.rename(columns={"value": "NodeMemUsageGB"}, inplace = True)
        node_cpu_trend_df.plot(title="Memory Usage across Nodes GB",figsize=(30, 15))
        plt.savefig('../../output/breakdown/node-mem-usage.png')
        saveCSV(node_cpu_trend_df,"node-mem-usage")
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting memory usage across Nodes: ",e) 
        print(Style.RESET_ALL)   
    print("=============================================")
   
    status=True
    return status   

def kubeAPIMemUsage(pc,startTime, endTime, step):

    print("Total Kube API Server Memory usage GB")

    try:
        kubeapi_cpu = pc.custom_query('sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", namespace="openshift-kube-apiserver"})/(1024*1024*1024)')

        kubeapi_cpu_df = MetricSnapshotDataFrame(kubeapi_cpu)
        kubeapi_cpu_df["value"]=kubeapi_cpu_df["value"].astype(float)
        kubeapi_cpu_df.rename(columns={"value": "KubeAPIMemUsageGB"}, inplace = True)
        print(kubeapi_cpu_df[['KubeAPIMemUsageGB']].to_markdown())

        kubeapi_cpu_trend = pc.custom_query_range(
        query='sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", namespace="openshift-kube-apiserver"})/(1024*1024*1024)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        kubeapi_cpu_trend_df = MetricRangeDataFrame(kubeapi_cpu_trend)
        kubeapi_cpu_trend_df["value"]=kubeapi_cpu_trend_df["value"].astype(float)
        kubeapi_cpu_trend_df.index= pandas.to_datetime(kubeapi_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        kubeapi_cpu_trend_df.rename(columns={"value": "KubeAPIMemUsageGB"}, inplace = True)
        kubeapi_cpu_trend_df.plot(title="Kube API Server Memory usage GB",figsize=(30, 15))
        plt.savefig('../../output/kubeapi-mem-usage.png')
        saveCSV(kubeapi_cpu_trend_df,"kubeapi-mem-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting memory for Kube API Server: ",e)    
        print(Style.RESET_ALL)
    print("=============================================")
   
    status=True
    return status  

def ACMMemUsage(pc,startTime, endTime, step):

    print("Total ACM Memory usage GB")

    try:
        acm_cpu = pc.custom_query('sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", namespace=~"multicluster-engine|open-cluster-.+"})/(1024*1024*1024)')

        acm_cpu_df = MetricSnapshotDataFrame(acm_cpu)
        acm_cpu_df["value"]=acm_cpu_df["value"].astype(float)
        acm_cpu_df.rename(columns={"value": "ACMMemUsageGB"}, inplace = True)
        print(acm_cpu_df[['ACMMemUsageGB']].to_markdown())

        acm_cpu_trend = pc.custom_query_range(
        query='sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", namespace=~"multicluster-engine|open-cluster-.+"})/(1024*1024*1024)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        acm_cpu_trend_df = MetricRangeDataFrame(acm_cpu_trend)
        acm_cpu_trend_df["value"]=acm_cpu_trend_df["value"].astype(float)
        acm_cpu_trend_df.index= pandas.to_datetime(acm_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        acm_cpu_trend_df.rename(columns={"value": "ACMMemUsageGB"}, inplace = True)
        acm_cpu_trend_df.plot(title="ACM Memory usage GB",figsize=(30, 15))
        plt.savefig('../../output/acm-mem-usage.png')
        saveCSV(acm_cpu_trend_df,"acm-mem-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting Memory for ACM: ",e)  
        print(Style.RESET_ALL)  
    print("=============================================")
   
    status=True
    return status

def ACMDetailMemUsage(pc,startTime, endTime, step):

    print("Detailed ACM Memory usage GB")

    try:
        acm_detail_cpu = pc.custom_query('(sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", namespace=~"multicluster-engine|open-cluster-.+"}) by (namespace))/(1024*1024*1024)')

        acm_detail_cpu_df = MetricSnapshotDataFrame(acm_detail_cpu)
        acm_detail_cpu_df["value"]=acm_detail_cpu_df["value"].astype(float)
        acm_detail_cpu_df.rename(columns={"value": "ACMDetailMemUsageGB"}, inplace = True)
        print(acm_detail_cpu_df[['namespace','ACMDetailMemUsageGB']].to_markdown())

        acm_detail_cpu_trend = pc.custom_query_range(
        query='(sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", namespace=~"multicluster-engine|open-cluster-.+"}) by (namespace))/(1024*1024*1024)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        acm_detail_cpu_trend_df = MetricRangeDataFrame(acm_detail_cpu_trend)
        acm_detail_cpu_trend_df["value"]=acm_detail_cpu_trend_df["value"].astype(float)
        acm_detail_cpu_trend_df.index= pandas.to_datetime(acm_detail_cpu_trend_df.index, unit="s")
        acm_detail_cpu_trend_df =  acm_detail_cpu_trend_df.pivot( columns='namespace',values='value')
        acm_detail_cpu_trend_df.plot(title="ACM Detailed Memory usage GB",figsize=(30, 15))
        plt.savefig('../../output/breakdown/acm-detail-mem-usage.png')
        saveCSV(acm_detail_cpu_trend_df,"acm-detail-mem-usage")
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting memory details for ACM: ",e)    
        print(Style.RESET_ALL)
    print("=============================================")
   
    status=True
    return status

def OtherMemUsage(pc,startTime, endTime, step):

    print("Total Memory usage for Others GB")

    try:
        acm_cpu = pc.custom_query('sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", namespace=~"multicluster-engine|open-cluster-.+|openshift-kube-apiserver|openshift-etcd"})/(1024*1024*1024)')

        acm_cpu_df = MetricSnapshotDataFrame(acm_cpu)
        acm_cpu_df["value"]=acm_cpu_df["value"].astype(float)
        acm_cpu_df.rename(columns={"value": "OtherMemUsageGB"}, inplace = True)
        print(acm_cpu_df[['OtherMemUsageGB']].to_markdown())

        acm_cpu_trend = pc.custom_query_range(
        query='sum(container_memory_rss{job="kubelet", metrics_path="/metrics/cadvisor", cluster="", container!="", namespace=~"multicluster-engine|open-cluster-.+|openshift-kube-apiserver|openshift-etcd"})/(1024*1024*1024)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        acm_cpu_trend_df = MetricRangeDataFrame(acm_cpu_trend)
        acm_cpu_trend_df["value"]=acm_cpu_trend_df["value"].astype(float)
        acm_cpu_trend_df.index= pandas.to_datetime(acm_cpu_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        acm_cpu_trend_df.rename(columns={"value": "OtherMemUsageGB"}, inplace = True)
        acm_cpu_trend_df.plot(title="Other Memory usage GB",figsize=(30, 15))
        plt.savefig('../../output/other-mem-usage.png')
        saveCSV(acm_cpu_trend_df,"other-mem-usage",True)
        plt.close('all')

    except Exception as e:
        print(Fore.RED+"Error in getting Memory for Other: ",e)  
        print(Style.RESET_ALL)  
    print("=============================================")
   
    status=True
    return status