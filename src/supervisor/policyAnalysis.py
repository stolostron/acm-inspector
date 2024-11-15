from prometheus_api_client import *
import datetime
import sys
import numpy as np
import pandas
from utility import *
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt

"""
policyAnalysis.py

This modules gathers all policy specific metrics. 
Using these metrics and the causal graph for policy, we should be able to debug issues 
related to capacity/performance of the Policy framework on ACM hub.
We get the:
- number of root policies
- number of managed clusters (in container.py)
- total number of propagated policies
- number of status updates coming in from propagated policies
- number of root policy defintions changing - by user or template varianble changes
- controller_runtime_reconcile_time_seconds_bucket (stress on) :
    - root-policy-status controller
    - root-policy-spec and controller
    - replicated-policy controller


Aside from these policy specific metrics, we do have other modules that collect:
- CPU data of GRC Pods: cpuAnalysis.py
- Memory data of GRC Pods: memoryAnalysis.py
- API Server objects related to GRC: apiServerObjects.py

"""

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
    status=getReplicatedPolicyStatusChange(pc,startTime, endTime, step)
    status=getRootPolicySpecChange(pc,startTime, endTime, step)
    status=getRootPolicyControllerResponseTimeforSpecChange(pc,startTime, endTime, step)
    status=getRootPolicyControllerResponseTimeforStatusChange(pc,startTime, endTime, step)

    

    
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Policy Framework Health Check  - ", "PLEASE CHECK to see if the results are concerning!! ")
    print("************************************************************************************************")
    print(Style.RESET_ALL)
    return status

     
