# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 11:26:53 2018

@author: guigr
"""
import csv
import pandas as pd
import numpy as np
from objects import *
from constantes import *
from main import lectureEntrees

def dico_transf_init():
    
    x=constantes.path # Nom du fichier contenant la liste des autres CSV
    d=lectureEntrees(x)# Lecture des fichiers d'entrées

    dicoAssociation= dict()
    dicoDollar = dict()
    nbrMission = 1101
    
    for i in d["listeMission"]:
        nomMission = i.nom
        dicoAssociation[nomMission] = nbrMission
        nbrMission += 1
        
    nbrMaintenance = 1001        
    for i in d["listeMaintenance"]:   
        nomMaintenance = i.nom
        dicoAssociation[nomMaintenance] = nbrMaintenance
        nbrMaintenance += 1
        
    for i in d["listeMission"]:
        nomMission = ''.join([i.nom, '$', str(int(i.pu))])
        dicoDollar[i.nom] = nomMission
        nbrMission += 1
    
#    dM = pd.DataFrame(list(dicoMatricule.items()), columns=['nomAvion', 'typeAvion'])
    dA = pd.DataFrame(list(dicoAssociation.items()), columns=['nom', 'numero'])
    dM = pd.DataFrame(list(dicoDollar.items()), columns=['nom', 'nomDollar'])

    
#    dM.T.to_csv("NomToType", sep=';')
    dA.T.to_csv("Transformation.csv", sep=';')
    dM.T.to_csv("MissionDollar.csv", sep=';')



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
    
    f = open('Transformation.csv')
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
    
    f = open('Transformation.csv')
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
                    
            
def transf_Mission2MissionDollar(pathSolution):
    
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
    nomDollar =[]
    dicoTransformation = dict()
    
    f = open('MissionDollar.csv')
    csv_f = csv.reader(f, delimiter = ';')
    row1 = next(csv_f)
    row2 = next(csv_f)
    nom = row2
    del nom[0]
    row3 = next(csv_f)
    nomDollar = row3
    del nomDollar[0]
    
    
    
    for i in range(0,len(nom)):
        dicoTransformation[nom[i]] = nomDollar[i]
        
    dicoTransformation['-'] = ''
    
    nom.append('-')
    
    dicoTransformation[''] = ''
    
    #Transformation du csv en dataframe
    df = pd.read_csv(pathSolution, sep = ';')
    array = df.values
                            
    for column in range(1,len(array[1,:])):
        for row in range(0,len(array[:,1])):
            for j in range(0,len(nom)):
                if (array[row,column] == nom[j]):
                    array[row,column] = dicoTransformation[nom[j]]
                        
    df1 = pd.DataFrame(array)
                        
    df1.to_csv("solution_genetique.csv",sep=";",index=False,header=None)
    
    
    
    
    
    
    
    
        