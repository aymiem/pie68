import os
from lecture import *
import csv
from objects import *
from constantes import *
import pandas as pd
import numpy as np


def fitness_operationnel(df_classement):
    # evalue un score (ou fitness) de 3 indicateurs opérationnels aggrégés :
    # moyenne_heures_perdues, min_pot_perdu et last_cravate
    # pour les individus d'une même génération
    
    df_RWS = df_classement
    
    # on récupère les poids des indicateurs
    df_poids = pd.read_csv( 'poids_indicateurs.csv', sep=";",header=0,index_col=0)
    
    df_RWS["fitness_ope"] = np.zeros(len(df_RWS))
    
    # somme pondérée des scores par indicateurs - normalisée et à maximiser
    df_RWS["fitness_ope"] = - np.asarray(df_RWS["moy_pot_perdu"])*(df_poids.loc["moy_pot_perdu","poids"]) \
            + np.asarray(df_RWS["min_pot_perdu"])*(df_poids.loc["min_pot_perdu","poids"]) \
            - np.asarray(df_RWS["last_cravate"])*(df_poids.loc["last_cravate","poids"]) 
    
    #print(df_RWS)
    return df_RWS.sort_values(by=["fitness_ope"], ascending=False)



def fitness_ope_indiv(solution):
    # evalue un score (ou fitness) de 3 indicateurs opérationnels aggrégés :
    # moyenne_heures_perdues, min_pot_perdu et last_cravate pour un individu 
    # normalisée dans l'ordre de grandeur des deux premiers critères
    
    df_poids = pd.read_csv( 'poids_indicateurs.csv', sep=";",header=0,index_col=0)
    
    if isinstance(solution, dict): # si l'input est un dictionnaire
        f_value = - solution["moy_pot_perdu"]*(df_poids.loc["moy_pot_perdu","poids"]) \
            + solution["min_pot_perdu"]*(df_poids.loc["min_pot_perdu","poids"]) \
            - solution["last_cravate"]*(df_poids.loc["last_cravate","poids"]) 
    
    else :
        if isinstance(solution, str): # si l'input est le nom de l'individu
            df_indics = pd.DataFrame.from_csv("indicateurs/indicateurs"+solution[8:10].replace(".","")+".csv", header=None, sep=';', index_col=0)
        else:
            df_indics = solution # si l'input est déjà le dataframe des indicateurs de la solution
        
        # Calcul de l'indic aggrégé opérationnel : à maximiser
        f = - (df_poids.loc["moy_pot_perdu","poids"])*df_indics.loc["moy_pot_perdu"] + (df_poids.loc["min_pot_perdu","poids"])*df_indics.loc["min_pot_perdu"] - (df_poids.loc["last_cravate","poids"])*df_indics.loc["last_cravate"]
        f_value = f.loc[1]
        
    return f_value



def fitness_lissage(df_classement):
    # evalue un score (ou fitness) de 2 indicateurs liés à la maintenance et
    # aggrégés : maint_var, delta_maint, pour les individus d'une même génération
    
    df_RWS = df_classement
    df_poids = pd.read_csv('poids_indicateurs.csv',sep=";",header=0,index_col=0)
    
    df_RWS["fitness_lis"] = np.zeros(len(df_RWS))
    
    # somme pondérée des scores par indicateurs - normalisée et à maximiser
    for nom_indic in ["var_maint", "delta_maint"]:
        df_RWS["fitness_lis"] = df_RWS["fitness_lis"] - np.asarray(df_RWS[nom_indic])*(df_poids.loc[nom_indic,"poids"])
    
    #print(df_RWS)
    return df_RWS.sort_values(by=["fitness_lis"], ascending=False)


def fitness_lis_indiv(solution):
    # evalue un score (ou fitness) de 2 indicateurs liés à la maintenance et
    # aggrégés : maint_var, delta_maint, pour les individus d'une même génération

    df_poids = pd.read_csv('poids_indicateurs.csv',sep=";",header=0,index_col=0)

    if isinstance(solution, dict): # si l'input est un dictionnaire
        f_value = - df_poids.loc["var_maint","poids"]*solution["var_maint"] - df_poids.loc["delta_maint","poids"]*solution["delta_maint"] 
    
    else :
        if isinstance(solution, str): # si l'input est le nom de l'individu
            df_indics = pd.DataFrame.from_csv("indicateurs/indicateurs"+solution[8:10].replace(".","")+".csv", header=None, sep=';', index_col=0)
        else:
            df_indics = solution # si l'input est déjà le dataframe des indicateurs de la solution
        # Calcul de l'indic aggrégé de maintenance : à maximiser  
        f = - df_poids.loc["var_maint","poids"]*df_indics.loc["var_maint"] - df_poids.loc["delta_maint","poids"]*df_indics.loc["delta_maint"]
        f_value = f.loc[1]
    return f_value


def Roulette_wheel_selection(df_classement, N, ope): 
    # input : dataframe classée de façon décroissante par fitness
    #       Si ope = True, sélection au sens de l'indicateur opérationnel aggrégé 
    #       et de celui de lissage si ope = False.
    # output : liste de N individus sélectionnés pour les opérateurs de mutations
    # et de cross-over. Cette selection est basee sur le fitness des individus d'une population
    df = df_classement
    if ope == True :
        f_sum = sum(df["fitness_ope"])
        df["proba"] = df["fitness_ope"]/f_sum
    else :
        f_sum = sum(df["fitness_lis"])
        df["proba"] = df["fitness_lis"]/f_sum        
    
    p_sum = sum(df["proba"])

    chosen_sol = []
    while len(chosen_sol) < N:
        rd_nb = np.random.random(1)[0]
        print(rd_nb)
        if len(list(df[df.proba >= rd_nb].index.values)) <= N :
            chosen_sol = chosen_sol + list(df[df.proba >= rd_nb].index.values)
        else:
            chosen_sol = chosen_sol + list(df[df.proba >= rd_nb].index.values)[0:N]
        print(chosen_sol)
        
    return chosen_sol