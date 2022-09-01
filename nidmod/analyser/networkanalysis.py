# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 15:18:23 2022

@author: jnevin
"""
import networkx as nx
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
from ndlib.viz.mpl.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.mpl.TrendComparison import DiffusionTrendComparison
import future.utils
import numpy as np
import pandas as pd

class ResultsAnalyser:
    '''
    Class for analysing diffusion results and the graph itself
    '''
    def __init__(self, model, graph, trends):
        self.model = model
        self.graph = graph
        self.trends = trends
        statuses = model.available_statuses
        self.srev = {v: k for k, v in future.utils.iteritems(statuses)}
        self.num_nodes = self.graph.number_of_nodes()
        self.num_sims = len(trends)
     
    # returns a dictionary of graph properties
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
    
    # plots the diffusion trends
    def plot_diff_trend(self, plot_params = None):
        viz = DiffusionTrend(self.model, self.trends)
        if plot_params is not None:
            viz.plot(*plot_params)
        else:
            viz.plot()
    
    # plots the diffusion prevalence (derivative)
    def plot_diff_prevalence(self, plot_params = None):
        viz = DiffusionPrevalence(self.model, self.trends)
        if plot_params is not None:
            viz.plot(*plot_params)
        else:
            viz.plot()        
    
    # returns a dictionary of statistics from the trends
    def get_average_statistics(self):
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
        average_measurements = dict(zip(measurement_names, 
                                          measurement_values))
        
        return average_measurements
    
class MultiResultsAnalyser:
    '''
    Class for jointly analysing multiple graphs and diffusion results
    '''
    def __init__(self, results_analysers):
        self.results_analysers = results_analysers
    
    # returns a dataframe of average trend statistics for the indexed graphs
    def get_average_stat_comparison(self, indices = None):
        stat_compare_df = pd.DataFrame()
        if indices is None:
            indices = np.arange(len(self.results_analysers))
        for idx in indices:
            stat_compare_df = stat_compare_df.append(self.results_analysers[idx].get_average_statistics(),
                                   ignore_index = True)
        stat_compare_df.index = indices
        return stat_compare_df
    
    # returns a dataframe of graph statistics for the indexed graphs
    def get_graph_prop_comparison(self, indices = None):
        graph_compare_df = pd.DataFrame()
        if indices is None:
            indices = np.arange(len(self.results_analysers))
        for idx in indices:
            graph_compare_df = graph_compare_df.append(self.results_analysers[idx].get_graph_properties(),
                                   ignore_index = True)
        graph_compare_df.index = indices
        return graph_compare_df
        
    def plot_trend_comparison(self, indices, statuses = 'Infected'):
        # plot sets of models and trends, haven't implemented plotting parms yet
        viz = DiffusionTrendComparison([self.results_analysers[i].model for i in indices],
                                       [self.results_analysers[i].trends for i in indices],
                                       statuses = statuses)
        viz.plot()
        
        
    
    
        
        
