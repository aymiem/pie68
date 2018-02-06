#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import shutil
import random
from classement_population import choix_indiv_rg
from classement_population import rankings


def crossover(parents_gen, ope):
    
    #ope: True/False

    #prend 3 plannings en entrée (meilleur, moyen et pire)
    
    indicateurs = ["fitness_ope","fitness_lis"] 
    
    if ope == True :
        indic = indicateurs[0]
        
    else:
        indic = indicateurs[1]
        
    gen=parents_gen
    df_c = rankings(gen)
    a_meilleur= choix_indiv_rg(df_c, gen, indic, 1)
    a_moyen= choix_indiv_rg(df_c, gen, indic, 0.5)
    a_pire = choix_indiv_rg(df_c, gen, indic, 0)
    sel_gene_1 = [a_meilleur,a_moyen,a_pire]

    #Meilleur avion en fonction de l'indicateur choisi et dictionnaire avec temps et mission/maint ou on a une difference entre les 3 plannings
    avion, dic_chg = calculs(sel_gene_1)
   
    #genere les deux plannings 
    generateur(avion,2,2,dic_chg,gen)
    
 #Calcule l'avion qui a le plus d'influence pour l'indicateur choisi   
def calculs(sel):
    df = {}

    for num in sel :
        
        print('analyse planning '  + num)
        
        df[num] = pd.read_csv('solution'+str(num)+'.csv', sep =";")
        #df[num] = transf_Mission2Numb(str(num))
        
        #Transformation des noms des missions et maint en numeros pour pouvoir calculer des covariances
        #Pas "automatique" pour l'instant, le sera avec ce qu'a fait Guillaume
        df[num] = df[num].replace(['NANCY_D','NDJAMENA_D','LUXEUIL_5F',"NIAMEY_D","ORANGE_C","DJIBOUTI_5F","MARSAN_5F","CHAMMAL_D","MARSAN_D","MARSAN_C","NIAMEY_C","ORANGE_B","V5","V10","V15","V20","V25","V30","-"],[1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019]) 
        df[num] = df[num].fillna(0)
        #print(df[num])
        
    #Calcul du nb total d'avions
    total_rows = len(df[sel[0]])
    #print(total_rows)
    #print("prueba")
    
    #Dict avec les covariances entre avions (ex:cov[1] represente la covariance de l'avion 1 (D602) pour les 3 plannings)
    cor = {}
    
    #On prend la ligne i de chacun des 3 plannings, on les stack et on calcule la cov
    for i in range (0,total_rows):
        x = np.vstack([df[sel[0]].iloc[i,1:],df[sel[1]].iloc[i,1:],df[sel[2]].iloc[i,1:]])
        #print(x)
        cor[i] = np.corrcoef(x.astype(float))
        #print(i)
        #print(cor[i])
    
    
    #On calcule le minimum qui nous donnera l'avion qui a le plus d'impact
    dif = {}
    dife = {}
    for i in cor:
        dif[i] = (np.abs(cor[i].item(3))+np.abs(cor[i].item(7)))/2
        dife[i] = np.abs(cor[i].item(6))
    
    #print(dif)
    #print(dife)
    
    val = min(dif, key=lambda i: dif[i])
    
    #Donne l'avion correspondant au minimum calculé
    avion = df[sel[0]].iloc[val][0]
    #val = min(dife, key=lambda i: dife[i])
    
    #On concatenate les 3 lignes correspondant à l'avion choisi, chacune des 3 étant celle du meilleur, moyen et pire planning
    liste = []
    values = ["meilleur", "moyen", "pire"]
    dictionaire = dict(zip(sel, values))
    for num in sel:
        df[num]=df[num].replace(df[num].iloc[val][0],df[num].iloc[val][0] + dictionaire[num])
        liste.append(df[num].loc[val:val])
        
    #print(liste)  
    
    result = pd.concat(liste,ignore_index=True)
    
    #print(result)
    
    #Dictonnaire missions/numero
    missions = ["NaN",'NANCY_D','NDJAMENA_D','LUXEUIL_5F',"NIAMEY_D","ORANGE_C","DJIBOUTI_5F","MARSAN_5F","CHAMMAL_D","MARSAN_D","MARSAN_C","NIAMEY_C$50","ORANGE_B$23","V5","V10","V15","V20","V25","V30","-"]
    numero = [0,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019]
    dic_miss = dict(zip(missions, numero))
    
    #On regarde à quel pas de temps il y'a une difference pour cet avion pour les 3 plannings
    dic_chg = {}
    for column in result.columns[1:]:
        
        if (result[column][0] != result[column][1] != result[column][2]):
            valeur= result[column][0]
            mission= list(dic_miss.keys())[list(dic_miss.values()).index(valeur)]
            dic_chg[column] = mission
            #print(valeur)
      
    #Supprime ls - et NaN du dictionnaire, necessaire par la suite                         
    for k,v in list(dic_chg.items()):
        if (v == '-') or (v == 'NaN'):
           del dic_chg[k]
           
    return (avion, dic_chg)

#Creation des nouveaux sitInit.cscv
def new_sitInit(plane,n,planing,dic,gen):
    #read csv, and split on "," the line
    csv_file = csv.reader(open('sitInit.csv', "r"), delimiter=";")
    index = 1
    #loop through csv list
    for row in csv_file:
        #if current rows 2nd value is equal to input, print that row
        if plane == row[0]:
             #print(row)
             #print(index)
             break
        else : index += 1
    
    shutil.copy("sitInit.csv", "sitInittemp.csv")
    df = pd.read_csv("sitInittemp.csv",sep=";",header=None)

    for i in range(n):
        key=random.choice(list(dic))
        df.loc[index-1,int(key)]= dic[key]
    #print(df)
    #df.set_value(index-1, 34,)
    
    df.to_csv("sitInit_"+str(gen) +"_"+ str(planing) + ".csv",sep=";",index=False,header=None)
    
    return df
 
#Genere les sitInit en fonction des param choisis
def generateur(plane,n_plan,n_fix,dic,gene):
    dfs = []
    for m in range(n_plan):
        dfs.append(new_sitInit(plane,n_fix,m,dic,gene))
    return dfs
