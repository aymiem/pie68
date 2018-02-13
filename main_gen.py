 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:45:59 2018

@author: arthur
"""
import os
import time
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
    
    start = time.time() # timer
    elapsed = 0    
    
    ## INITIALISATION
    
    # Initialisation des individus de la première génération
    initialisation()
    ranked = rankings("1") # Classement de la premiere génération
    # Initialisation des données du Front de Pareto
    dataPareto = pd.DataFrame() 
    dataPareto = addGeneration(ranked, dataPareto) 
    # Initialisation du numero de la generation
    gen = 1 
    
    ## EVOLUTION par CROSSOVER et MUTATION
    
    while((elapsed <= max_time) & (gen < max_iter)):
        gen +=1
        gen_str = str(gen)
        
        # CROSSOVER pour les individus X0, X1 selon indicateur opérationnel
        
        # dictionnaire des solutions pour le crossover
        sols_ope = {}
        sols_ope["best"] = choix_indiv_rg(ranked, gen_str, "fitness_ope", 1)
        sols_ope["worst"] = choix_indiv_rg(ranked, gen_str, "fitness_ope", 0)
        sols_ope["median"] = choix_indiv_rg(ranked, gen_str, "fitness_ope", 0.5)
        # crossover
        print("Crossover sur generation", gen, "pour indic operationnel")
        sitInit_ope = crossover(sols_ope, gen)
        # génération des deux nouveaux individus "solution_gen_0" et "solution_gen_1"
        indiv=0
        for x in sitInit_ope:
            nom_fichier_sortie(gen,indiv)
            programme(False, x)
            indiv+=1
    
        # CROSSOVER pour les individus X2, X3 selon indicateur de maintenance
        
        # dictionnaire des solutions pour le crossover
        sols_lis = {}
        sols_lis["best"]  = choix_indiv_rg(ranked, gen_str, "fitness_lis", 1)
        sols_lis["worst"] = choix_indiv_rg(ranked, gen_str, "fitness_lis", 0)
        sols_lis["median"]  = choix_indiv_rg(ranked, gen_str, "fitness_lis", 0.5)
        # crossover
        print("crossover sur generation", gen, "pour indic maint lissage")
        sitInit_lis = crossover(sols_lis, gen)
        # génération des deux nouveaux individus "solution_gen_2" et "solution_gen_3"
        for x in sitInit_lis:
            nom_fichier_sortie(gen,indiv)
            programme(False, x)
            indiv+=1
        
        # MUTATION pour créer individu "solution_gen_4" 
        # à partir du meilleur individu selon indicateur opérationnel
        
        print("mutation sur generation", gen, "pour indic operationnel")        
        nom_fichier_sortie(gen, 4)
        changes_ope = mutation(str(gen-1), sols_ope["best"], 4, True)

        # MUTATION pour créer individu "solution_gen_5" 
        # à partir du meilleur individu selon indicateur de maintenance

        print("mutation sur generation", gen, "pour indic maint lissage")
        nom_fichier_sortie(gen, 5)
        changes_lis = mutation(str(gen-1), sols_lis["best"], 5, False)
        
        # On conserve les meilleurs individus de la génération précédente et on 
        # les intègre à la nouvelle génération sous les numéros "gen_6" et "gen_7"
        
        nom_fichier_sortie(gen, 6)
        if changes_ope == True: 
            os.rename("solution"+sols_ope["best"]+".csv", "solution"+gen_str+"6"+".csv")
            os.rename("indicateurs"+sols_ope["best"]+".csv", "indicateurs"+gen_str+"6"+".csv")
        nom_fichier_sortie(gen, 7)
        if changes_lis == True: 
            os.rename("solution"+sols_lis["best"]+".csv", "solution"+gen_str+"7"+".csv")
            os.rename("indicateurs"+sols_lis["best"]+".csv", "indicateurs"+gen_str+"7"+".csv")

        # Classement de la nouvelle génération
        ranked = rankings(gen_str)
        dataPareto = addGeneration(ranked, dataPareto)
        
        elapsed = time.time() - start
        
        print(elapsed)
        
        nom_fichier_sortie(gen, 8)
        nom_fichier_sortie(gen, 9)

    print ("temps total", elapsed, "sec")
    ## AFFICHAGE
    
    drawPareto(dataPareto)
    dataPareto.to_csv("dataPareto0.csv",sep=";",index=False,header=None)

    return dataPareto

pareto = programme_gen(5,100000)
