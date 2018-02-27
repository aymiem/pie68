# -*- coding: utf-8 -*-
import time
import pandas as pd
from classement_population import rankings, choix_indiv_rg
from Pareto import drawPareto, addGeneration
from mutation import mutation
from crossover import crossover
from transf import dico_transf_init
from constantes import constantes

### ATTENTION : inscrire "solutionTest.csv" dans le fichier "donnees_lecture.csv"

def test_operateur_mutation1():
    
    # Initialisation des dictionnaires pour les conversions de fichiers
    dico_transf_init()
    # Classement d'une génération
    ranked = rankings("1") 
    # Initialisation des données du Front de Pareto
#    dataPareto = pd.DataFrame() 
#    dataPareto = addGeneration(ranked, dataPareto) 
    # récupération meilleures solutions
    best_ope = choix_indiv_rg(ranked, "1", "fitness_ope", 1)
    best_liss = choix_indiv_rg(ranked, "1", "fitness_lis", 1)
    
#    start_time = time.time()
#    constantes.typechoix = 0
#    #constantes.typechoix = 1
#    
#    changes_ope = mutation(0, best_ope, 0, True, 10)
#    
#    if changes_ope == True: 
#        print("mutation operateur opérationnel with cravate OK in ", time.time() - start_time)
#        
#    start_time = time.time()
#    constantes.typechoix = 1
#    
#    changes_ope = mutation(0, best_ope, 0, True, 50)
#    
#    if changes_ope == True: 
#        print("mutation operateur opérationnel OK in ", time.time() - start_time)
#            
    start_time = time.time()
    changes_liss = mutation(0, best_liss, 0, True, 50)
    
    if changes_liss == True: 
        print("mutation operateur lissage maintenance OK in ", time.time() - start_time)


