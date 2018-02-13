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
from selection_operator import fitness_operationnel, fitness_lissage

# Module permettant de classer les individus d'une même génération 
    
def classement_population():
    # Classement visuel par front de Pareto
    dataPareto = pd.DataFrame()
    gen = '1'
    df_c = rankings(gen)  
    dataPareto = addGeneration(df_c, dataPareto)
    drawPareto(dataPareto) 
    
    return dataPareto


def rankings(generation):
    # Fonction qui créé la matrice des scores des indicateurs pour toute une génération
    #       et calcule les fitness lissage et opérationnel
    # Input : numero de la generation à classer
    # Output : dataframe avec les solutions/individus en index et donnant les scores 
    #          des indicateurs et les scores des fitness (indics agrégés)

    listeFiles = [] 
    # liste des fichiers de type "indicateursXX.csv" de la génération étudiée à lire
    for file in os.listdir(os.getcwd()): # Pour les fichiers du dossier courant
        if file.endswith(".csv") and file.startswith("indicateurs"+generation):
            listeFiles.append(file)
            
    if generation == "1":
        listeFiles.append("indicateurs0.csv")
    # récupération des dataframes conservées dans les fichiers indicateursXX.csv
    dfs = []
    for nom_fichier in listeFiles:
        df_loc = pd.read_csv(nom_fichier,sep=";",header=None,index_col=0)
        df_loc.loc["solution"]=[nom_fichier[11:13].replace(".","")]
        df_loc=df_loc.transpose()
        dfs.append(df_loc)
    # création dataframe des indicateurs de tous les individus de la génération
    df_indic = pd.concat(dfs,ignore_index=True)
    df_indic = df_indic.set_index('solution')
       
    # Attribution d'une note entre 0 et 1 de chaque individu pour chaque indicateur
    # par normalisation : xj' = (xj − minj)/(maxj − minj))
    #for ind in df_indic.columns:
    #    
    #    if (ind == "max_maint"):
    #        # Rg 1 si maintenance max > 18
    #        df_indic[ind+"_rg"] = df_indic[ind]/18 - (df_indic[ind]/18 - 1)
    #    else:
    #        if min(df_indic[ind]) != max(df_indic[ind]) :
    #            #Objectifs à minimiser
    #            if (ind == "var_maint") or (ind == "moy_pot_perdu" ) or (ind == "delta_nbmaint") :
    #                #df_indic = df_indic.sort_values(by=[ind])
    #                df_indic[ind+"_rg"] = 1 - (df_indic[ind]-min(df_indic[ind]))/(max(df_indic[ind])-min(df_indic[ind]))
    #            #Objectifs à maximiser
    #            else:
    #                #df_indic = df_indic.sort_values(by=[ind], ascending=False)
    #                df_indic[ind+"_rg"] = (df_indic[ind]-min(df_indic[ind]))/(max(df_indic[ind])-min(df_indic[ind]))            
    #        else : # Si indic constant pour toute solution, non pris en compte dans le calcul du fitness
    #            if (max(df_indic[ind]) != 0):
    #                df_indic[ind+"_rg"] = 1 - df_indic[ind]/max(df_indic[ind])
    #            else:
    #                df_indic[ind+"_rg"] = 0    
    
    # Calcul et ajout des colonnes des indics agrégés "fitness_ope" et "fitness_lis"
    df_indic = fitness_operationnel(df_indic)
    df_indic = fitness_lissage(df_indic)
    print(df_indic.iloc[:,-2:])
    
    return df_indic



def choix_indiv_rg(df_indic, generation, nom_indic, niveau_sol):
    # renvoit une solution ayant un niveau choisi pour un indicateur donné
    
    # inputs : df_indic, la dataframe des indicateurs pour les individus d'une génération après évaluation des rangs
    #         generation, le numero de la generation etudiee
    #         nom_indic, le nom de l'indicateur agrégé sur lequel on évalue les individus
    #         niveau_sol, le rang de l'individu cherché vis à vis de l'indicateur choisi
    # Si niveau_sol = 1, la fonction renvoit la meilleure solution pour l'indicateur choisi
    # Si niveau_sol = 0, elle renvoit la pire solution et sinon elle renvoit une solution intermédiaire

     # Remarque : les indicateurs agrégés sont construits de sorte qu'il faut les maximiser
     #          La meilleure solution est donc la première avec un tri tq ascending = False
    if (niveau_sol == 0) :
        num_sol = list(df_indic.sort_values(by=[nom_indic]).index.values)[0]
    elif (niveau_sol == 1) :
        num_sol = list(df_indic.sort_values(by=[nom_indic],ascending=False).index.values)[0]
    else :
        num_sol = list(df_indic.sort_values(by=[nom_indic],ascending=False).index.values)[int(len(df_indic)/2)]
    print("solution retenue pour niveau", niveau_sol, "et indic"+ nom_indic + ": " + num_sol)
    
    return num_sol
