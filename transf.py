# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 11:26:53 2018

@author: guigr
"""
import csv
import pandas as pd
import numpy as np
from objects import *

def transf_Mission2Numb(pathSolution):
    
#    #Lecture pour avoir le type de l'avion en fonction de son nom
#    
#    nomAvion = []
#    typeAvion =[]
#    
#    f = open('NomToType')
#    csv_f = csv.reader(f, delimiter = ';')
#    row1 = next(csv_f)
#    row2 = next(csv_f)
#    nomAvion = row2
#    del nomAvion[0]
#    row3 = next(csv_f)
#    typeAvion = row3
#    del typeAvion[0]

    
    #Lecture pour avoir le numéro associé au nom de mission
    
    nom = []
    numero =[]
    dicoTransformation = dict()
    
    f = open('Transformation')
    csv_f = csv.reader(f, delimiter = ';')
    row1 = next(csv_f)
    row2 = next(csv_f)
    nom = row2
    del nom[0]
    row3 = next(csv_f)
    numero = row3
    del numero[0]
    
    
    
    for i in range(0,len(nom)):
        dicoTransformation[nom[i]] = numero[i]
        
    dicoTransformation['-'] = 600
    
    nom.append('-')
    
    dicoTransformation[''] = 500
    
    #Transformation du csv en dataframe
    df = pd.read_csv(pathSolution, sep = ';')
    array = df.values
                            
    for column in range(1,len(array[1,:])):
        for row in range(0,len(array[:,1])):
            if(type(array[row,column]) == float):
                array[row,column] = 500
            else:
                for j in range(0,len(nom)):
                    if (array[row,column] == nom[j]):
                        array[row,column] = dicoTransformation[nom[j]]
                        
    df1 = pd.DataFrame(array)
                        
    return df1, dicoTransformation

def transf_NumbtoMission(df):
    
    #Lecture pour avoir le type de l'avion en fonction de son nom
    
#    nomAvion = []
#    typeAvion =[]
#    
#    f = open('NomToType')
#    csv_f = csv.reader(f, delimiter = ';')
#    row1 = next(csv_f)
#    row2 = next(csv_f)
#    nomAvion = row2
#    del nomAvion[0]
#    row3 = next(csv_f)
#    typeAvion = row3
#    del typeAvion[0]

    
    #Lecture pour avoir le numéro associé au nom de mission
    
    nom = []
    numero =[]
    dicoTransformation = dict()
    
    f = open('Transformation')
    csv_f = csv.reader(f, delimiter = ';')
    row1 = next(csv_f)
    row2 = next(csv_f)
    nom = row2
    del nom[0]
    row3 = next(csv_f)
    numero = row3
    del numero[0]
    
    
    
    for i in range(0,len(nom)):
        dicoTransformation[nom[i]] = numero[i]
        
    dicoTransformation['-'] = 600
    
    nom.append('-')
    
    #Transformation du csv en dataframe
    array = df.values
    
    for i in range(0,len(nom)):
        for m in nom:
            array[array == dicoTransformation[m]] = m
            array[array == 500] = float('nan')
        
    df1 = pd.DataFrame(array)
                        
    return df1
                    
            
    
    
    
    
    
    
    
    
    
        