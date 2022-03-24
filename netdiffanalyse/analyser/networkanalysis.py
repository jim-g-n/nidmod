# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:18:23 2022

@author: jnevin
"""
import networkx as nx

class ResultsAnalyser:
    def __init__(self, graph, trends):
        self.graph = graph
        self.trends = trends
        
    def get_graph_properties(self):
        num_nodes = len(self.graph.nodes())
        num_edges = len(self.graph.edges())
        connected = nx.is_connected(self.graph)
        degree_cent = nx.degree_centrality(self.graph)
        betweenness = nx.betweenness_centrality(self.graph)
        closeness = nx.closeness_centrality(self.graph)
        
        properties_dict = {'num_nodes': num_nodes, 'num_edges': num_edges,
                           'connected': connected, 'degree_cent': degree_cent,
                           'betweenness': betweenness, 'closeness': closeness}
        
        return properties_dict
    
    
        
        
