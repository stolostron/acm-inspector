from prometheus_api_client import *
#import prometheus_api_client
import datetime
import sys
import numpy as np
import pandas
from utility import *

def checkACMContainerStatus():
    print("ACM Pod/Container Health Check")
    status = True

    pc=promConnect()
    status=restartCount(pc)
    status=checkPV(pc)
    status=checkContainerCount(pc)
    status=etcdDBSize(pc)
    status=etcdLeaderChanges(pc)
    status=majorAlertCount(pc)
    #TODO: Add API_SERVER Health Check

    print(" ============ ACM Pod/Container Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ============")
    return status

def restartCount(pc):

    restart_data = pc.custom_query('sum(kube_pod_container_status_restarts_total{namespace=~"open-cluster-managemen.+"}) by (namespace,container) >0')
    restart_data_df = MetricSnapshotDataFrame(restart_data);
    restart_data_df["value"]=restart_data_df["value"].astype(int)
    restart_data_df.rename(columns={"value": "RestartCount"}, inplace = True)
    print(restart_data_df[['container','namespace','RestartCount']])
    print("==============================================")

    status=True
    return status    

def checkPV(pc):
    
    pv_data = pc.custom_query('sum by (persistentvolumeclaim) ((kubelet_volume_stats_available_bytes{namespace="open-cluster-management-observability"})*100/(kubelet_volume_stats_capacity_bytes{namespace="open-cluster-management-observability"}))')
    pv_data_df = MetricSnapshotDataFrame(pv_data);
    pv_data_df["value"]=pv_data_df["value"].astype(float)
    pv_data_df.rename(columns={"value": "AvailPct"}, inplace = True)
    print(pv_data_df[['persistentvolumeclaim','AvailPct']])
    print("==============================================")
     
    status=True
    return status   

def checkContainerCount(pc):
    
    #start_time, end_time,step = helperTime()

    container_data = pc.custom_query('sum by (namespace) (kube_pod_info{namespace=~"open-cluster-managemen.+"})')

    container_data_df = MetricSnapshotDataFrame(container_data);
    container_data_df["value"]=container_data_df["value"].astype(int)
    container_data_df.rename(columns={"value": "PodCount"}, inplace = True)
    print(container_data_df[['namespace','PodCount']])
    print("=============================================")
    
    status=True
    return status  

def etcdDBSize(pc):

    etcd_data = pc.custom_query('etcd_mvcc_db_total_size_in_bytes{job="etcd"}/(1024*1024)')

    etcd_data_df = MetricSnapshotDataFrame(etcd_data);
    etcd_data_df["value"]=etcd_data_df["value"].astype(float)
    etcd_data_df.rename(columns={"value": "etcdDBSizeMB"}, inplace = True)
    print(etcd_data_df[['instance','etcdDBSizeMB']])
    #print(etcd_data_df)
    print("=============================================")
   
    status=True
    return status       

def etcdLeaderChanges(pc):

    etcd_leader_data = pc.custom_query('changes(etcd_server_leader_changes_seen_total{job="etcd"}[1d])')

    etcd_leader_data_df = MetricSnapshotDataFrame(etcd_leader_data);
    etcd_leader_data_df["value"]=etcd_leader_data_df["value"].astype(int)
    etcd_leader_data_df.rename(columns={"value": "LeaderChanges"}, inplace = True)
    print(etcd_leader_data_df[['instance','LeaderChanges']])
    #print(etcd_data_df)
    print("=============================================")
    
    status=True
    return status   

def majorAlertCount(pc):

    alert_data = pc.custom_query('sum by (alertname) (ALERTS{alertstate="firing"}) >1')

    alert_data_df = MetricSnapshotDataFrame(alert_data);
    alert_data_df["value"]=alert_data_df["value"].astype(int)
    print(alert_data_df[['alertname','value']])
    print("=============================================")
    
    status=True
    return status    


