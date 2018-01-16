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

def programme():
    
    gen = input("Donner le numero de la generation (1 pour population initiale):")
    
    return classement(gen)


def classement(generation):
    print('Lancement du programme ')

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
    
    print(df_indic)
    
    for ind in df_indic.columns:
        if (ind == "max_maint"):
            # Rg 1 si maintenance max <= 18
            df_indic[ind+"_rg"] = df_indic[ind]/18 + (df_indic[ind]/18 - 1)*10
        else:
            if (ind == "var_maint") or (ind == "pot_perdu" ):
                df_indic = df_indic.sort_values(by=[ind])
            else:
                df_indic = df_indic.sort_values(by=[ind], ascending=False)
            
            df_indic[ind+"_rg"] = list(range(1,len(df_indic[ind])+1))    
    
    print(df_indic)
        
    return df_indic
    
if __name__ == '__main__': df = programme()