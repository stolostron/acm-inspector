import matplotlib.pyplot as plt
import os
import numpy as np
import sys
import datetime
import pandas
from analysis.utility.analytics import *
from analysis.utility.causalExtractor import *
from analysis.utility.results import *
import json
import importlib.resources

# Can we make this code generic?
# We are almost there!! - There are 2 GRC specific things in this code:
# 1. Comments state that this is for GRC
# 2. In the data load section, there is a calculated column added for rate determination. We can try to offload it to master.csv generation
# Else this code is GRC agnostic.
# And it assumes a 2 tier causal diagram for now. Tier 1 contains metrics that causes/effects metrics in Tier 2
# 2 tier ==> A causes X and Y. B causes Z. C causes X and Z. We are not inputting what causes A, B and C yet.
def startGRCAnalysis() :

    print("Starting GRC on the ACM Hub Analysis")
    pdfFile = create_pdf(title="GRC Analysis")
    causal_graph_grc_nx = getCausality()
    grc_df = loadData()
    analyzeBottleneck(grc_df,causal_graph_grc_nx, pdfFile)

def getCausality() :
    print("Loading GRC on the ACM Hub causal relationship")
    #causal_graph_nx = getCausalGraph()

    # Access the JSON file from the package's resource directory
    with importlib.resources.open_text('analysis.causalrelations', 'grc_bottleneck.json') as file:
        data = json.load(file)

    # Now `data` contains the dictionary from the JSON file
    print(data)
    causal_graph_nx = getCausalGraph(data)
    print("Causal Graph created successfully")
    return causal_graph_nx


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

def generate_chart():
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]
    plt.plot(x, y)
    plt.title("Sample Chart")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    tempPDFDir = get_output_directory()
    chart_filename = tempPDFDir /"temp_chart.pdf"

    plt.savefig(chart_filename, format='pdf')  # Save chart as PDF (temporary)
    plt.close()
    
    return chart_filename


def analyzeBottleneck(grc_df,causal_graph_grc_nx,pdfFile) :
    print("----------------------------------------------------------")
    print("Running Bottleneck analysis for GRC on the ACM Hub data")
    print("----------------------------------------------------------")

    all_metrics=getMetricList(causal_graph_grc_nx)
    print("List of all metrics that are critical to the analysis: ", all_metrics)

    # List of leaf nodes/metrics thru which the bottlneck is seen 
    impactedMetricList = getImpactedMetricList(causal_graph_grc_nx)
    print("List of all metrics that show if system is stalling (leaf nodes): ", impactedMetricList)

    # and from that list, we can crawl to find out the metrics which causes the bottlenecks
    fooList = getDriverMetricList(causal_graph_grc_nx)
    print("List of all Metrics that drive the load on the system): ", fooList)
    
    
    columns = ['MetricName', 'TrendProblem', 'ThresholdProblem','DependsOn']
    
    conclusion_df = pandas.DataFrame(columns=columns)

    print(" ")
    print("----------------------------------------------------------")

    for metric in impactedMetricList:
        
        # more analysis will be added here:
        # - are there any abrupt changes in levels of data
        # - ability to forecast
        # Strength of association between the metrics - cause and effect
        trend=checkIfTrendIsRising(grc_df,metric)
        threshold=pctTimeValueIsHigh(grc_df, metric,0.5)
        depends = dependsOn(causal_graph_grc_nx,metric)
        
        row = pandas.DataFrame([[metric, trend, threshold,depends]], columns=columns)
        conclusion_df = pandas.concat([conclusion_df, row], ignore_index=True)
    
    # else this breaks saving the dataframe into pdf
    conclusion_df['DependsOn'] = conclusion_df['DependsOn'].astype(str)

    tempPDFDir = get_output_directory()
    tempPDF = tempPDFDir /"temp.pdf"
    tempTable = tempPDFDir /"table.pdf"
    
    add_text_to_pdf(tempPDF, "All is well")
    merge_pdfs(pdfFile, tempPDF)
    
    add_dataframe_to_pdf(tempTable,conclusion_df)
    merge_pdfs(pdfFile, tempTable)
    
    tempChart = generate_chart()
    merge_pdfs(pdfFile, tempChart)

    os.remove(tempPDF)
    os.remove(tempTable)
    os.remove(tempChart)
    
    print(" ")
    print("----------------------------------------------------------")
    print("In Conclusion...")    
    print(conclusion_df)
    print(" ")
    print("Detailed Report in PDF is here: ", pdfFile)