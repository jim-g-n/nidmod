# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 11:13:13 2022

@author: jnevin
-Supports ndlib CompositeModels
"""

import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm

class CustomDiffusionModel:
    def __init__(self, model_name, statuses, compartments, transition_rules, 
                 parameters):
        self.model_name = model_name
        self.statuses = statuses
        self.compartments = compartments
        self.transition_rules = transition_rules
        self.parameters = parameters
        
class InitialisedDiffusionModel:
    def __init__(self, graph, custom_diffusion_model):
        self.graph = graph
        self.custom_diffusion_model = custom_diffusion_model
        
    def initialise_model(self):
        self.model = gc.CompositeModel(self.graph)
    
    def add_statuses(self):
        for status in self.custom_diffusion_model.statuses:
            self.model.add_status(status)
            
    def add_compartments(self):
        set_compartments = {}
        for compartment_type in self.custom_diffusion_model.compartments:
            compartment_type_fun = getattr(cpm, compartment_type)
            for compartment in self.custom_diffusion_model.compartments[compartment_type]:
                set_compartments[compartment] = compartment_type_fun(*self.custom_diffusion_model.compartments
                                                [compartment_type][compartment])
        self.set_compartments = set_compartments
        
    def add_rules(self):
        for rule in self.custom_diffusion_model.transition_rules:
            self.model.add_rule(rule[0], rule[1], self.set_compartments[rule[2]])
            
    def set_initial_model_status(self):
        config = mc.Configuration()
        for parameter in self.custom_diffusion_model.parameters:
            config.add_model_parameter(*parameter)
        self.model.set_initial_status(config)
    