#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:45:59 2018

@author: arthur
"""
import os
import timeit as tt
import pandas as pd
import numpy as np
from initialisation  import initialisation
from classement_population import rankings, choix_indiv_rg
from selection_operator import *
from Pareto import drawPareto, addGeneration
from crossover import calculs
from main import programme
from ecriture import nom_fichier_sortie
from mutation import mutation

def programme_gen(max_iter, max_time):
    print("Lancement du programme génétique")
    ## Initialisation 
    start = tt.default_timer() # timer
    elapsed = 0    
    initialisation()
    ranked = rankings("1") #premiere génération
    dataPareto = pd.DataFrame()
    dataPareto = addGeneration(ranked, dataPareto)
    gen = 1 # initialisation du numero de la generation
    
    while((elapsed <= max_time) & (gen < max_iter)):
        gen +=1
        gen_str = str(gen)
        
        best_ope = choix_indiv_rg(ranked, gen_str, "fitness_ope", 1)
        worst_ope = choix_indiv_rg(ranked, gen_str, "fitness_ope", 0)
        med_ope = choix_indiv_rg(ranked, gen_str, "fitness_ope", 0.5)
        
        sitInit_ope = crossover([best_ope, med_ope, worst_ope], True, gen_str)
        
        indiv=0
        for x in sitInit_ope:
            nom_fichier_sortie(gen,indiv)
            programme(False, x)
            i+=1
    
        best_lis = choix_indiv_rg(ranked, gen_str, "fitness_lis", 1)
        worst_lis = choix_indiv_rg(ranked, gen_str, "fitness_lis", 0)
        med_lis = choix_indiv_rg(ranked, gen_str, "fitness_lis", 0.5)
        
        sitInit_lis = crossover([best_lis, med_lis, worst_lis], True, gen_str)
                
        for x in sitInit_lis:
            nom_fichier_sortie(gen,indiv)
            programme(False, x)
            i+=1
        
        nom_fichier_sortie(gen, 4)
        changes_ope = mutation(str(gen-1), best_ope[1], 4, True)
        
        nom_fichier_sortie(gen, 5)
        changes_lis = mutation(str(gen-1), best_lis[1], 5, False)
        
        if changes_ope == True: 
            os.rename("solution"+best_ope+".csv", "solution"+gen_str+"6"+".csv")

        if changes_lis == True: 
            os.rename("solution"+best_lis+".csv", "solution"+gen_str+"7"+".csv")
        
        ranked = rankings(gen_str)
        dataPareto = addGeneration(ranked, dataPareto)
        elapsed = start - tt.default_timer()


    drawPareto(dataPareto)
    return dataPareto

pareto = programme_gen(1,100000)