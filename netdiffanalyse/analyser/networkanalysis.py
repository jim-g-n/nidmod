# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:18:23 2022

@author: jnevin
"""
import networkx as nx

class ResultsAnalyser:
    def __init__(self, run_diffusion_model):
        self.run_diffusion_model = run_diffusion_model
        self.graph = run_diffusion_model.initialised_diffusion_model.graph
        self.trends = run_diffusion_model.trends
        
    def calculate_graph_properties(self):
        self.num_nodes = len(self.graph.nodes())
        self.num_edges = len(self.graph.edges())
        self.connected = nx.is_connected(self.graph)
        self.degree_centrality = nx.degree_centrality(self.graph)
        self.betweenness = nx.betweenness_centrality(self.graph)
        self.closeness = nx.closeness_centrality(self.graph)
        
        
