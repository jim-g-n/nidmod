# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:36:59 2022

@author: jnevin

-Only works for dedupe in a single df at the moment
-Only has exact and string comparisons implemented
"""

import recordlinkage

def read_comparisons(comparer, compare_dict):
    
    for comparison in compare_dict['exact']:
        comparer.exact(left_on = comparison[0], right_on = comparison[1], label = comparison[2])
    
    for comparison in compare_dict['string']:
        comparer.string(left_on = comparison[0], right_on = comparison[1], method=comparison[2],
                      threshold=comparison[3], label=comparison[4])
    
    return comparer

class FeatureSetup: # at the moment only works for dedupe in single df
    '''
    A class to store feature setups
    '''
    def __init__(self, blocks, compare_dict, df):
        self.blocks = blocks
        self.compare_dict = compare_dict
        self.df = df
    
    def initialise_indexer(self):
        indexer = recordlinkage.Index()
        if self.blocks:
            for block in self.blocks:
                indexer.block(block)
        else:
            indexer.full()
        self.indexer = indexer
        
    def get_candidate_links(self):
        self.candidate_links = self.indexer.index(self.df)
        
    def read_comparisons(comparer, compare_dict):
        
        for comparison in compare_dict['exact']:
            comparer.exact(left_on = comparison[0], right_on = comparison[1], label = comparison[2])
        
        for comparison in compare_dict['string']:
            comparer.string(left_on = comparison[0], right_on = comparison[1], method=comparison[2],
                          threshold=comparison[3], label=comparison[4])
        
        return comparer
        
    def initialise_comparer(self):
        comparer = recordlinkage.Compare()
        comparer = read_comparisons(comparer, self.compare_dict)
        self.comparer = comparer

class ComparisonFeatures:
    '''
    A class to store and calculate comparison features
    '''
    def __init__(self, feature_setup):
        self.comparer = feature_setup.comparer
        self.candidate_links = feature_setup.candidate_links
        self.df = feature_setup.df
    
    def calculate_features(self):
        self.features = self.comparer.compute(self.candidate_links, self.df)
        
#class MatchesCalculation:
#    def __init__(self, comparison_features, )
        

        

        