# -*- coding: utf-8 -*-
import time
import pandas as pd
from classement_population import rankings, choix_indiv_rg
from Pareto import drawPareto, addGeneration
from mutation import *
from transf import dico_transf_init
from constantes import constantes
from ecriture import nom_fichier_sortie

### ATTENTION : inscrire "solutionTest.csv" dans le fichier "donnees_lecture.csv"

def test_mutation_indic_lis(num):
    # Permet de calculer sur 100 itérations le nombre de fois où la mutation de 
    # type choisi (0, 1, 2 ou 3) a réussi à générer une solution fille ayant un
    # score de fitness lissage supérieur à celui de la meilleure solution de la 
    # génération initiale.
    
    # Initialisation des dictionnaires pour les conversions de fichiers
    dico_transf_init()
    # Classement d'une génération
    ranked = rankings("1") 
    # récupération meilleure solution lissage
    best_liss = choix_indiv_rg(ranked, "1", "fitness_lis", 1)
    constantes.typechoix = 1
    iteration_reussie = 0
    start_time = time.time()
    
    # Choix du type de la mutation
    mutation = type_mutation(num)
    
    for i in range(100):
        print("Iter ",i)
        changes_lis = mutation(0, best_liss, 0, False, 1)
        if changes_lis == True: 
            print("mutation operateur lissage maintenance OK in ", time.time() - start_time)
            iteration_reussie += 1
    print("nombre d'itérations réussies :", iteration_reussie)
    
    
def test_mutation_indic_ope(num):
    # Permet de calculer sur 100 itérations le nombre de fois où la mutation de 
    # type choisi (0, 1, 2 ou 3) a réussi à générer une solution fille ayant un
    # score de fitness opérationnel supérieur à celui de la meilleure solution 
    # de la génération initiale.
    
    # Initialisation des dictionnaires pour les conversions de fichiers
    dico_transf_init()
    # Classement d'une génération
    ranked = rankings("1") 
    # récupération meilleure solution opérationnelle
    best_ope = choix_indiv_rg(ranked, "1", "fitness_ope", 1)
    iteration_reussie = 0
    start_time = time.time()
    
    if best_ope == "0":
        constantes.typechoix = 1
    else :
        constantes.typechoix = 0

    # Choix du type de la mutation
    mutation = type_mutation(num)

    for i in range(100):
        changes_ope = mutation(0, best_ope, 0, True, 1)
        print("Iter ",i)
        if changes_ope == True: 
            print("Mutation operateur operationnel ok in ", time.time() - start_time)
            iteration_reussie += 1
    print("nombre d'itérations réussies :", iteration_reussie)


def test_mutation_cravate(num):
    
    # On cherche ici, à partir de la solution présentant le meilleur score 
    # pour l'indicateur de lissage de maintenance, à améliorer le score 
    # opérationnel de cette solution, sans dégrader son score "lissage". Pour 
    # ce faire on utilise dans le re-bouclage l'algorithme glouton avec l'option 
    # "cravate" qui présente de bonnes performances opérationnelles lors de la  
    # création d'une solution.
    
    # Initialisation des dictionnaires pour les conversions de fichiers
    dico_transf_init()
    # Initialisation : création des individus de la première génération
    ranked = rankings("1") # Classement de la premiere génération
    # Initialisation des données du Front de Pareto
    dataPareto = pd.DataFrame() 
    dataPareto = addGeneration(ranked, dataPareto) 
    
    # Récupération de la solution de la génération 1 ayant le meilleur score "lissage"
    best_liss = choix_indiv_rg(ranked, "1", "fitness_lis", 1)
    # On utilise le re-bouclage avec option "cravate"
    constantes.typechoix = 0
    iteration_reussie = 0    
    gen = 2
    
    # Choix du type de la mutation
    mutation = type_mutation(num)  
    
    for i in range(10):
        nom_fichier_sortie(gen,i)
        print("Iter ",i)
        changes_ope = mutation(0, best_liss, 0, True, 3)
        if changes_ope == True: 
            print("Fitness operationnelle améliorée par mutation_cravate")
            iteration_reussie += 1
    
    print("Nombre d'itérations réussies : ", iteration_reussie)

    # Classement et ajout des nouvelles solutions
    ranked = rankings("2") 
    dataPareto = addGeneration(ranked, dataPareto)
    
    drawPareto(dataPareto)
    
    dataPareto.to_csv("ParetoTestCravate.csv",sep=";",index=False,header=None)

    
def type_mutation(num):  
    # Fonction appelant la mutation choisie pour le test
    if num == 0 :
        return mutation_arriere
    elif num == 1 :
        return mutation_avant
    elif num == 2 :
        return mutation_del_some_planes
    elif num == 3 :
        return mutation_i_aléatoire
    else : 
        return mutation_arriere