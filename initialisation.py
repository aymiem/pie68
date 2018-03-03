import os
from lecture import *
import csv
from objects import *
from constantes import *
import pandas as pd
import numpy as np
from main import programme
from ecriture import nom_fichier_sortie

def initialisation() :
    
    # création solution0 avec stratégie d'affectation "cravate"
    constantes.typechoix = 0
    programme(True, 0)

    # creation des solution 10 a 19 de la generation 1
    constantes.typechoix = 1 # stratégie d'affectation en mission aléatoire
    
    for i in range(10):
        print("Initialisation step :", i)
        
        nom_fichier_sortie(1, i)

        indic, d = programme(True, 0)
    return d