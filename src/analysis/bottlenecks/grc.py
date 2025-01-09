import matplotlib.pyplot as plt
import os
import numpy as np
import sys
import datetime
import pandas
from analysis.utility.analytics import *
from analysis.utility.causalExtractor import *
from analysis.utility.charting import *
import json
import importlib.resources


results={}

# Can we make this code generic?
# We are almost there!! - There are 2 GRC specific things in this code:
# 1. Comments state that this is for GRC
# 2. In the data load section, there is a calculated column added for rate determination. We can try to offload it to master.csv generation
# Else this code is GRC agnostic.
# And it assumes a 2 tier causal diagram for now. Tier 1 contains metrics that causes/effects metrics in Tier 2
# 2 tier ==> A causes X and Y. B causes Z. C causes X and Z. We are not inputting what causes A, B and C yet.
def startGRCAnalysis() :

    print("Starting GRC on the ACM Hub Analysis")
    causal_graph_grc_nx,causal_metricgv = getCausality()
    grc_df = loadData()
    analyzeBottleneck(grc_df,causal_graph_grc_nx,causal_metricgv)

def getCausality() :
    print("Loading GRC on the ACM Hub causal relationship")
    #causal_graph_nx = getCausalGraph()

    # Access the JSON file from the package's resource directory
    with importlib.resources.open_text('analysis.causalrelations', 'grc_bottleneck.json') as file:
        data = json.load(file)

    # Now `data` contains the dictionary from the JSON file
    print(data)
    results["relationship"]=data
    causal_graph_nx,causal_metricgv = getCausalGraph(data)
    print("Causal Graph created successfully")
    return causal_graph_nx,causal_metricgv


def loadData() :
    print("Extracting GRC on the ACM Hub data from master.csv")
    
    # this assumes master.csv in under
    # acm-inspector/output and this code is under
    # acm-inspector/src/analysis/
    
    current_dir = os.getcwd()
    fname = os.path.join(current_dir, "..","output","master.csv")
    master_df = pandas.read_csv(fname,index_col=0)

    #print(master_df.info())
    grc_df = master_df[['ManagedClusterCount', 'RootPolicyCount', 'PropagatedtPolicyTotal',
                    'ReplicatedPolicyCtrlResponse95Pctle','ReplicatedPolicyCtrlWorkQueueResponse95Pctle',
                    'NonCompliantPropagatedPoliciesTotal','RateOfRootPolicySpecChange',
                    'RootPolicySpecCtrlResponse95Pctle','RootPolicyStatusCtrlResponse95Pctle']]

    #print(grc_df.describe())

    # Convert index field, ie timestamp into integer so that numpy can work
    # https://stackoverflow.com/questions/57435794/using-np-gradient-with-datetimes

    time_seconds = grc_df.index.astype('datetime64[s]').astype('int64')
    #print(time_seconds)
    grc_df['RateOfPropagatedPolicyNonCompliance'] = np.gradient(grc_df['NonCompliantPropagatedPoliciesTotal'], time_seconds)
    print("Extracted GRC on the ACM Hub data from master.csv successfully")

    return grc_df


def analyzeBottleneck(grc_df,causal_graph_grc_nx,causal_metricgv) :
    print("----------------------------------------------------------")
    print("Running Bottleneck analysis for GRC on the ACM Hub data")
    print("----------------------------------------------------------")

    allMetrics=getMetricList(causal_graph_grc_nx)
    print("List of all metrics that are critical to the analysis: ", allMetrics)
    results["allMetrics"]= allMetrics

    # List of leaf nodes/metrics thru which the bottlneck is seen 
    impactedMetricList = getImpactedMetricList(causal_graph_grc_nx)
    print("List of Health metrics that show if system is stalling : ", impactedMetricList)
    results["impactedMetricList"]= impactedMetricList

    # and from that list, we can crawl to find out the metrics which causes the bottlenecks
    driverMetricList = getDriverMetricList(causal_graph_grc_nx)
    print("List of Causal Metrics that drive the Health Metrics): ", driverMetricList)
    results["driverMetricList"]=driverMetricList
    
    
    columns = ['MetricName', 'TrendProblem', 'ThresholdProblem','DependsOn','Bottleneck']
    
    conclusion_df = pandas.DataFrame(columns=columns)

    print(" ")
    print("----------------------------------------------------------")

    for metric in impactedMetricList:
        
        # more analysis will be added here:
        # - are there any abrupt changes in levels of data
        # - ability to forecast
        # Strength of association between the metrics - cause and effect
        print(" ")
        trend=checkIfTrendIsRising(grc_df,metric)
        threshold=pctTimeValueIsHigh(grc_df, metric,0.5)
        depends = dependsOn(causal_graph_grc_nx,metric)
        plot(grc_df,metric,0.5)
        #correlationMatrix(grc_df, allMetrics)
        scatterPlot(grc_df,metric, depends)
        checkLinearity(grc_df, metric, depends)
        runRegression(grc_df, metric, depends)
        conclusion= metricBottleneck(trend,threshold)
        changeLevelDetection(grc_df,metric)
   
        
        row = pandas.DataFrame([[metric, trend, threshold,depends,conclusion]], columns=columns)
        conclusion_df = pandas.concat([conclusion_df, row], ignore_index=True)
        #results["metric"]={"trend": trend, "threshold": threshold, "dependsOn": depends}
        results["conclusion"]={"conclusion_df contains the summary finding"}
    
    correlationMatrix(grc_df, allMetrics)
   
    
    print(" ")
    
    print(" ")
    print("----------------------------------------------------------")
    print("In Conclusion...")    
    print(conclusion_df)
    print(" ")
    summarizeBottleneck(conclusion_df)