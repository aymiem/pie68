 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:45:59 2018

@author: arthur
"""
import os
import time
import shutil
import pandas as pd
from initialisation  import initialisation
from classement_population import rankings, choix_indiv_rg
from Pareto import drawPareto, addGeneration, is_pareto_efficient
from main import programme
from ecriture import nom_fichier_sortie, resetDonneeLecture, addDollars
from mutation import type_mutation
from crossover import crossover
from transf import dico_transf_init
from constantes import*
from lecture import emptyFolder

def programme_gen(max_iter, max_time, mut_type):
    print("Lancement du programme génétique")
    
    start = time.time()
    elapsed = 0    
    
    ### INITIALISATION
    
    #On remet à zéro le fichier de lecture des données
    resetDonneeLecture()
    
    # Si les dossiers n'existent pas on les recrée
    if not os.path.exists(paths.indicateurs_path):
        os.mkdir(paths.indicateurs_path)
        os.mkdir(paths.indicateurs_final_path)
        os.mkdir(paths.sitInits_path)
        os.mkdir(paths.solutions_path)
        os.mkdir(paths.solutions_final_path)
    
    
    #On vide les répertoires des précédentes solutions
    print('Suppression archives')
    emptyFolder(paths.indicateurs_path)
    emptyFolder(paths.indicateurs_final_path)
    emptyFolder(paths.sitInits_path)
    emptyFolder(paths.solutions_path)
    emptyFolder(paths.solutions_final_path)
    
    # Initialisation des dictionnaires pour les conversions de fichiers
    dico_transf_init()
    # Initialisation : création des individus de la première génération
    d = initialisation()  # Pour avoir un accès aux caractéristiques des missions
    ranked = rankings("1") # Classement de la premiere génération
    # Initialisation des données du Front de Pareto
    dataPareto = pd.DataFrame() 
    dataPareto = addGeneration(ranked, dataPareto) 
    # Initialisation du numero de la generation
    gen = 1 
    # Itialisation de l'opérateur de mutation
    mutation = type_mutation(mut_type)

    
    ### EVOLUTION par CROSSOVER et MUTATION
    
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
        # à partir de l'individu ayant le meilleur score opérationnel
        
        print("mutation sur generation", gen, "pour indic operationnel")        
        nom_fichier_sortie(gen, 4)
        changes_ope = mutation(str(gen-1), sols_ope["best"], 4, True, 4)

        # MUTATION pour créer individu "solution_gen_5" à partir
        # de l'individu ayant le meilleur score de lissage de maintenance

        print("mutation sur generation", gen, "pour indic maint lissage")
        nom_fichier_sortie(gen, 5)
        changes_lis = mutation(str(gen-1), sols_lis["best"], 5, False, 4)
        
        # On conserve les meilleurs individus de la génération précédente et on 
        # les intègre à la nouvelle génération sous les numéros "gen_6" et "gen_7"
        
        nom_fichier_sortie(gen, 6)
        os.rename("solutions\solution"+sols_ope["best"]+".csv", "solutions\solution"+gen_str+"6"+".csv")
        os.rename("indicateurs\indicateurs"+sols_ope["best"]+".csv", "indicateurs\indicateurs"+gen_str+"6"+".csv")
        if sols_ope["best"] != sols_lis["best"] :
            nom_fichier_sortie(gen, 7)
            os.rename("solutions\solution"+sols_lis["best"]+".csv", "solutions\solution"+gen_str+"7"+".csv")
            os.rename("indicateurs\indicateurs"+sols_lis["best"]+".csv", "indicateurs\indicateurs"+gen_str+"7"+".csv")

        # Classement de la nouvelle génération et ajout au front de Pareto
        ranked = rankings(gen_str)
        dataPareto = addGeneration(ranked, dataPareto)
        
        elapsed = time.time() - start
        
        print(elapsed)
        
        nom_fichier_sortie(gen, 8)
        nom_fichier_sortie(gen, 9)

    
    

    ### AFFICHAGE et SAUVEGARDE du front de Pareto
    
    #drawPareto(dataPareto)
    dataPareto.to_csv("dataPareto0.csv",sep=";",index=False,header=None)
    
    
    #On determine les solutions pareto-optimales et on les deplace dans les répertoires _final
    
    print("Selection des solutions pareto-optimales")
    pareto_opti = is_pareto_efficient(dataPareto)
    for ind in pareto_opti:
            print("Sélection du planning" + ind)
            shutil.copy("solutions\solution"+ind+".csv", "solutions_final\solution"+ind+".csv")
            addDollars("solutions\solution"+ind+".csv",d) #On aoute les dollars pour l'excel
            shutil.copy("indicateurs\indicateurs"+ind+".csv", "indicateurs_final\indicateurs"+ind+".csv")
            
    
    print ("temps total", elapsed, "sec")
    return dataPareto
pareto = programme_gen(3,100000,0)
