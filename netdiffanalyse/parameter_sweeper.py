# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:28:04 2022

@author: jnevin
"""

import itertools
import pandas as pd
from netdiffanalyse.datahandling.dataintegration import FeatureSetup, MatchClassifier, NetworkIntegrator
from netdiffanalyse.diffusionmodel.diffusionmodel import InitialisedDiffusionModel
from netdiffanalyse.analyser.networkanalysis import ResultsAnalyser, MultiResultsAnalyser

class CombinationBuilder:
    '''
    A class for building all possible integration setups
    
    Inputs are lists, where each element is a dictionary defining a blocking/compare/classifer/clustering alg setup
    
    Output is a list where each element is a full integration setup
    '''
    def __init__(self, block_setups, compare_setups, classifier_names, clustering_algs):
        self.block_setups = block_setups
        self.compare_setups = compare_setups
        self.classifier_names = classifier_names
        self.clustering_algs = clustering_algs
        
    def get_all_combinations(self):
        return list(itertools.product(self.block_setups, self.compare_setups, 
                                 self.classifier_names, self.clustering_algs))
        
class ParameterSweeper:
    '''
    Class for calculating different possible integrated graphs based on different integration setups
    
    Input is a list of integration setups, a list of graphs, and a set of training matches
    
    Output is a list of integrated networks
    '''
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
                network_integrator = NetworkIntegrator(self.graphs[0], self.pred_matches)
            else:
                network_integrator = NetworkIntegrator(self.graphs, self.pred_matches)
    
            integrated_networks.append(network_integrator.integrate_network(clustering_alg))
            
        return integrated_networks
    
class MultiNetworkDiffusion:
    '''
    Class for running a custom diffusion model on different graphs
    
    Input is a set of graphs and a custom diffusion model
    
    Output is a MultiResultsAnalyser object
    '''
    def __init__(self, graphs, custom_diffusion_model):
        self.graphs = graphs
        self.custom_diffusion_model = custom_diffusion_model
        
        graph_assc_diff_models = []
        for graph in graphs:
            initialised_diffusion_model = InitialisedDiffusionModel(graph, custom_diffusion_model)
            graph_assc_diff_models.append(initialised_diffusion_model)
            
        self.graph_assc_diff_models = graph_assc_diff_models
        
    def run_diffusion_model(self, simulation_setup):
        graph_assc_trends = []
        for model in self.graph_assc_diff_models:
            trends = model.run_diffusion_model(simulation_setup)
            graph_assc_trends.append(trends)
            
        graph_assc_results_analysers = []
        for i in range(len(self.graphs)):
            results_analyser = ResultsAnalyser(self.graph_assc_diff_models[i].model, self.graphs[i],
                                           graph_assc_trends[i])
            graph_assc_results_analysers.append(results_analyser)
            
        return MultiResultsAnalyser(graph_assc_results_analysers)
            
        
            
    