# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:36:59 2022

@author: jnevin

"""

import recordlinkage
import recordlinkage.index
import recordlinkage.compare
import nidmod.datahandling.clustering_algorithms as clustering_algorithms

    
class FeatureSetup:
    '''
    A class to store feature setups
    
    Inputs are dictionaries for blocks and attribute comparisons, and dataframe(s)
    
    Can calculate a set of comparison features to be used in a match classifier
    
    Blocks and attribute comparisons need to be provided in a format accepted by recordlinkage
    '''
    def __init__(self, blocks, compares, network_A_df, network_B_df = None):
        self.blocks = blocks
        self.compares = compares
        self.network_A_df = network_A_df
        if network_B_df is not None:
            self.network_B_df = network_B_df
        
        # create the indexer object based on the blocks provided
        indexer = recordlinkage.Index()
        for block_type in blocks:
            block_type_fun = getattr(recordlinkage.index, block_type)
            for attribute_block in blocks[block_type]:
                indexer.add(block_type_fun(*attribute_block))
        self.indexer = indexer
        
        # create the comparer object based on the comparisons provided
        comparer = recordlinkage.Compare()
        for comp_type in compares:
            comp_type_fun = getattr(recordlinkage.compare, comp_type)
            for attribute_comp in compares[comp_type]:
                comparer.add(comp_type_fun(*attribute_comp))
        self.comparer = comparer

        # create the candidate links based on whether there are two dataframes
        if network_B_df is not None:
            self.candidate_links = indexer.index(network_A_df, network_B_df)
        else:
            self.candidate_links = indexer.index(network_A_df)
    
    # calculate comparison features 
    def calculate_features(self):
        if hasattr(self, 'network_B_df'):
            return(self.comparer.compute(self.candidate_links, self.network_A_df, self.network_B_df))
        else:
            return(self.comparer.compute(self.candidate_links, self.network_A_df))

class MatchClassifier:
    '''
    A class for fitting a match classifier
    
    Inputs are the name of the classifier, and sets of training features and matches
    
    Classifier needs to be a valid recordlinkage classifier
    
    Returns a fit match classifier model
    '''
    def __init__(self, match_classifier_name, training_features, training_matches = None):
        self.training_features = training_features
        self.match_classifier_name = match_classifier_name
        if training_matches is not None:
            self.training_matches = training_matches
    
    # fits the model
    def fit_model(self):
        model = getattr(recordlinkage, self.match_classifier_name)()
        if hasattr(self, 'training_matches'): 
            model.fit(self.training_features, self.training_matches)
        else:
            model.fit(self.training_features)
        return model
        
    
class NetworkIntegrator:
    '''
    A class for integrating a network with matches and a graph
    
    Inputs are one or more graphs and nodes that are identified as the same entity, plus an integration algorithm
    
    Clustering algorithm needs to receive a list of graphs, a set of matches, and return a single graph
    
    Can return the integrated network based on the matches
    '''
    def __init__(self, graphs, matches):
        self.graphs = graphs
        self.matches = matches
    
    # integrates the network based on matches and the clustering algorithm
    def integrate_network(self, clustering_alg):
        used_clustering_alg = getattr(clustering_algorithms, clustering_alg)
        return used_clustering_alg(self.graphs, self.matches)
        
        
        
        
        
        
        

        