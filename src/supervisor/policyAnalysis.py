from prometheus_api_client import *
import datetime
import sys
import numpy as np
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

def checkPolicyControllers(startTime, endTime, step):
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Checking Policy Framework across the cluster")
    pc=promConnect()
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    status = True

    status=getRootPolicy(pc,startTime, endTime, step)
    status=getReplicatedPolicy(pc,startTime, endTime, step)
    status=getReplicatedPolicyControllerResponseTime(pc,startTime, endTime, step)
    status=getReplicatedPolicyControllerWorkQueueResponseTime(pc,startTime, endTime, step)

    

    
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Policy Framework Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    return status
# get the number of root policies
# get the number of managed clusters
# get the pct of propapagtion or the total propagated count
# the amount of status changes coming in
# amount of policy defintions changing - by user or template varianble changes
# get how stressed the system is
     
def getRootPolicy(pc,startTime, endTime, step):
    print("Get the details of root policies")

    try:
        root_policy = pc.custom_query('sum(policy_governance_info{type="root"}) by (policy, policy_namespace)')

        root_policy_df = MetricSnapshotDataFrame(root_policy)
        root_policy_df["value"]=root_policy_df["value"].astype(float)
        #node_cpu_df.rename(columns={"value": "ClusterCPUCoreUsage"}, inplace = True)
        #print(node_cpu_df[['ClusterCPUCoreUsage']].to_markdown())
        print(root_policy_df.to_markdown())
        
        root_policy_number_trend = pc.custom_query_range(
        query='count(policy_governance_info{type="root"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        root_policy_number_trend_df = MetricRangeDataFrame(root_policy_number_trend)
        root_policy_number_trend_df["value"]=root_policy_number_trend_df["value"].astype(float)
        root_policy_number_trend_df.index= pandas.to_datetime(root_policy_number_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        root_policy_number_trend_df.rename(columns={"value": "RootPolicyCount"}, inplace = True)
        root_policy_number_trend_df.plot(title="Count of Root Policies",figsize=(30, 15))
        plt.savefig('../../output/policy-root-count.png')
        saveCSV(root_policy_number_trend_df,"policy-root-count",True)
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting number of root policies: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status

def getReplicatedPolicy(pc,startTime, endTime, step):
    print("Get details of the replicated policies")

    try:
        propagated_policy = pc.custom_query('count(policy_governance_info{type="propagated"})')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "NumOfPropagatedPolicies"}, inplace = True)
        print(propagated_policy_df[['NumOfPropagatedPolicies']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='count(policy_governance_info{type="propagated"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        propagated_policy_number_trend_df.rename(columns={"value": "PropagatedtPolicyTotal"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="Total Count of propagated Policies",figsize=(30, 15))
        plt.savefig('../../output/policy-propagated-count.png')
        saveCSV(propagated_policy_number_trend_df,"policy-propagated-count",True)
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting number of propagated policies: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status


def getReplicatedPolicyControllerResponseTime(pc,startTime, endTime, step):
    print("Get Percentage of replicated-policy reconcile times le 1 sec")

    # what is the issue with
    # histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy"}[30m])))
    try:
        propagated_policy = pc.custom_query('sum without(le,instance,pod) (controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy",le="1"})/sum without(le,instance,pod) (controller_runtime_reconcile_time_seconds_count{controller="replicated-policy"})')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "ReplicatedPolicyCtrlResponsePctle1sec"}, inplace = True)
        print(propagated_policy_df[['ReplicatedPolicyCtrlResponsePctle1sec']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='sum without(le,instance,pod) (controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy",le="1"})/sum without(le,instance,pod) (controller_runtime_reconcile_time_seconds_count{controller="replicated-policy"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        propagated_policy_number_trend_df.rename(columns={"value": "ReplicatedPolicyCtrlResponsePctle1sec"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="Percentage of replicated-policy reconcile times le 1 se",figsize=(30, 15))
        plt.savefig('../../output/policy-rep-ctrl-le1sec-count.png')
        saveCSV(propagated_policy_number_trend_df[['ReplicatedPolicyCtrlResponsePctle1sec']],"policy-rep-ctrl-le1sec-count",True)
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting Percentage of replicated-policy reconcile times le 1 sec: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status


def getReplicatedPolicyControllerWorkQueueResponseTime(pc,startTime, endTime, step):
    print("Get Percentage of replicated-policy controller workqueuing times le 1 sec")

    # what is the issue with
    # histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy"}[30m])))
    try:
        propagated_policy = pc.custom_query('sum without(le,instance,pod) (workqueue_queue_duration_seconds_bucket{name="replicated-policy",le="1"})/sum without(le,instance,pod) (workqueue_queue_duration_seconds_count{name="replicated-policy"})')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "ReplicatedPolicyCtrlWorkQueueResponsePctle1sec"}, inplace = True)
        print(propagated_policy_df[['ReplicatedPolicyCtrlWorkQueueResponsePctle1sec']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='sum without(le,instance,pod) (workqueue_queue_duration_seconds_bucket{name="replicated-policy",le="1"})/sum without(le,instance,pod) (workqueue_queue_duration_seconds_count{name="replicated-policy"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        #node_cpu_trend_df =  node_cpu_trend_df.pivot( columns='node',values='value')
        propagated_policy_number_trend_df.rename(columns={"value": "ReplicatedPolicyCtrlWorkQueueResponsePctle1sec"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="Percentage of replicated-policy work queue times le 1 se",figsize=(30, 15))
        plt.savefig('../../output/policy-rep-ctrl-wq-le1sec-count.png')
        saveCSV(propagated_policy_number_trend_df[['ReplicatedPolicyCtrlWorkQueueResponsePctle1sec']],"policy-rep-ctrl-wq-le1sec-count",True)
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting Percentage of replicated-policy controller workqueuing times le 1 secc: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status


