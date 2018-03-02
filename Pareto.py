# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 17:56:11 2018

@author: Melvin Foulgoc
"""
import os
from lecture import *
import csv
from objects import *
from constantes import *
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def programmePareto():
    
    dataPareto = pd.DataFrame()
    dataPareto = addGeneration(df_e, dataPareto)
    dataPareto = addGeneration(df_e, dataPareto)
    dataPareto = addGeneration(df_e, dataPareto)


    return dataPareto

def addGeneration(df, dataPareto):
    #On ajoute la génération aux données pour le tracé de Pareto
    # df : dataframe contenant l'ensembles des indicateurs, les rangs et les fitness
    # dataPareto : dataframe contenant les données nécessaires au tracé de Pareto final
    
    dataPareto = dataPareto.append(df.loc[:, ['fitness_lis', 'fitness_ope']])
    return dataPareto

def drawPareto(data):
    #Tracé du Pareto 
    # data : dataframe contenant l'ensembles des fitness
    
    plt.show()
    plt.figure(figsize=(15,8))
    plt.scatter(data[data.columns[0]].values,data[data.columns[1]].values)
    plt.title("Front de Pareto")
    plt.xlabel(data.columns[0])
    plt.ylabel(data.columns[1])
    
    for label, x, y in zip(data.index, data[data.columns[0]].values, data[data.columns[1]].values):
        plt.annotate(
            label,
            xy = (x, y), xytext = (15, 10),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    return data

def is_pareto_efficient(data):
    #Extraction de la liste des solutions pareto-optimales
    # data : dataframe contenant l'ensembles des fitness
    
    
    is_better = dict()
    is_better2 = []
    is_better3 = []
    
    for i in data.index: #Pour chaque plannings on liste des autres plannings strictement meilleurs 
        liste = []
        for j in data.index:
            if data['fitness_lis'][i] < data['fitness_lis'][j] and data['fitness_ope'][i] < data['fitness_ope'][j]:
                liste.append(j)
                
        
        is_better[i] = liste    
    
    for i in is_better.keys(): #Liste des numeros non dominés strictement sur les 2 critères
        if is_better[i] == []:
            is_better2.append(i)
        
    is_better3 = is_better2
       
    for i in is_better2: #On supprimes les dominés sur 1 critère parmi les précédents
        for j in is_better2:
            better = 0
            if (data['fitness_lis'][i] >= data['fitness_lis'][j] and data['fitness_ope'][i] > data['fitness_ope'][j] and j in is_better2) or (data['fitness_lis'][i] > data['fitness_lis'][j] and data['fitness_ope'][i] >= data['fitness_ope'][j] and j in is_better2):
                better = 1
            if better == 1:
                is_better3.remove(j)
        
    is_better4 = is_better3
    print(is_better3)
 
    for i in is_better3: #On supprimes les doublons
        for j in is_better3:
            better = 0
            if data['fitness_lis'][i] == data['fitness_lis'][j] and data['fitness_ope'][i] == data['fitness_ope'][j] and j in is_better3 and j != i:
                better = 1
            if better == 1:
                is_better4.remove(j)
    
    return is_better4


