#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


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
        df[num] = df[num].replace(['NANCY_D$23','NDJAMENA_D$60','LUXEUIL_5F$23',"NIAMEY_D$50","ORANGE_C$23","DJIBOUTI_5F$23","MARSAN_5F$23","CHAMMAL_D$80","MARSAN_D$23","MARSAN_C$23","NIAMEY_C$50","ORANGE_B$23","V5","V10","V15","V20","V25","V30","-"],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]) 
        df[num] = df[num].fillna(0)
        #print(df[num])

    #Calcul du nb total d'avions
    total_rows = len(df[sel_gene_1[0]])
    #print(total_rows)
    #print("prueba")
    
    #Dict avec les covariances entre avions (ex:cov[1] represente la covariance de l'avion 1 (D602) pour les 3 plannings)
    cov = {}
    
    #On prend la ligne i de chacun des 3 plannings, on les stack et on calcule la cov
    for i in range (0,total_rows):
        x = np.vstack([df[sel_gene_1[0]].iloc[i,1:],df[sel_gene_1[1]].iloc[i,1:],df[sel_gene_1[2]].iloc[i,1:]])
        #print(x)
        cov[i] = np.cov(x.astype(float))
        print(cov[i])
                
    #for i in dict:
       # liste = dict[i]
       # print(liste)
        
    #for i in dict:
        #for items in dict[i]:
            #print(i, items)
            #print(random.sample(dict[i], 2))
            
    #for i in dict:
        #print(random.sample(dict[i], 2))
        
    #print(dict["2000_D"])
        
    
    #for avion in liste:
        
       # if avion.type
        
    #print(lst)
        
if __name__ == '__main__': indic, df = programme()