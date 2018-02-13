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
from crossover import crossover

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
        
        # dictionnaire des solutions pour le crossover
        sols_ope = {}
        sols_ope["best"] = choix_indiv_rg(ranked, gen_str, "fitness_ope", 1)
        sols_ope["worst"] = choix_indiv_rg(ranked, gen_str, "fitness_ope", 0)
        sols_ope["median"] = choix_indiv_rg(ranked, gen_str, "fitness_ope", 0.5)
        
        print("crossover sur generation", gen, "pour indic operationnel")
        sitInit_ope = crossover(sols_ope, gen)
        
        indiv=0
        for x in sitInit_ope:
            nom_fichier_sortie(gen,indiv)
            programme(False, x)
            indiv+=1
    
        sols_lis = {}
        sols_lis["best"]  = choix_indiv_rg(ranked, gen_str, "fitness_lis", 1)
        sols_lis["worst"] = choix_indiv_rg(ranked, gen_str, "fitness_lis", 0)
        sols_lis["median"]  = choix_indiv_rg(ranked, gen_str, "fitness_lis", 0.5)
        
        print("crossover sur generation", gen, "pour indic maint lissage")
        sitInit_lis = crossover(sols_lis, gen)
                
        for x in sitInit_lis:
            nom_fichier_sortie(gen,indiv)
            programme(False, x)
            indiv+=1
        
        print("mutation sur generation", gen, "pour indic operationnel")        
        nom_fichier_sortie(gen, 4)
        changes_ope = mutation(str(gen-1), sols_ope["best"], 4, True)
        
        print("mutation sur generation", gen, "pour indic maint lissage")
        nom_fichier_sortie(gen, 5)
        changes_lis = mutation(str(gen-1), sols_lis["best"], 5, False)
        
        if changes_ope == True: 
            os.rename("solution"+sols_ope["best"]+".csv", "solution"+gen_str+"6"+".csv")
            os.rename("indicateurs"+sols_ope["best"]+".csv", "indicateurs"+gen_str+"6"+".csv")

        if changes_lis == True: 
            os.rename("solution"+sols_lis["best"]+".csv", "solution"+gen_str+"7"+".csv")
            os.rename("indicateurs"+sols_lis["best"]+".csv", "indicateurs"+gen_str+"7"+".csv")

        
        ranked = rankings(gen_str)
        dataPareto = addGeneration(ranked, dataPareto)
        elapsed = start - tt.default_timer()


    drawPareto(dataPareto)
    return dataPareto

pareto = programme_gen(2,100000)
