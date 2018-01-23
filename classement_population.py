# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 14:37:27 2018
@author: aymeline
"""
import os
from lecture import *
import csv
from objects import *
from constantes import *
import pandas as pd
import numpy as np

def programme():
    print('Lancement du programme ') 
    
    gen = input("Donner le numero de la generation (1 pour population initiale):")
    df_c = classement(gen)
    df_e = evaluation(df_c)
    
    return Roulette_wheel_selection(df_e,3)


def classement(generation):

    listeFiles = [] 
    # liste des fichiers de type "indicateursXX.csv" de la génération étudiée à lire
    for file in os.listdir(os.getcwd()): # Pour les fichiers du dossier courant
        if file.endswith(".csv") and file.startswith("indicateurs"+generation):
            listeFiles.append(file)
            
    if generation == "1":
        listeFiles.append("indicateurs0.csv")
    
    print(listeFiles)
    
    dfs = []
    for nom_fichier in listeFiles:
        df_loc = pd.read_csv(nom_fichier,sep=";",header=None,index_col=0)
        df_loc.loc["solution"]=[nom_fichier[11:13].replace(".","")]
        df_loc=df_loc.transpose()
        dfs.append(df_loc)
        
    df_indic = pd.concat(dfs,ignore_index=True)
    df_indic = df_indic.set_index('solution')
    
    
    # Attribution d'une note entre 0 et 1 de chaque individu pour chaque indicateur
    # par normalisation : xj' = (xj − minj)/(maxj − minj))
    for ind in df_indic.columns:
        
        if (ind == "max_maint"):
            # Rg 1 si maintenance max > 18
            df_indic[ind+"_rg"] = df_indic[ind]/18 - (df_indic[ind]/18 - 1)
        else:
            if min(df_indic[ind]) != max(df_indic[ind]) :
                if (ind == "var_maint") or (ind == "pot_perdu" ) :
                    #df_indic = df_indic.sort_values(by=[ind])
                    df_indic[ind+"_rg"] = 1 - (df_indic[ind]-min(df_indic[ind]))/(max(df_indic[ind])-min(df_indic[ind]))
                else:
                    #df_indic = df_indic.sort_values(by=[ind], ascending=False)
                    df_indic[ind+"_rg"] = (df_indic[ind]-min(df_indic[ind]))/(max(df_indic[ind])-min(df_indic[ind]))
                #df_indic[ind+"_rg"] = list(range(1,len(df_indic[ind])+1)) 
            
            else : # Si indic constant pour toute solution, non pris en compte dans le calcul du fitness
                df_indic[ind+"_rg"] = 1 - df_indic[ind]/max(df_indic[ind])
             
        
    print(df_indic)
        
    return df_indic

def evaluation(df_classement):
    # evalue la fonction fitness
    # combinaison linéaire des rangs par indicateurs
    df_RWS = df_classement
    # on récupère ici les poids des indicateurs
    df_poids = pd.read_csv('poids_indicateurs.csv',sep=";",header=0,index_col=0)

    df_RWS["fitness"] = np.zeros(len(df_RWS))

    for nom_indic in list(df_poids.index):
        df_RWS["fitness"] = df_RWS["fitness"] + np.asarray(df_RWS[nom_indic+"_rg"])*(df_poids.loc[nom_indic,"poids"])
        print(df_RWS)
    return df_RWS.sort_values(by=["fitness"], ascending=False)

def Roulette_wheel_selection(df_classement, N): 
    # N est le nombre de membres choisis pour créer la génération suivante 
    # selection basee sur le fitness d'une population
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
    
if __name__ == '__main__': df_c = programme()