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
from crossover import calculs

def programme_gen(max_iter, max_time, indic_ref_1, indic_ref_2):
    print("Lancement du programme génétique")
    start = tt.default_timer()
    elapsed = 0    
    initialisation()
    ranked = rankings("1")
    dataPareto = pd.DataFrame()
    dataPareto = addGeneration(ranked, dataPareto)
    gen = 1
    gen_str = str(gen)

    best_1 = choix_indiv_rg(ranked, gen_str, indic_ref_1, 1)
    worst_1 = choix_indiv_rg(ranked, gen_str, indic_ref_1, 0)
    med_1 = choix_indiv_rg(ranked, gen_str, indic_ref_1, 0.5)
    
    
    best_2 = choix_indiv_rg(ranked, gen_str, indic_ref_2, 1)
    worst_2 = choix_indiv_rg(ranked, gen_str, indic_ref_2, 0)
    med_2 = choix_indiv_rg(ranked, gen_str, indic_ref_2, 0.5)
    
    avion, dic_changes = calculs([best_1, med_1, worst_1])
    dfs = generateur(avion,2,2,dic_changes,gen_str)
    
    programme(False, dfs[0])
    programme(False,dfs[1])
    
    avion, dic = calculs([best_1, med_1, worst_1])
    generateur(avion,2,2,dic_chg,gen_str)
    
    while((elapsed <= max_time) & (gen < max_iter)):
        batch = select_batch(gen, indic_ref_1, indic_ref_2)
        addGeneration(str(gen), dataPareto)
        elapsed = start - tt.default_timer()
        gen += 1
    
#    drawPareto(dataPareto)
    return dataPareto


pareto = programme_gen(1,100000, "var_maint", "pot_perdu")