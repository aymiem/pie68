#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:45:59 2018

@author: arthur
"""
import timeit as tt
import pandas as pd
import numpy as np
from initialisation  import initialisation
from classement_population import rankings, choix_indiv_rg
from selection_operator import Roulette_wheel_selection, evaluation_fitness
from Pareto import drawPareto, addGeneration

def programme_gen(max_iter, max_time, indic_ref_1, indic_ref_2):
    print("Lancement du programme génétique")
    start = tt.default_timer()
    elapsed = 0    
    initialisation()
    dataPareto = pd.DataFrame()
    dataPareto = addGeneration(rankings("1"), dataPareto)   
    
    gen = 1
    
    while((elapsed <= max_time) & (gen < max_iter)):
        batch = select_batch(gen, indic_ref_1, indic_ref_2)
        addGeneration(str(gen), dataPareto)
        elapsed = start - tt.default_timer()
        gen += 1
    
#    drawPareto(dataPareto)
    return dataPareto

def select_batch(gen, indic_ref_1, indic_ref_2):
    # returns 
    ranked = rankings(gen)
    sol1 = choix_indiv_rg(ranked, gen, indic_ref_1, 1)
    sol2 = choix_indiv_rg(ranked, gen, indic_ref_2, 1)
    batch = np.array(range(10))
    batch = np.delete(batch, sol1)
    batch = np.delete(batch, sol2)
    batch = np.random.choice(batch, size = 3)
    
    batch = np.append(batch, [sol1,sol2])
    batch = np.add(batch, 10)
     
    return list(batch)

pareto = programme_gen(1,100000, "var_maint", "pot_perdu")