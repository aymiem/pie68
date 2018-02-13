#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import shutil
import random
from transf import transf_NumbtoMission, transf_Mission2Numb

def crossover(input_dict, children_gen):
    
    # prend 3 plannings en entrée (meilleur, moyen et pire) dans un dictionnaire
    # ex : {'best': '0', 'worst': '12', 'median': '14'}
    
    # Meilleur avion en fonction de l'indicateur choisi et dictionnaire avec 
    # temps et mission/maint ou on a une difference entre les 3 plannings
    avion, dic_chg = calculs(input_dict)
    print("calculs ok")
    
    # Genere les deux plannings 
    dfs = generateur(avion,2,2,dic_chg,children_gen)
    
    return dfs
    
def calculs(sols):
    
    # Calcule l'avion qui a le plus d'influence pour l'indicateur choisi  
    # Input: Dictionnaire des 3 plannings (meilleur, moyen et pire) avec leur numero
    # Output: avion qui influence le plus l'indicateur choisi  avec un dictionnaire contenant
    #         le temps ou il y a une dif avec la la mission/maint correspondante 
    
    df = {}
    
    for key, num in sols.items() :
        
        print('analyse planning ' + key + num)
        
        df[num], dic_miss = transf_Mission2Numb('solution'+str(num)+'.csv')
        
    #Calcul du nb total d'avions
    total_rows = len(df[sols["best"]])
    
    # Dict avec les covariances entre avions (ex:cov[1] represente 
    # la covariance de l'avion 1 (D602) pour les 3 plannings)
    cor = {}
    
    #On prend la ligne i de chacun des 3 plannings, on les stack et on calcule la cov
    for i in range (0,total_rows):
        x = np.vstack([df[sols["best"]].iloc[i,1:],df[sols["median"]].iloc[i,1:],df[sols["worst"]].iloc[i,1:]])
        cor[i] = np.corrcoef(x.astype(float))
     
    #On calcule le minimum qui nous donnera l'avion qui a le plus d'impact
    #Deux methodes possibles: dif (moyenne de abs cor(moyen,meilleur) et abs 
    # cor(moyen,pire)) et dife (cor(meilleur,pire))). Commenter pour choisir.
    
    dif = {}
    #dife = {}
    for i in cor:
        dif[i] = (np.abs(cor[i].item(3))+np.abs(cor[i].item(7)))/2
        #dife[i] = np.abs(cor[i].item(6))
    
    #Index dans le df de l'avion qui a le plus d'influence sur l'indicateur
    val = min(dif, key=lambda i: dif[i])
    
    #Liste triée des correlations par ordre croissant (utilisée si pour 
    # le meilleur avion on a un dictionnaire vide)
    dif_sorted = sorted(dif.items(), key=lambda kv: kv[1], reverse=False)
    
    #Donne l'avion (reg. number) correspondant au minimum calculé
    avion = df[sols["best"]].iloc[val][0]

    #On concatenate les 3 lignes correspondant à l'avion choisi, chacune des 3 étant celle du meilleur, moyen et pire planning
    liste = []

    #Renommer les 3 lignes par best, median, worse
    for key, num in sols.items():
        df[num]=df[num].replace(df[num].iloc[val][0], key)
        liste.append(df[num].loc[val:val])
        
    #Transformation en dataframe de liste[]
    result = pd.concat(liste, ignore_index=True)
    
    #On regarde à quel pas de temps il y'a une difference pour cet avion pour les 3 plannings 
    # et on l'enregistre dans un dictionnaire dic_chg. key=temps et value=affectation
    
    dic_chg = {}
    for column in result.columns[1:]:
        
        if (result[column][0] != result[column][1] != result[column][2]):
            valeur= result[column][0]
            mission= list(dic_miss.keys())[list(dic_miss.values()).index(valeur)]
            dic_chg[column] = mission
            
    #Supprime les "-" et "NaN" du dictionnaire dic_chg                       
    for k,v in list(dic_chg.items()):
        if (v == '-') or (v == ''):
            del dic_chg[k]
    
    # Si pour le premier avion on obtient un dictionnaire vide, on regarde dans la liste triée,
    # dif_sorted, l'avion suivant et on recalcule tout jusqua'à obtenir un dictionnaire non vide
    
    av = 0
    while (len(dic_chg) == 0):
        
        print("step recherche with avion",avion)
        
        #Numéro d l'itération (=av-ième avion a prendre dans la liste triée)
        av = av + 1
        
        #Index de l'avion dans le dataframe (equivalent à val)
        avion_val = dif_sorted[av]
        
        #Nom de l'avion
        avion = df[sols["best"]].iloc[avion_val[0]]
        
        #A partir d'ici et jusqu'à la fin du while les fonctions ont déjà été expliquées
        
        liste = []
          
        for key, num in sols.items():
            df[num]=df[num].replace(avion.iloc[0], key)
            liste.append(df[num].loc[avion_val[0]:avion_val[0]])
        
        result = pd.concat(liste,ignore_index=True)
        
        for column in result.columns[1:]:
        
            if (result[column][0] != result[column][1] != result[column][2]):
                valeur= result[column][0]
                mission= list(dic_miss.keys())[list(dic_miss.values()).index(valeur)]
                dic_chg[column] = mission
        
        for k,v in list(dic_chg.items()):
            if (v == '-') or (v == ''):
                del dic_chg[k]
          
    if isinstance(avion,str):
        return (avion, dic_chg)
    else :
        return (avion.iloc[0], dic_chg)

def new_sitInit(plane,n,planing,dic,gen):
    
    # Creation des nouveaux sitInit.csv
    # Input: avion qui a le plus d'influence, numero d'affectations à fixer,numero du planing a creer,
    #       dictionnaire avec les affectations qui changent (dic_chg) et numero de la generation
    # Output: dataframe du la nouvelle sitInit avec les affectations fixées
    
    #Lecture du sitInit.csv 
    csv_file = csv.reader(open('sitInitD.csv', "r"), delimiter=";")
    index = 1
    
    #Boucle qui itere le long des lignes de la premiere colonne jusqu'a trouver l'avion (plane)
    #et calculer l'index de cet avion
    for row in csv_file:
        if plane == row[0]:
             break
        else : index += 1
    
    shutil.copy("sitInitD.csv", "sitInittemp.csv")
    df = pd.read_csv("sitInittemp.csv",sep=";",header=None)
    
    #Tire aléatoirement n affectations du dic_chg afin de les fixer dans la nouvelle sitInit
    for i in range(n):
        key=random.choice(list(dic))
        df.loc[index-1,int(key)]= int(key)
    
    #Le dataframe obtenu contient des chiffres au lieu du nom des missions donc on appelle la fonction
    #NumbtoMission afin de reconvertir en nom de missions.
    dataframe = transf_NumbtoMission(df)
    dataframe.to_csv("sitInit_"+str(gen) +"_"+ str(planing) + ".csv",sep=";",index=False,header=None)
    
    return dataframe
 
def generateur(plane,n_plan,n_fix,dic,gene):
    
    #Genere les sitInit 
    #Input: avion qui a le plus d'influence, numero de planings a creer, numero d'affectations à fixer,
    #       dictionnaire avec les affectations qui changent (dic_chg) et numero de la generation
    #Output: Dictionnaire de dataframes qui corrspondent aux SitInit
    
    dfs = []
    
    #Appelle n_plan fois la fonction new_sitInit pour créer n_plan SitInit
    for m in range(n_plan):
        dfs.append(new_sitInit(plane,n_fix,m,dic,gene))
    return dfs
