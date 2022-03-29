# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:28:04 2022

@author: jnevin
"""

import itertools
import pandas as pd
from netdiffanalyse.datahandling.dataintegration import FeatureSetup, MatchClassifier, NetworkIntegrator

class CombinationBuilder:
    def __init__(self, block_setups, compare_setups, classifier_names, clustering_algs):
        self.block_setups = block_setups
        self.compare_setups = compare_setups
        self.classifier_names = classifier_names
        self.clustering_algs = clustering_algs
        
    def get_all_combinations(self):
        return list(itertools.product(self.block_setups, self.compare_setups, 
                                 self.classifier_names, self.clustering_algs))
        

class ParameterSweeper:
    def __init__(self, integration_setups, graphs, training_matches = None):
        self.integration_setups = integration_setups
        self.graphs = graphs
        self.training_matches = training_matches
            
        self.num_graphs = len(graphs)
        graph_attribute_dfs = {}
        for i in range(self.num_graphs):
            graph_attribute_dfs['graph_' + str(i)] = pd.DataFrame.from_dict(dict(graphs[i].nodes(data=True)), orient='index')
        self.graph_attribute_dfs = graph_attribute_dfs
        
    def get_integrated_networks(self):
        integrated_networks = []
        for setup in self.integration_setups:
            blocks, compares, classifier_name, clustering_alg = setup
            if len(self.graphs) == 1:
                feature_setup = FeatureSetup(blocks, compares, self.graph_attribute_dfs['graph_0'])
            else:
                feature_setup = FeatureSetup(blocks, compares, self.graph_attribute_dfs['graph_0'], self.graph_attribute_dfs['graph_1'])
            
            self.features = feature_setup.calculate_features()
            
            if self.training_matches is not None:
                match_classifier = MatchClassifier(classifier_name, self.features, self.training_matches)
            else:
                match_classifier = MatchClassifier(classifier_name, self.features)
                
            self.fit_model = match_classifier.fit_model()
            self.pred_matches = self.fit_model.predict(self.features)
            
            if len(self.graphs) == 1:
                network_integrator = NetworkIntegrator(self.graphs[0], self.pred_matches, clustering_alg)
            else:
                network_integrator = NetworkIntegrator(self.graphs, self.pred_matches, clustering_alg)
    
            integrated_networks.append(network_integrator.integrate_network())
            
        return integrated_networks
            
    