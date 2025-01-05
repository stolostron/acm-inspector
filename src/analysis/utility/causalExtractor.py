import pymannkendall as mk
import networkx as nx
import json

def getCausalGraph(jsonAsDict) :
    
    causal_metricnx = nx.DiGraph()

    #causal_metricnx.add_edge('RateOfRootPolicySpecChange', 'RootPolicySpecCtrlResponse95Pctle', label="causes")
    #causal_metricnx.add_edge('RateOfRootPolicySpecChange', 'ReplicatedPolicyCtrlResponse95Pctle', label="causes")
    #causal_metricnx.add_edge('RateOfPropagatedPolicyNonCompliance', 'ReplicatedPolicyCtrlResponse95Pctle', label="causes")
    #causal_metricnx.add_edge('RateOfPropagatedPolicyNonCompliance', 'RootPolicyStatusCtrlResponse95Pctle', label="causes")

    #causal_metric=graphviz.Digraph()
    #causal_metric.edge('RateOfRootPolicySpecChange','RootPolicySpecCtrlResponse95Pctle', label="causes")
    #causal_metric.edge('RateOfRootPolicySpecChange','ReplicatedPolicyCtrlResponse95Pctle',label="causes")
    #causal_metric.edge('RateOfPropagatedPolicyNonCompliance','ReplicatedPolicyCtrlResponse95Pctle', label="causes")
    #causal_metric.edge('RateOfPropagatedPolicyNonCompliance','RootPolicyStatusCtrlResponse95Pctle',label="causes")

    #causal_metric

    #causal_metric.render('causal_grc_bottleneck_graph', format='png', view=True)

    # Add the edges to the graph from the dictionary
    try:
        for key, values in jsonAsDict.items():
            for value in values:
                # that is key is the cause
                # key causes value
                # marketing campaign CAUSES web traffic (can increase or decrease)
                causal_metricnx.add_edge(key, value, label="causes")
    except json.JSONDecodeError:
        print("Invalid JSON format.")

    return causal_metricnx

