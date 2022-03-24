# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:52:48 2022

@author: jnevin
"""

import networkx as nx
import numpy as np
from cdlib import algorithms

def walktrap_integration(graph, matches):
    adj_graph = graph.copy()
    match_graph = nx.Graph()
    match_graph.add_edges_from(list(matches))
    
    S = [match_graph.subgraph(c).copy() for c in nx.connected_components(match_graph)]
    S_com = []
    for s_subgraph in S:
        node_names = list(s_subgraph.nodes())

        rename = dict(zip((node_names), np.arange(len(node_names))))
        rev_rename = { v:k for k,v in rename.items()}

        s_subgraph = nx.relabel_nodes(s_subgraph, rename)
        communities = algorithms.walktrap(s_subgraph).communities
        for community in communities:
            S_com.append([rev_rename.get(item,item)  for item in community])

    for component in S_com:
        for node in component[1:]:
            if node in adj_graph.nodes() and component[0] in adj_graph.nodes():
                adj_graph = nx.contracted_nodes(adj_graph, component[0], node, self_loops = False)

    return adj_graph