def getRootPolicy(pc,startTime, endTime, step):
    print("Get the details of root policies")

    try:
        # policy_governance_info{type="root"} =0,1,-1 capture different states.
        # Therefore total number is found out by using count(policy_governance_info{type="root"})
        root_policy = pc.custom_query('count(policy_governance_info{type="root"}) by (policy, policy_namespace)')

        root_policy_df = MetricSnapshotDataFrame(root_policy)
        root_policy_df["value"]=root_policy_df["value"].astype(float)
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
    print("Get 95th Percentile replicated-policy reconcile times")

    # This should have got us the 95th percentike
    # histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy"}[10m])) by (le))
    # however, if no policies are to be replicated, this metric does not change. Therefore we do not have results for this period
    # Thus we use: histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy"}[30m]))  by(le)  )  or vector(0)
    try:
        propagated_policy = pc.custom_query('histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy"}[30m]))  by(le)  )  or vector(0)')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df.fillna(0,inplace=True)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "ReplicatedPolicyCtrlResponse95Pctle"}, inplace = True)
        print(propagated_policy_df[['ReplicatedPolicyCtrlResponse95Pctle']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy"}[30m]))  by(le)  )  or vector(0)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.fillna(0,inplace=True)    
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        propagated_policy_number_trend_df.rename(columns={"value": "ReplicatedPolicyCtrlResponse95Pctle"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="95th Percentile replicated-policy reconcile times le 1 se",figsize=(30, 15))
        plt.savefig('../../output/policy-rep-ctrl-95pctle.png')
        saveCSV(propagated_policy_number_trend_df[['ReplicatedPolicyCtrlResponse95Pctle']],"policy-rep-ctrl-le1sec-count",True)
        plt.savefig('../../output/breakdown/policy-rep-ctrl-95pctle.png')
        saveCSV(propagated_policy_number_trend_df,"policy-rep-ctrl-95pctle")
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting 95th Percentile replicated-policy reconcile times: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status


def getReplicatedPolicyControllerWorkQueueResponseTime(pc,startTime, endTime, step):
    print("Get 95th Percentile replicated-policy controller workqueuing times")

    # This should have got us the 95th percentike
    # histogram_quantile(0.95, sum(rate(workqueue_queue_duration_seconds_bucket{name="replicated-policy"}[30m])) by (le))
    # however, if no policies are to be replicated, this metric does not change. Therefore we do not have results for this period
    # Thus we use: histogram_quantile(0.95, sum(rate(workqueue_queue_duration_seconds_bucket{name="replicated-policy"}[30m])) by (le)) or vector(0)
    try:
        propagated_policy = pc.custom_query('histogram_quantile(0.95, sum(rate(workqueue_queue_duration_seconds_bucket{name="replicated-policy"}[30m])) by (le)) or vector(0)')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df.fillna(0,inplace=True)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "ReplicatedPolicyCtrlWorkQueueResponse95Pctle"}, inplace = True)
        print(propagated_policy_df[['ReplicatedPolicyCtrlWorkQueueResponse95Pctle']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='histogram_quantile(0.95, sum(rate(workqueue_queue_duration_seconds_bucket{name="replicated-policy"}[30m])) by (le)) or vector(0)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.fillna(0,inplace=True)        
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        propagated_policy_number_trend_df.rename(columns={"value": "ReplicatedPolicyCtrlWorkQueueResponse95Pctle"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="95th Percentile replicated-policy work queue times le 1 se",figsize=(30, 15))
        plt.savefig('../../output/policy-rep-ctrl-wq-95pctle.png')
        saveCSV(propagated_policy_number_trend_df[['ReplicatedPolicyCtrlWorkQueueResponse95Pctle']],"policy-rep-ctrl-wq-le1sec-count",True)
        plt.savefig('../../output/breakdown/policy-rep-ctrl-wq-95pctle.png')
        saveCSV(propagated_policy_number_trend_df,"policy-rep-ctrl-wq-95pctle")
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting 95th Percentile replicated-policy controller workqueuing times: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status

def getReplicatedPolicyStatusChange(pc,startTime, endTime, step):
    print("Get details of the replicated policy status changes")

    # policy_governance_info{type="propagated"} =0,1,-1 capture different states.
    # Therefore total number is found out by using count(policy_governance_info{type="propagated"})
    # Total number of non-compliant is found out by using sum(policy_governance_info{type="propagated"})
    # Though this query may not be able detect when 
    # Say we have 2 policies and both are deployed to 3 clusters. 
    # And all are compliant. Now suddenly one day in one of the clusters - the policies start flip flopping. 
    # And this flip flop goes on for a long time. This will create a constant update cycle in the policy propagator. 
    # However at an aggregate level, all that we see is - 6 replicated policies were compliant. 
    # And then suddenly that changed to 5 and remained at 5. 
    # But this is an edge case. Therefore we do not complicate our process for now.

    # But should we make it same as getRootPolicySpecChange()
    # and change it to: rate(controller_runtime_reconcile_time_seconds_count{controller="replicated-policy"}[30m])
    # Issue may be that replicated-policy controller is called also when the policy spec changes and 
    # not only when replicated policy status changes
    # or should we do a derivative of this metric while analyzing,
    try:
        propagated_policy = pc.custom_query('sum(policy_governance_info{type="propagated"})')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "NumOfNonCompliantPropagatedPolicies"}, inplace = True)
        print(propagated_policy_df[['NumOfNonCompliantPropagatedPolicies']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='sum(policy_governance_info{type="propagated"})',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        propagated_policy_number_trend_df.rename(columns={"value": "NonCompliantPropagatedPoliciesTotal"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="Total Count of NonCompliant propagated Policies",figsize=(30, 15))
        plt.savefig('../../output/policy-non-compliant-propagated-count.png')
        saveCSV(propagated_policy_number_trend_df,"policy-non-compliant-propagated-count",True)
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting number of (non-compliant) propagated policy status changes: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status

def getRootPolicySpecChange(pc,startTime, endTime, step):
    print("Get details of the root policy spec rate changes")

    # This number should reflect user changes to root policy
    # as well root policy changes due to template variable (hub side) changes
    # as well as new policy creations
    try:
        # this metric is a counter. So we need rate. sum will not make sense
        propagated_policy = pc.custom_query('rate(controller_runtime_reconcile_time_seconds_count{controller="root-policy-spec"}[30m])')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "RateOfRootPolicySpecChange"}, inplace = True)
        print(propagated_policy_df[['RateOfRootPolicySpecChange']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='rate(controller_runtime_reconcile_time_seconds_count{controller="root-policy-spec"}[30m])',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        propagated_policy_number_trend_df.rename(columns={"value": "RateOfRootPolicySpecChange"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="Rate of Root Policy Spec change",figsize=(30, 15))
        plt.savefig('../../output/policy-root-spec-change-count.png')
        saveCSV(propagated_policy_number_trend_df[['RateOfRootPolicySpecChange']],"policy-root-spec-change-count",True)
        plt.savefig('../../output/breakdown/policy-root-spec-change-count.png')
        saveCSV(propagated_policy_number_trend_df,"policy-root-spec-change-count")
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting number of root policy spec rate changes: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status

# sum without(le,instance,pod) (controller_runtime_reconcile_time_seconds_bucket{controller="root-policy-spec",le="1"})/sum without(le,instance,pod) (controller_runtime_reconcile_time_seconds_count{controller="root-policy-spec"})

def getRootPolicyControllerResponseTimeforSpecChange(pc,startTime, endTime, step):
    print("Get 95th Percentile root-policy-spec reconcile times")

    # This metric should be strongly causally related to getRootPolicySpecChange

    # This should have got us the 95th percentike
    # histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy"}[10m])) by (le))
    # however, if no policies are to be replicated, this metric does not change. Therefore we do not have results for this period
    # Thus we use: histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="root-policy-spec"}[30m]))  by(le)) or vector(0)
    try:
        propagated_policy = pc.custom_query('histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="root-policy-spec"}[30m]))  by(le)) or vector(0)')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df.fillna(0,inplace=True)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "RootPolicySpecCtrlResponse95Pctle"}, inplace = True)
        print(propagated_policy_df[['RootPolicySpecCtrlResponse95Pctle']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="root-policy-spec"}[30m]))  by(le)) or vector(0)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.fillna(0,inplace=True)    
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        propagated_policy_number_trend_df.rename(columns={"value": "RootPolicySpecCtrlResponse95Pctle"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="95th Percentile root-policy-spec reconcile times le 1 se",figsize=(30, 15))
        plt.savefig('../../output/policy-root-ctrl-spec-95pctle.png')
        saveCSV(propagated_policy_number_trend_df[['RootPolicySpecCtrlResponse95Pctle']],"policy-root-ctrl-spec-le1sec-count",True)
        plt.savefig('../../output/breakdown/policy-root-ctrl-spec-95pctle.png')
        saveCSV(propagated_policy_number_trend_df,"policy-root-ctrl-spec-95pctle")
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting 95th Percentile root-policy-spec reconcile times: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status

def getRootPolicyControllerResponseTimeforStatusChange(pc,startTime, endTime, step):
    print("Get 95th Percentile root-policy-status reconcile times")

    # This metric should be strongly causally related to getReplicatedPolicyStatusChange

    # This should have got us the 95th percentike
    # histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="replicated-policy"}[10m])) by (le))
    # however, if no policies are to be replicated, this metric does not change. Therefore we do not have results for this period
    # Thus we use: histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="root-policy-status"}[30m])) by (le)) or vector(0)
    try:
        propagated_policy = pc.custom_query('histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="root-policy-status"}[30m])) by (le)) or vector(0)')

        propagated_policy_df = MetricSnapshotDataFrame(propagated_policy)
        propagated_policy_df.fillna(0,inplace=True)
        propagated_policy_df["value"]=propagated_policy_df["value"].astype(float)
        propagated_policy_df.rename(columns={"value": "RootPolicyStatusCtrlResponse95Pctle"}, inplace = True)
        print(propagated_policy_df[['RootPolicyStatusCtrlResponse95Pctle']].to_markdown())

        
        propagated_policy_number_trend = pc.custom_query_range(
        query='histogram_quantile(0.95, sum(rate(controller_runtime_reconcile_time_seconds_bucket{controller="root-policy-status"}[30m])) by (le)) or vector(0)',
            start_time=startTime,
            end_time=endTime,
            step=step,
        )

        propagated_policy_number_trend_df = MetricRangeDataFrame(propagated_policy_number_trend)
        propagated_policy_number_trend_df["value"]=propagated_policy_number_trend_df["value"].astype(float)
        propagated_policy_number_trend_df.fillna(0,inplace=True)    
        propagated_policy_number_trend_df.index= pandas.to_datetime(propagated_policy_number_trend_df.index, unit="s")
        propagated_policy_number_trend_df.rename(columns={"value": "RootPolicyStatusCtrlResponse95Pctle"}, inplace = True)
        propagated_policy_number_trend_df.plot(title="95th Percentile root-policy-status reconcile times le 1 se",figsize=(30, 15))
        plt.savefig('../../output/policy-root-ctrl-status-95pctle.png')
        saveCSV(propagated_policy_number_trend_df[['RootPolicyStatusCtrlResponse95Pctle']],"policy-root-ctrl-status-le1sec-count",True)
        plt.savefig('../../output/breakdown/policy-root-ctrl-status-95pctle.png')
        saveCSV(propagated_policy_number_trend_df,"policy-root-ctrl-status-95pctle")
        plt.close('all') 

    except Exception as e:
        print(Fore.RED+"Error in getting 95th Percentile root-policy-status reconcile times: ",e)
        print(Style.RESET_ALL)    
    print("=============================================")
   
    status=True
    return status
