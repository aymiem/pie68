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


def programme():
    print('Lancement du programme ') 
    
    data = df_c.loc[:, ['min_pot_hor_rg', 'var_maint_rg', 'pot_perdu_rg']]
    data[1].name
    
    pca = PCA(n_components=3)
    print(pca.fit(data))
    pca.explained_variance_ratio_
    
    

    plt.bar(np.arange(len(pca.explained_variance_ratio_))+0.5, pca.explained_variance_ratio_)
    plt.title("Variance expliquée")
    
    axis_list = [pca.components_.T]    
    
    X_reduced = pca.transform(data)
    plt.figure(figsize=(10,4))
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1])
   
    if axis_list is not None:
        
        colors = ['orange','red','blue']
        
        for color, axis in zip(colors, axis_list):
            
            x_axis, y_axis = axis[0],axis[1]
            # Trick to get legend to work
            #plt.plot(0.1 * x_axis, 0.1 * y_axis, linewidth=1, color=color)
            plt.quiver(0, 0, x_axis, y_axis, zorder=5, width=0.005, scale=10,
                           color=color)

    for label, x, y in zip(data.index, X_reduced[:, 0], X_reduced[:, 1]):
        plt.annotate(
            label,
            xy = (x, y), xytext = (-10, 10),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    
    plt.figure(figsize=(10,4))
    plt.scatter(X_reduced[:, 1], X_reduced[:, 2])
   
    if axis_list is not None:
        
        colors = ['orange','red','blue']
        
        for color, axis in zip(colors, axis_list):
            
            x_axis, y_axis = axis[1],axis[2]
            # Trick to get legend to work
            #plt.plot(0.1 * x_axis, 0.1 * y_axis, linewidth=1, color=color)
            plt.quiver(0, 0, x_axis, y_axis, zorder=5, width=0.005, scale=10,
                           color=color)

    for label, x, y in zip(data.index, X_reduced[:, 1], X_reduced[:, 2]):
        plt.annotate(
            label,
            xy = (x, y), xytext = (-10, 10),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    
    
    return X_reduced

if __name__ == '__main__': Pareto = programme()
