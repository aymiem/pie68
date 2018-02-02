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
from Pareto import addGeneration, drawPareto
import pandas as pd
import numpy as np
from selection_operator import evaluation_fitness, Roulette_wheel_selection

# Module permettant de classer les individus d'une même génération 
    
def classement_population():
    # Classement visuel par front de Pareto
    dataPareto = pd.DataFrame()
    gen = '1'
    df_c = classement_population_tab(gen)
    df_e = evaluation_fitness(df_c)   
    dataPareto = addGeneration(df_e, dataPareto)
    drawPareto(dataPareto) 
    
    return dataPareto

def classement_population_tab():
    
    gen = input("Donner le numero de la generation (1 pour population initiale):")
    df_c = rankings(gen)
    df_e = evaluation_fitness(df_c)
    return df_e


def rankings(generation):
    # input : numero de la generation pour laquelle on doit attribuer un rg par indicateur
    # output : dataframe avec les solutions/individus en index et donnant les valeurs 
    #          des indicateurs et les un score/rg par indicateur

    listeFiles = [] 
    # liste des fichiers de type "indicateursXX.csv" de la génération étudiée à lire
    for file in os.listdir(os.getcwd()): # Pour les fichiers du dossier courant
        if file.endswith(".csv") and file.startswith("indicateurs"+generation):
            listeFiles.append(file)
            
    if generation == "1":
        listeFiles.append("indicateurs0.csv")
    
    #print(listeFiles)
    
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
             
    #print(df_indic)
    return df_indic

    #for nom_indic in list(df_poids.index):
    #    df_RWS["fitness"] = df_RWS["fitness"] + np.asarray(df_RWS[nom_indic+"_rg"])*(df_poids.loc[nom_indic,"poids"])
    #    #print(df_RWS)
    #return df_RWS.sort_values(by=["fitness"], ascending=False)

def choix_indiv_rg(df_indic, generation, nom_indic, niveau_sol):
    # renvoit une solution ayant un niveau choisi pour un indicateur donné
    
    # inputs : df_indic, la dataframe des indicateurs pour les individus d'une génération après évaluation des rangs
    #         generation, le numero de la generation etudiee
    #         nom_indic, le nom de l'indicateur sur lequel on évalue les individus
    #         niveau_sol, le rang de l'individu cherché vis à vis de l'indicateur choisi
    # Si niveau_sol = 1, la fonction renvoit la meilleure solution pour l'indicateur choisi
    # Si niveau_sol = 0, elle renvoit la pire solution et sinon elle renvoit une solution intermédiaire

    ind_rg = nom_indic + "_rg"
    if (niveau_sol == 0) :
        num_sol = list(df_indic.sort_values(by=[ind_rg]).index.values)[0]
    elif (niveau_sol == 1) :
        num_sol = list(df_indic.sort_values(by=[ind_rg],ascending=False).index.values)[0]
    else :
        num_sol = list(df_indic.sort_values(by=[ind_rg],ascending=False).index.values)[int(len(df_indic)/2)]
    print(num_sol)
    print("solution" + num_sol + ".csv")
    
    return num_sol
