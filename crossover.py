#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
#import random

def programme():
    
    print('Lancement du programme ')
     
    #prend 3 plannings en entrée (meilleur, moyen et pire)
    sel_gene_1 = [10,11,12]
    
    #Dictionnaire de data frame des plannings 
    df = {}

    for num in sel_gene_1 :
        
        #print(num)
        
        df[num] = pd.read_csv('solution' + str(num) + '.csv', sep =";")
        
        #Transformation des noms des missions et maint en numeros pour pouvoir calculer des covariances
        df[num] = df[num].replace(['NANCY_D$23','NDJAMENA_D$60','LUXEUIL_5F$23',"NIAMEY_D$50","ORANGE_C$23","DJIBOUTI_5F$23","MARSAN_5F$23","CHAMMAL_D$80","MARSAN_D$23","MARSAN_C$23","NIAMEY_C$50","ORANGE_B$23","V5","V10","V15","V20","V25","V30","-"],[1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019]) 
        df[num] = df[num].fillna(0)
        print(df[num])
        
        

    #Calcul du nb total d'avions
    total_rows = len(df[sel_gene_1[0]])
    #print(total_rows)
    #print("prueba")
    
    #Dict avec les covariances entre avions (ex:cov[1] represente la covariance de l'avion 1 (D602) pour les 3 plannings)
    cor = {}
    
    #On prend la ligne i de chacun des 3 plannings, on les stack et on calcule la cov
    for i in range (0,total_rows):
        x = np.vstack([df[sel_gene_1[0]].iloc[i,1:],df[sel_gene_1[1]].iloc[i,1:],df[sel_gene_1[2]].iloc[i,1:]])
        #print(x)
        cor[i] = np.corrcoef(x.astype(float))
        #print(i)
        #print(cor[i])
    
    dif = {}
    dife = {}
    for i in cor:
        dif[i] = (np.abs(cor[i].item(3))+np.abs(cor[i].item(7)))/2
        dife[i] = np.abs(cor[i].item(6))
    
    #print(dif)
    #print(dife)
    
    val = min(dif, key=lambda i: dif[i])
    
    #val = min(dife, key=lambda i: dife[i])
    
    liste = []
    values = ["meilleur", "moyen", "pire"]
    dictionaire = dict(zip(sel_gene_1, values))
    for num in sel_gene_1:
        df[num]=df[num].replace(df[num].iloc[val][0],df[num].iloc[val][0] + dictionaire[num])
        liste.append(df[num].loc[val:val])
        
    #print(liste)  
    
    result = pd.concat(liste,ignore_index=True)

    print(result)
  
    for column in result.columns[1:]:
        
        if (result[column][0] != result[column][1] != result[column][2]):
            print(result[column])
        
    #dict = {} 
    #for i in dict:
        #liste = dict[i]
        #print(liste)
        
   # for i in dict:
        #for items in dict[i]:
           # print(i, items)
            #print(random.sample(dict[i], 2))
            
    #for i in dict:
       # print(random.sample(dict[i], 2))
        
    #print(dict["2000_D"])
        
    
    #for avion in liste:
        
       # if avion.type
        
    #print(lst)
        
if __name__ == '__main__': indic, df = programme()