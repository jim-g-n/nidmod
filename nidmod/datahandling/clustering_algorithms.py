# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:52:48 2022

@author: jnevin
"""

'''
Point for defining clustering algorithms.

These algorithms should be functions that take as input a graph or list of graphs
and a pandas MultiIndex representing matches based on attributes for nodes in the graph.

The algorithm should return a single, integrated graph.
'''

import networkx as nx
import numpy as np
from cdlib import algorithms

def walktrap_integration(graph, matches):
    '''
    An algorithm based on clustering matches based on walktrap communities.
    
    A graph is built based on the matches and community detection is run on this graph.
    Nodes within the same community are taken to represent the same entity.
    Same entity nodes are combined into a single node.
    '''
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

def multigraph_walktrap_integration(graphs, matches):
    '''
    Performs the walktrap integration defined above on a list of graphs.
    
    Graphs are first all combined into one large graph, and then the walktrap integration
    is applied.
    '''
    adj_graph = graphs[0]
    for graph in graphs[1:]:
        adj_graph = nx.compose(adj_graph,graph)
    
    return walktrap_integration(adj_graph, matches)