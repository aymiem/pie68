import os
from lecture import *
import csv
from objects import *
from constantes import *
import pandas as pd
import numpy as np
from main import programme

def initialisation() :
    
    # création solution0 avec stratégie d'affectation "cravate"
    constantes.typechoix = 0
    programme()

    # creation des solution 10 a 19 de la generation 1
    constantes.typechoix = 1 # stratégie d'affectation en mission aléatoire
    
    for i in range(10):
        print(i)
        
        new_rows = [] 
        changes = {   # un dictionnaire du changement a effectuer 
<<<<<<< HEAD
                'solution0' : 'solution1'+str(i)}
=======
                'solution0' : 'solution1'+str(i)
                }
>>>>>>> 8db762da01049691f83d6ede252763b8df6e5ddf

        with open('donnees_lecture.csv', 'r') as f:
            reader = csv.reader(f) 
            for row in reader:     # pour chaque ligne
                new_row = row      # on copie la ligne
                for key, value in changes.items(): 
                    # et on modifie le nom du fichier enregistré
                    new_row = [ x.replace(key, value) for x in new_row ] 
                new_rows.append(new_row) # ajoute les nouvelles lignes

<<<<<<< HEAD
        with open('donnees_lecture.csv', 'w') as f:
=======
        with open('donnees_lecture.csv', 'w', newline='') as f:
>>>>>>> 8db762da01049691f83d6ede252763b8df6e5ddf
            # Ecrase les anciennes lignes par les nouvelles
            writer = csv.writer(f)
            writer.writerows(new_rows)
            
        programme()
        
initialisation()