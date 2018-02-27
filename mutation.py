import pandas as pd
import numpy as np
from main import programme
from ecriture import nom_fichier_sortie
import time
from constantes import paths
from selection_operator import fitness_ope_indiv, fitness_lis_indiv


def mutation(parents_gen, parent_num, child_num, ope, nb_iter):
    
    tt = time.time()
    parent = "solution"+parent_num+".csv" # nom du parente
        
    # Lors de la première tentative de mutation à partir de l'individu "parent_num"
    # on met à jour le nom du fichier de sortie pour enregistrer une nouvelle solution
    # Après tant que is_better renvoit False, on itère jusqu'à trouver une meilleure
    # solution au sens de l'indicateur aggrégé choisi. On ré-écrit sur la solution 
    # précédente dans ce cas.
    
    changes = False
    
    for iteration in range(nb_iter):
        
        df = pd.read_csv(paths.solutions_path + parent, sep=';', \
                         header=0, index_col=0)
        
        # choix aléatoire de la taille de la zone des mutations
        changes_size = np.random.randint(30,min(len(df.index),len(df.columns)))
        kept_height_size = len(df.index) - changes_size
        kept_length_size = len(df.columns) - changes_size
        
        # choix aléatoire de la position de la zone de mutation
        offset = np.random.randint(0,kept_height_size+1)
        
        # Mutation en fin de planning
        df.iloc[offset:offset+changes_size, kept_length_size:] = pd.DataFrame(index=df.iloc[offset:offset+changes_size, \
              kept_length_size:].index, columns=df.iloc[offset:offset+changes_size, kept_length_size:].columns)
            
        # Mutation en début de planning 
        #df.iloc[offset:offset+changes_size, :changes_size] = pd.DataFrame(index=df.iloc[offset:offset+changes_size, \
        #     :changes_size].index, columns=df.iloc[offset:offset+changes_size, :changes_size].columns)
        
        print("pourcentage de mutation :", changes_size*changes_size*100/(len(df.index)*len(df.columns)))
        
        dummy_df = pd.DataFrame(0, index = range(5), columns = df.columns.values)
        df = pd.concat([dummy_df, df])
        dummy_df = np.zeros(len(df))
        df.insert(0, value = dummy_df, column = '0')

        # mutation         
        new_indic, new_df = programme(False, df)
        
        # si on trouve une meilleure solution on sort de la boucle et on renvoit la solution
        if is_better(parent, new_indic, ope):
            changes = True
            break
        
    print(time.time() - tt, "secondes pour la mutation !")
    return changes

            
def is_better(parent_name, indics_enfant, operationnel):
    # répond au sens de l'indicateur opérationnel (ope = True) ou de maintenance 
    # (ope = False si operateur de lissage) si l'enfant est plus performant que le parent
    # output = True si l'enfant a un meilleur score et False sinon

    if operationnel == True : 
        if fitness_ope_indiv(parent_name) <= fitness_ope_indiv(indics_enfant):
            return True
        else:
            return False
    else:
        if fitness_lis_indiv(parent_name) <= fitness_ope_indiv(indics_enfant):
            return True
        else:
            return False
        