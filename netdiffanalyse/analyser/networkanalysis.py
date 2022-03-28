# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:18:23 2022

@author: jnevin
"""
import networkx as nx
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.mpl.OpinionEvolution import OpinionEvolution
import future.utils
import numpy as np

class ResultsAnalyser:
    def __init__(self, model, graph, trends):
        self.model = model
        self.graph = graph
        self.trends = trends
        statuses = model.available_statuses
        self.srev = {v: k for k, v in future.utils.iteritems(statuses)}
        self.num_nodes = self.graph.number_of_nodes()
        self.num_sims = len(trends)
        
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
    
    def plot_diff_trend(self, plot_params = None):
        viz = DiffusionTrend(self.model, self.trends)
        if plot_params is not None:
            viz.plot(*plot_params)
        else:
            viz.plot()
        
    def plot_diff_prevalence(self, plot_params = None):
        viz = DiffusionPrevalence(self.model, self.trends)
        if plot_params is not None:
            viz.plot(*plot_params)
        else:
            viz.plot()        
    
    def plot_opinion_evolution(self, plot_params = None):
        viz = OpinionEvolution(self.model, self.trends)
        if plot_params is not None:
            viz.plot(*plot_params)
        else:
            viz.plot()
        
    def get_aggregate_statistics(self):
        # calculate aggregate statistics (peaks, final, times to peak and stable)
        #stability_rand.append([trends[j]['trends']['node_count'][0].index(trends[j]['trends']['node_count'][0][-1]) for j in range(10)])
        #peak_time_rand.append([trends[j]['trends']['node_count'][1].index(max(trends[j]['trends']['node_count'][1])) for j in range(10)])
        
        final_vals = []
        peak_vals = []
        
        for i in range(self.num_sims):
            final_vals.append([self.trends[i]['trends']['node_count'][j][-1] 
                                   for j in self.srev])
            peak_vals.append([max(self.trends[i]['trends']['node_count'][j]) 
                                   for j in self.srev])
        peak_vals = np.mean(np.array(peak_vals)/self.num_nodes, axis = 0)
        final_vals = np.mean(np.array(final_vals)/self.num_nodes, axis = 0)
        
        
        peak_state_names = [x + '_peak' for x in list(self.srev.values())]
        final_state_names = [x + '_final' for x in list(self.srev.values())]
        
        measurement_names = peak_state_names + final_state_names
        measurement_values = np.concatenate((peak_vals, final_vals))
        aggregate_measurements = dict(zip(measurement_names, 
                                          measurement_values))
        
        return aggregate_measurements
        
        
    
    
        
        
