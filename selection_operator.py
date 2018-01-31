import os
from lecture import *
import csv
from objects import *
from constantes import *
import pandas as pd
import numpy as np

def evaluation_fitness(df_classement):
    # evalue la fonction fitness, combinaison linéaire des rangs 
    # par indicateurs pour les individus d'une génération
    df_RWS = df_classement
    # on récupère ici les poids des indicateurs
    df_poids = pd.read_csv('poids_indicateurs.csv',sep=";",header=0,index_col=0)

    df_RWS["fitness"] = np.zeros(len(df_RWS))
    
    # somme pondérée des scores par indicateurs
    for nom_indic in list(df_poids.index):
        df_RWS["fitness"] = df_RWS["fitness"] + np.asarray(df_RWS[nom_indic+"_rg"])*(df_poids.loc[nom_indic,"poids"])
    
    print(df_RWS)
    return df_RWS.sort_values(by=["fitness"], ascending=False)


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