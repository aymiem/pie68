#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import shutil
import random
from constantes import paths
from transf import transf_NumbtoMission, transf_Mission2Numb


def crossover(input_dict, children_gen):
    
    # prend 3 plannings en entrée (meilleur, moyen et pire) dans un dictionnaire
    # ex : {'best': '0', 'worst': '12', 'median': '14'}
    
    # Meilleur avion en fonction de l'indicateur choisi et dictionnaire avec temps et mission/maint ou on a une difference entre les 3 plannings
    avion, dic_chg = calculs(input_dict)
    print("calculs ok")
    #genere les deux plannings 
    dfs = generateur(avion,2,2,dic_chg,children_gen)
    
    return dfs
    
 #Calcule l'avion qui a le plus d'influence pour l'indicateur choisi   
def calculs(sols):
    df = {}
    
    for key, num in sols.items() :
        
        print('analyse planning ' + key + num)
        
        df[num], dic_miss = transf_Mission2Numb(paths.solutions_path +'solution'+str(num)+'.csv')
        
        #Transformation des noms des missions et maint en numeros pour pouvoir calculer des covariances
        #Pas "automatique" pour l'instant, le sera avec ce qu'a fait Guillaume
        #df[num] = df[num].replace(['NANCY_D','NDJAMENA_D','LUXEUIL_5F',"NIAMEY_D","ORANGE_C","DJIBOUTI_5F","MARSAN_5F","CHAMMAL_D","MARSAN_D","MARSAN_C","NIAMEY_C","ORANGE_B","V5","V10","V15","V20","V25","V30","-"],[1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019]) 
        #df[num] = df[num].replace(['NANCY_D','NDJAMENA_D',"NIAMEY_D","CHAMMAL_D","MARSAN_D","V5","V10","V15","V20","V25","V30","-"],[1001,1002,1004,1008,1009,1013,1014,1015,1016,1017,1018,1019]) 

        #df[num] = df[num].fillna(0)
        #print(df[num])
    #print(df , dic_miss)
    #Calcul du nb total d'avions
    total_rows = len(df[sols["best"]])
    #print(total_rows)
    #print("prueba")
    
    #Dict avec les covariances entre avions (ex:cov[1] represente la covariance de l'avion 1 (D602) pour les 3 plannings)
    cor = {}
    
    #On prend la ligne i de chacun des 3 plannings, on les stack et on calcule la cov
    for i in range (0,total_rows):
        x = np.vstack([df[sols["best"]].iloc[i,1:],df[sols["median"]].iloc[i,1:],df[sols["worst"]].iloc[i,1:]])
        cor[i] = np.corrcoef(x.astype(float))
    
    
    #On calcule le minimum qui nous donnera l'avion qui a le plus d'impact
    dif = {}
    #dife = {}
    for i in cor:
        dif[i] = (np.abs(cor[i].item(3))+np.abs(cor[i].item(7)))/2
        #dife[i] = np.abs(cor[i].item(6))
    
    #print(dif)
    #print(dife)
    
    dif_sorted = sorted(dif.items(), key=lambda kv: kv[1], reverse=False)
    
    val = min(dif, key=lambda i: dif[i])
    
    #Donne l'avion correspondant au minimum calculé
    avion = df[sols["best"]].iloc[val][0]
    #val = min(dife, key=lambda i: dife[i])
    
    #On concatenate les 3 lignes correspondant à l'avion choisi, chacune des 3 étant celle du meilleur, moyen et pire planning
    liste = []
    # values = ["meilleur", "moyen", "pire"]
    # dictionaire = dict(zip(sel, values))
    for key, num in sols.items():
        df[num]=df[num].replace(df[num].iloc[val][0], key)
        liste.append(df[num].loc[val:val])
        
    #print(liste)  
    
    result = pd.concat(liste, ignore_index=True)
    
    #Dictonnaire missions/numero
    #missions = ["NaN",'NANCY_D','NDJAMENA_D','LUXEUIL_5F',"NIAMEY_D","ORANGE_C","DJIBOUTI_5F","MARSAN_5F","CHAMMAL_D","MARSAN_D","MARSAN_C","NIAMEY_C$50","ORANGE_B$23","V5","V10","V15","V20","V25","V30","-"]
    #numero = [0,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019]
    #dic_miss = dict(zip(missions, numero))
    
    #On regarde à quel pas de temps il y'a une difference pour cet avion pour les 3 plannings
    dic_chg = {}
    for column in result.columns[1:]:
        
        if (result[column][0] != result[column][1] != result[column][2]):
            valeur= result[column][0]
            mission= list(dic_miss.keys())[list(dic_miss.values()).index(valeur)]
            dic_chg[column] = mission
       
    av = 0
    while (len(dic_chg) == 0):
        print("step recherche with avion",avion)
        av = av + 1
        avion_val = dif_sorted[av]
        avion = df[sols["best"]].iloc[avion_val[0]]
        
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
        
        #Supprime ls - et NaN du dictionnaire, necessaire par la suite                         
        for k,v in list(dic_chg.items()):
            if (v == '-') or (v == ''):
                del dic_chg[k]
    
        
    if isinstance(avion,str):
        return (avion, dic_chg)
    else :
        return (avion.iloc[0], dic_chg)

#Creation des nouveaux sitInit.cscv
def new_sitInit(plane,n,planing,dic,gen):
    #read csv, and split on "," the line
    path_to_file = 'sitInit.csv'
    csv_file = csv.reader(open(path_to_file, "r"), delimiter=";")
    index = 1
    #loop through csv list
    for row in csv_file:
        #if current rows 2nd value is equal to input, print that row
        if plane == row[0]:
            break
        else : 
            index += 1
    
    shutil.copy(path_to_file, "sitInittemp.csv")
    df = pd.read_csv("sitInittemp.csv",sep=";",header=None)
    
    for i in range(n):
        key=random.choice(list(dic))
        df.loc[index-1,int(key)]= int(key)
    
    dataframe = transf_NumbtoMission(df)
    
    dataframe.to_csv(paths.sitInits_path +"sitInit_"+str(gen) +"_"+ str(planing) + ".csv",sep=";",index=False,header=None)
    
    return dataframe
 
#Genere les sitInit en fonction des param choisis
def generateur(plane,n_plan,n_fix,dic,gene):
    dfs = []
    for m in range(n_plan):
        dfs.append(new_sitInit(plane,n_fix,m,dic,gene))
    return dfs
