import pymannkendall as mk
import networkx as nx
import json


def checkIfTrendIsRising(df, metric):
    # A little bit of regression and then check slope
    # We may have to change boolean to a value
    
    #Run Mann-Kendall Test. It is a non parametric test
    
    trend = False
    # Perform the Mann-Kendall test
    result = mk.original_test(df[metric])

    #print(f"Mann-Kendall Test Statistic: {result.z}")
    #print(f"P-value: {result.p}")
    if result.p < 0.05 and result.trend == 'increasing':
        trend = True
        print("There is a statistically significant rising trend in: ",metric)
    else:
        print("No significant trend detected in: ",metric)
    
    return trend

#0.5 sec threshold default
def pctTimeValueIsHigh(df, metric,thresholdValue = 0.5):
    # How many times have this exceeded over a given value
    # How many observations in total
    # Therefore conclude ....
    
    countThresholhExceed = (df[metric] > thresholdValue).sum() 
    totalCount = len(df[metric])
    print(thresholdValue)
    percentageExceeds = (countThresholhExceed / totalCount) * 100

    print("Threshold Violation analysis for: ",metric, " completed")
    print("The percentage of times it has exceed threshold of ",thresholdValue," is: ",percentageExceeds )
    
    return percentageExceeds

def dependsOn(causal_graph_nx, metric):
    metricList= list(causal_graph_nx.predecessors(metric))
    print("Dependency - Metric: ", metric, " depends on ", metricList)
    return metricList

def getMetricList(causal_graph_nx) :
    metricList= list(causal_graph_nx.nodes)
    return metricList

def getImpactedMetricList(causal_graph_nx) :
    # Nodes with no outgoing edges
    leafNodeMetricList = [node for node in causal_graph_nx.nodes if causal_graph_nx.out_degree(node) == 0]

    return leafNodeMetricList

def getDriverMetricList(causal_graph_nx):

    # Find leaf nodes (nodes with no outgoing edges)
    leafNodeMetricList = getImpactedMetricList(causal_graph_nx)

    # Find the metrics that cause the leaf node metrics
    driverMetricSet = set()
    for metric in leafNodeMetricList:
        # Get the nodes that have outgoing edges to the leaf node
        causalList = list(causal_graph_nx.predecessors(metric))
        driverMetricSet.update(causalList)

    # convert set to list
    driverMetricList = list(driverMetricSet)
    
    return driverMetricList

    
