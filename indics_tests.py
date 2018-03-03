import time
import numpy as np
import pandas as pd
from classement_population import rankings, choix_indiv_rg
from Pareto import drawPareto, addGeneration
from mutation import type_mutation
from transf import dico_transf_init
from constantes import constantes
from ecriture import nom_fichier_sortie
from main import programme
from selection_operator import fitness_lis_indiv, fitness_ope_indiv

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
    # Initialisation des données du Front de Pareto
    dataPareto = pd.DataFrame() 
    dataPareto = addGeneration(ranked, dataPareto) 
    
    # Choix du type de la mutation
    mutation = type_mutation(num)
    for generation in [2,3]:
        for i in range(10):
            print("Generation", generation, "Iter ",i)
            nom_fichier_sortie(generation,i)
            changes_lis = mutation(0, best_liss, 0, False, 1)
            if changes_lis == True: 
                print("mutation operateur lissage maintenance OK in ", time.time() - start_time)
                iteration_reussie += 1
        # Classement et ajout des nouvelles solutions
        ranked = rankings(str(generation)) 
        dataPareto = addGeneration(ranked, dataPareto)
        
    print("nombre d'itérations réussies :", iteration_reussie)
       
    drawPareto(dataPareto)
    dataPareto.to_csv("ParetoTestMutArriereLis.csv",sep=";",index=False,header=None)
    
    
    
    
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
        print("Iter ",i)
        changes_ope = mutation(0, best_ope, 0, True, 1)
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



# INSCIRE "solutionTest.csv" dans "donnees_lecture.csv"

def test_pareto_optimalite(nb_iter):
    
    # 0: mutation_arriere, 1: mutation_DSP, 2: mutation_i_aleatoire
    indice_mutation = [0, 1, 2]
    
    scores_cumules =  pd.DataFrame(np.nan, index = range(4), columns = range(nb_iter))
    scores_cumules.index = ["mut_arr", "mut_DSP", "mut_i_al", "no_mut"]
    
    fitness =  pd.DataFrame(np.nan, index = range(8), columns = range(nb_iter))
    fitness.index = ["fit_ope_mut_arr", "fit_lis_mut_arr", "fit_ope_mut_DSP", \
                     "fit_lis_mut_DSP", "fit_ope_mut_i_al", "fit_lis_mut_i_al",\
                     "fit_ope_no_mut", "fit_lis_no_mut"]
    
    nb_solution_PO = 0
    for i in range(nb_iter):
        new_indic, new_df = programme(True, 0)
        fitness.loc["fit_ope_no_mut"][i] = fitness_ope_indiv(new_indic)
        fitness.loc["fit_lis_no_mut"][i] = fitness_lis_indiv(new_indic)

        if is_Pareto_opt(fitness.loc["fit_ope_no_mut":"fit_lis_no_mut",:i].T,\
                         fitness.loc["fit_ope_no_mut"][i], fitness.loc["fit_lis_no_mut"][i], "no_mut") :
            nb_solution_PO += 1
            scores_cumules.loc["no_mut"][i] = nb_solution_PO
        print(scores_cumules)
        
    for mut_type in indice_mutation :
        nb_solution_PO = 0
        for it in range(nb_iter):
            ranked = rankings("1")
            sol = choix_indiv_rg(ranked, "1", "fitness_lis", 1)
            mutation = type_mutation(mut_type)
            mutation(0, sol, 0, True, 1)
            # A chaque iteration on réécrit sur la solution test
            nom_mut = scores_cumules.index[indice_mutation[mut_type]]
            print(nom_mut)
            fitness.loc["fit_ope_"+nom_mut][it] = fitness_ope_indiv("solutionTest.csv")
            fitness.loc["fit_lis_"+nom_mut][it] = fitness_lis_indiv("solutionTest.csv")

            if is_Pareto_opt(fitness.loc["fit_ope_"+nom_mut:"fit_lis_"+nom_mut,:it-1].T,\
                         fitness.loc["fit_ope_"+nom_mut][it], fitness.loc["fit_lis_"+nom_mut][it],nom_mut) :
                nb_solution_PO += 1
                scores_cumules.loc[nom_mut][it] = nb_solution_PO
            print(scores_cumules)

    return fitness, scores_cumules
            
def is_Pareto_opt(fit_values_df, new_score_ope, new_score_lis, nom_m):
    print(fit_values_df, type(new_score_ope), new_score_lis, nom_m)
    
    if len(fit_values_df.index) == 1 :
        return True
    else :
        meilleures_sol = fit_values_df.loc[(fit_values_df['fit_ope_'+nom_m] >= new_score_ope) \
                                | (fit_values_df['fit_lis_'+nom_m] >= new_score_lis)]
        print(meilleures_sol,len(meilleures_sol))
        res = True
        if len(meilleures_sol) < 1 :
            return res
        else :
            for row in meilleures_sol.index :
                print(row)
                if (fit_values_df['fit_ope_'+nom_m][row] >= new_score_ope) and \
                    (fit_values_df['fit_lis_'+nom_m][row] >= new_score_lis):
                    res = False
                    break     
            return res
    
    
    
    
    
    