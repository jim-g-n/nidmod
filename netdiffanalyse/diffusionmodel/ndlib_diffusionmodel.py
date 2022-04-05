# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 11:13:13 2022

@author: jnevin
-Doesn't support cascading or conditional compartments
"""

import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm
from ndlib.utils import multi_runs

class CustomDiffusionModel:
    '''
    Class for storing a custom diffusion model
    
    The custom diffusion model can be defined based on the ndlib CompositeModel
    
    There are some standard models implemented as well
    '''
    def __init__(self, statuses, compartments, transition_rules, 
                 parameters, model_name = None):
        self.statuses = statuses
        self.compartments = compartments
        self.transition_rules = transition_rules
        self.parameters = parameters
        if model_name is not None:
            self.model_name = model_name
    
    # creates an SIR model with the given parameters
    @classmethod
    def SIR(cls, beta, gamma, fraction_infected):
        statuses = ['Susceptible', 'Infected', 'Removed']
        compartments = {'NodeStochastic': {'c1': [beta, 'Infected'], 'c2': [gamma]}}
        transition_rules = [["Susceptible", "Infected", "c1"], ["Infected", "Removed", "c2"]]
        model_parameters = [['fraction_infected', fraction_infected]]
        model_name = 'SIR'
        return cls(statuses, compartments, transition_rules, model_parameters,
                   model_name)
   
    # creates a threshold model with the given parameters
    @classmethod
    def Threshold(cls, threshold, fraction_infected):
        statuses = ['Susceptible', 'Infected']
        compartments = {'NodeThreshold': {'c1': [threshold, 'Infected']}}
        transition_rules = [['Susceptible', 'Infected', 'c1']]
        model_parameters = [['fraction_infected', fraction_infected]]
        model_name = 'Threshold'
        return cls(statuses, compartments, transition_rules, model_parameters,
                   model_name)
        
class InitialisedDiffusionModel:
    '''
    Class to initialise and run the supplied custom diffusion model on the supplied graph
    '''
    def __init__(self, graph, custom_diffusion_model):
        self.graph = graph
        self.model = gc.CompositeModel(self.graph)
    
        # adding the model statuses
        for status in custom_diffusion_model.statuses:
            self.model.add_status(status)
        
        # adding the model compartments
        set_compartments = {}
        for compartment_type in custom_diffusion_model.compartments:
            compartment_type_fun = getattr(cpm, compartment_type)
            for compartment in custom_diffusion_model.compartments[compartment_type]:
                set_compartments[compartment] = compartment_type_fun(*custom_diffusion_model.compartments
                                                [compartment_type][compartment])
        
        # adding the model rules
        for rule in custom_diffusion_model.transition_rules:
            self.model.add_rule(rule[0], rule[1], set_compartments[rule[2]])
         
        # setting the model initial status parameters    
        config = mc.Configuration()
        for parameter in custom_diffusion_model.parameters:
            config.add_model_parameter(*parameter)
        self.model.set_initial_status(config)
    
    # returns the initialised diffusion model
    def get_initialised_model(self):
        return self.model
    
    # performs an ndlib multi_runs based on given parameters
    def run_diffusion_model(self, parameters):
        trends = multi_runs(self.model, *parameters)
        return trends

    