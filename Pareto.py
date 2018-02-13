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
    plt.show()
    plt.figure(figsize=(10,4))
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
    
#    #Traitement par ACP
#    pca = PCA(n_components=3)
#    print(pca.fit(data))
#    pca.explained_variance_ratio_
#    
#    #Diagramme barre des variances agrégée
#    plt.bar(np.arange(len(pca.explained_variance_ratio_))+0.5, pca.explained_variance_ratio_)
#    plt.title("Variance expliquée")
#    
#    #Tracé de l'ACP
#    axis_list = [pca.components_.T]    
#    X_reduced = pca.transform(data)
#    plt.figure(figsize=(10,4))
#    plt.scatter(X_reduced[:, 0], X_reduced[:, 1])
#   
#    if axis_list is not None:
#        colors = ['orange']
#        for color, axis in zip(colors, axis_list):
#            x_axis, y_axis = axis[0],axis[1]
#            # Trick to get legend to work
#            #plt.plot(0.1 * x_axis, 0.1 * y_axis, linewidth=1, color=color)
#            plt.quiver(0, 0, x_axis, y_axis, zorder=5, width=0.005, scale=10,
#                           color=color)
#
#    for label, x, y in zip(data.index, X_reduced[:, 0], X_reduced[:, 1]):
#        plt.annotate(
#            label,
#            xy = (x, y), xytext = (-10, 10),
#            textcoords = 'offset points', ha = 'right', va = 'bottom',
#            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
#            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
#    
    return data

if __name__ == '__main__': dataPareto = programmePareto()
