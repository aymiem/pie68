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
    print('Lancement du programme ')

    generation = input('Donner le numero de la generation (1 pour population initiale):')
    print(type(generation))
    listeFiles = [] 
    # liste des fichiers de type "indicateursXX.csv" de la génération étudiée à lire
    for file in os.listdir(os.getcwd()): # Pour les fichiers du dossier courant
        if file.endswith(".csv") and file.startswith("indicateurs"+generation):
            listeFiles.append(file)
            print(listeFiles)
            
    if generation == "1":
        listeFiles.append("indicateurs0.csv")
        print(listeFiles)
    
    
    dfs = []
    #print(pd.read_csv("indicateurs10.csv",sep=";",header=None))
    for nom_fichier in listeFiles:
        df_loc = pd.read_csv(nom_fichier,sep=";",header=None,index_col=0)
        df_loc.loc[2]=[nom_fichier,0]
        df_loc=df_loc.transpose()
        print(df_loc)
        dfs.append(df_loc)
    
    df_indic = pd.concat(dfs,ignore_index=True)
    
    print(df_indic)
        
        
#    # Lecture des données de chaque categorie dans le fichier csv
#    listeInd=indexCategories(path)
#    lecture_l_p = lectureCategorie(path, listeInd, "parametres")
#    lecture_l_a = lectureCategorie(path, listeInd, "avion")
#    lecture_l_m = lectureCategorie(path, listeInd, "mission")
#    lecture_l_mt = lectureCategorie(path, listeInd, "maintenance")
    
    
    
    
if __name__ == '__main__': indic, df = programme()