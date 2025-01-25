import pymannkendall as mk
import networkx as nx
import json
import graphviz 
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from analysis.utility.charting import *

def getCausalGraph(jsonAsDict) :
    
    # networkx has good apis for graph traversal
    causal_metricnx = nx.DiGraph()
    # graphviz can visually render the graph better than netowrkx counterpart
    causal_metricgv=graphviz.Digraph()

    # Add the edges to the graph from the dictionary
    try:
        for key, values in jsonAsDict.items():
            for value in values:
                # that is key is the cause
                # key causes value
                # marketing campaign CAUSES web traffic (can increase or decrease)
                causal_metricnx.add_edge(key, value, label="causes")
                causal_metricgv.edge(key, value, label="causes")
                
                
        dir = get_output_directory()
        causal_metricgv.format = 'png' 
        causal_metricgv.render(f"{dir}/causal-topology", format='png', cleanup=True) 


    except json.JSONDecodeError:
        print("Invalid JSON format.")


    return causal_metricnx,causal_metricgv

