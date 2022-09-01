# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:32:12 2022

@author: jnevin
"""

from nidmod.datahandling.dataintegration import FeatureSetup, MatchClassifier, NetworkIntegrator
from nidmod.diffusionmodel.diffusionmodel import CustomDiffusionModel, InitialisedDiffusionModel
from nidmod.analyser.networkanalysis import ResultsAnalyser
import pandas as pd

class IntegrationPipeline:
    '''
    Class for entire integration and diffusion model pipeline
    
    Users can provide all the individual steps of the process and run in one go
    '''
    def __init__(self, graphs, blocks, compares, classifier_name,
                 clustering_alg, statuses, compartments, transition_rules,
                 model_parameters, simulation_parameters, model_name = None, 
                 training_matches = None):
        self.graphs = graphs
        self.blocks = blocks
        self.compares = compares
        self.classifier_name = classifier_name
        self.clustering_alg = clustering_alg
        self.statuses = statuses
        self.compartments = compartments
        self.transition_rules = transition_rules
        self.model_parameters = model_parameters
        self.simulation_parameters = simulation_parameters
        self.training_matches = training_matches
        
        # extracting the attributes of the individual graphs
        self.num_graphs = len(graphs)
        graph_attribute_dfs = {}
        for i in range(self.num_graphs):
            graph_attribute_dfs['graph_' + str(i)] = pd.DataFrame.from_dict(dict(graphs[i].nodes(data=True)), orient='index')
        self.graph_attribute_dfs = graph_attribute_dfs
        
        # calculating the comparison features of the graph(s)
        if len(graphs) == 1:
            feature_setup = FeatureSetup(blocks, compares, graph_attribute_dfs['graph_0'])
        else:
            feature_setup = FeatureSetup(blocks, compares, graph_attribute_dfs['graph_0'], graph_attribute_dfs['graph_1'])
        
        self.features = feature_setup.calculate_features()
        
        # fitting the model and predicting matches
        if training_matches is not None:
            match_classifier = MatchClassifier(classifier_name, self.features, training_matches)
        else:
            match_classifier = MatchClassifier(classifier_name, self.features)
            
        self.fit_model = match_classifier.fit_model()
        self.pred_matches = self.fit_model.predict(self.features)
        
        # integrating the network
        if len(graphs) == 1:
            network_integrator = NetworkIntegrator(graphs[0], self.pred_matches)
        else:
            network_integrator = NetworkIntegrator(graphs, self.pred_matches)

        self.integrated_network = network_integrator.integrate_network(clustering_alg)
        
        # running the diffusion model and storing the results
        custom_diffusion_model = CustomDiffusionModel(statuses, compartments,
                                             transition_rules, model_parameters)
        
        initialised_diffusion_model = InitialisedDiffusionModel(self.integrated_network, 
                                                                custom_diffusion_model)
        
        self.model = initialised_diffusion_model.get_initialised_model()
        self.trends = initialised_diffusion_model.run_diffusion_model(simulation_parameters)
        
        self.results_analyser = ResultsAnalyser(self.model, self.integrated_network, self.trends)
        
        
        