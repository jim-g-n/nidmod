# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:36:59 2022

@author: jnevin

-Blocks and comparisons need to match format of recordlinkage and be included
 in the rl library
-Classifier needs to be valid recordlinkagetoolkit classifier
"""

import networkx as nx
import numpy as np
from cdlib import algorithms
import recordlinkage
import recordlinkage.index
import recordlinkage.compare

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
    
class FeatureSetup:
    '''
    A class to store feature setups
    '''
    def __init__(self, blocks, compares, df):
        self.blocks = blocks
        self.compares = compares
        self.df = df
        
    def initialise_indexer(self):
        indexer = recordlinkage.Index()
        for block_type in self.blocks:
            block_type_fun = getattr(recordlinkage.index, block_type)
            for attribute_block in self.blocks[block_type]:
                indexer.add(block_type_fun(*attribute_block))
        self.indexer = indexer

    def get_candidate_links(self):
        self.candidate_links = self.indexer.index(self.df)
        
    def initialise_comparer(self):
        comparer = recordlinkage.Compare()
        for comp_type in self.compares:
            comp_type_fun = getattr(recordlinkage.compare, comp_type)
            for attribute_comp in self.compares[comp_type]:
                comparer.add(comp_type_fun(*attribute_comp))
        self.comparer = comparer
        
    def calculate_features(self):
        self.features = self.comparer.compute(self.candidate_links, self.df)

class MatchClassifierFit:
    '''
    A class for fitting classifier
    '''
    def __init__(self, classifier, training_features, training_matches):
        self.training_features = training_features
        self.training_matches = training_matches
        self.classifier = classifier
    
    def fit_model(self):
        model = getattr(recordlinkage, self.classifier)()
        model.fit(self.training_features, self.training_matches)
        self.fit_classifier = model
        
    def pred_matches(self, features):
        matches = self.fit_classifier.predict(features)
        return matches
    
class NetworkIntegration:
    '''
    A class for integrating a network with matches and a graph
    '''
    def __init__(self, graph, matches, clustering_alg):
        self.graph = graph
        self.matches = matches
        self.clustering_alg = clustering_alg
        
    def integrate_network(self):
        used_clustering_alg = eval(self.clustering_alg)
        self.adj_graph = used_clustering_alg(self.graph, self.matches)
        
        
        
        
        
        
        

        