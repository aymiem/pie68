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
    df_poids = pd.read_csv('poids_indicateurs.csv',sep=";",header=0,index_col=0)
    
    # somme pondérée des scores par indicateurs
    df_RWS["fitness_op"] = np.asarray(df_RWS["pot_perdu_rg"])*(df_poids.loc["pot_perdu","poids"]) \
            - np.asarray(df_RWS["min_pot_perdu_rg"])*(df_poids.loc["min_pot_perdu","poids"]) \
            + np.asarray(df_RWS["last_cravate_rg"])*(df_poids.loc["last_cravate","poids"]) 
    
    print(df_RWS)
    return df_RWS.sort_values(by=["fitness_op"], ascending=False)



def fitness_ope_indiv(solution):
    # evalue un score (ou fitness) de 3 indicateurs opérationnels aggrégés :
    # moyenne_heures_perdues, min_pot_perdu et last_cravate pour un individu 
    
    if isinstance(solution, str): # si l'input est le nom de l'individu
        df_indics = pd.DataFrame.from_csv("indicateurs"+solution[8:10]+".csv", header=None, sep=';', index_col=0)
    else:
        df_indics = solution # si l'input est déjà le dataframe des indicateurs de la solution
        
    # Calcul de l'indic aggrégé opérationnel : à minimiser  
    f_value = 0.5*df_indics.loc["pot_per"] - 0.3*df_indics.loc["min_pot_per"] + 0.2*1000*df_indics.loc["min_pot_per"]
    return f_value



def fitness_lissage(df_classement):
    # evalue un score (ou fitness) de 2 indicateurs liés à la maintenance et
    # aggrégés : maint_var, delta_maint, pour les individus d'une même génération
    
    df_RWS = df_classement
    df_poids = pd.read_csv('poids_indicateurs.csv',sep=";",header=0,index_col=0)
    df_RWS["fitness_lis"] = np.zeros(len(df_RWS))
    
    # somme pondérée des scores par indicateurs
    for nom_indic in ["maint_var", "delta_maint"]:
        df_RWS["fitness_lis"] = df_RWS["fitness_lis"] + np.asarray(df_RWS[nom_indic+"_rg"])*(df_poids.loc[nom_indic,"poids"])
    
    print(df_RWS)
    return df_RWS.sort_values(by=["fitness_lis"], ascending=False)


def fitness_lis_indiv(solution):
    # evalue un score (ou fitness) de 2 indicateurs liés à la maintenance et
    # aggrégés : maint_var, delta_maint, pour les individus d'une même génération

    if isinstance(solution, str): # si l'input est le nom de l'individu
        df_indics = pd.DataFrame.from_csv("indicateurs"+solution[8:10]+".csv", header=None, sep=';', index_col=0)
    else:
        df_indics = solution # si l'input est déjà le dataframe des indicateurs de la solution
        
    # Calcul de l'indic aggrégé de maintenance : à minimiser  
    f_value = 0.5*df_indics.loc["var_maint"] + 0.5*df_indics.loc["delta_maint"]
    return f_value   
    

def Roulette_wheel_selection(df_classement, N): 
    # input : dataframe classée de façon décroissante par fitness
    # output : liste de N individus sélectionnés pour les opérateurs de mutations
    # et de cross-over. Cette selection est basee sur le fitness des individus d'une population
    df = df_classement
    f_sum = sum(df["fitness"])
    df["proba"] = df["fitness"]/f_sum
    p_sum = sum(df["proba"])
    print(df)
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