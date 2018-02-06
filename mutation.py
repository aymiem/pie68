import pandas as pd
import numpy as np
from lecture import lectureDF
from main import programme
from ecriture import nom_fichier_sortie
import time
from selection_operator import fitness_ope_indiv, fitness_lis_indiv


def mutation(parents_gen, parent_num, child_num, ope):
    
    tt = time.time()
    parent = "solution"+parents_gen+parent_num+".csv" # nom du parente
    
    df = pd.read_csv(parent,sep=';',header=0,index_col=0)
    
    # Lors de la première tentative de mutation à partir de l'individu "parent_num"
    # on met à jour le nom du fichier de sortie pour enregistrer une nouvelle solution
    # Après tant que is_better renvoit False, on itère jusqu'à trouver une meilleure
    # solution au sens de l'indicateur aggrégé choisi. On ré-écrit sur la solution 
    # précédente dans ce cas.
    nom_fichier_sortie(int(parents_gen)+1, child_num)
    
    changes = False
    
    for iteration in range(4):
        # choix aléatoire de la taille de la matrice des mutations
        size_changes = len(df.index) - np.random.randint(1,len(df.index))
        df.iloc[size_changes:, size_changes:] = pd.DataFrame(index=df.iloc[size_changes:, \
               size_changes:].index, columns=df.iloc[size_changes:,size_changes:].columns)
        print("pourcentage de mutation :", size_changes*100/(len(df.index)*len(df.columns)))
        
        dummy_df = pd.DataFrame(0, index = range(5), columns = df.columns.values)
        df = pd.concat([dummy_df, df])
        dummy_df = np.zeros(len(df))
        df.insert(0, value = dummy_df, column = '0')
                
        print("mutation_df :", df)
        
        # mutation         
        new_indic, new_df = programme(False, df)
        
        # si on trouve une meilleure solution on sort de la boucle et on renvoit la solution
        if is_better(parent, new_indic, ope):
            changes = True
            break
        
    print(time.time() - tt, "secondes pour la mutation")
    return changes

            
def is_better(parent_name, indics_enfant, operationnel):
    # répond au sens de l'indicateur opérationnel (ope = True) ou de maintenance 
    # (ope = False si operateur de lissage) si l'enfant est plus performant que le parent
    # output = True si l'enfant a un meilleur score et False sinon
 
    if operationnel == True : 
        if fitness_ope_indiv(parent_name) >= fitness_ope_indiv(indics_enfant):
            return True
        else:
            return False
    else:
        if fitness_lis_indiv(parent_name) >= fitness_ope_indiv(indics_enfant):
            return True
        else:
            return False
        