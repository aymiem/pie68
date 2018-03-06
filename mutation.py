import pandas as pd
import numpy as np
from main import programme
import time
from constantes import paths
from selection_operator import fitness_ope_indiv, fitness_lis_indiv

# Lors de la première tentative de mutation à partir de l'individu "parent_num"
# on met à jour le nom du fichier de sortie pour enregistrer une nouvelle solution
# Après tant que is_better renvoit False, on itère jusqu'à trouver une meilleure
# solution au sens de l'indicateur aggrégé choisi. On ré-écrit sur la solution 
# précédente dans ce cas.

def mutation_arriere(parents_gen, parent_num, child_num, ope, nb_iter):
    
    tt = time.time()
    parent = "solution"+parent_num+".csv" # nom du parent
    # Variable booleene retournee indiquant si la mutation a abouti positivement
    changes = False 
    step_iter = 1
    
    for iteration in range(nb_iter):
        # Recuperation de la solution parente sous forme d'un dataframe
        df = pd.read_csv(paths.solutions_path + parent, sep=';', \
                         header=0, index_col=0)
        
        # Choix aléatoire oriente de la taille de la zone des mutations
        changes_size = np.random.randint(50,min(len(df.index),len(df.columns)))
        kept_height_size = len(df.index) - changes_size
        kept_length_size = len(df.columns) - changes_size
        
        # Choix aléatoire de la position de la zone de mutation
        offset = np.random.randint(0,kept_height_size+1)
        
        # Mutation part : ici, mutation en fin de planning
        df.iloc[offset:offset+changes_size, kept_length_size:] = pd.DataFrame(index=df.iloc[offset:offset+changes_size, \
               kept_length_size:].index, columns=df.iloc[offset:offset+changes_size, kept_length_size:].columns)
        
        print("Pourcentage de mutation :", changes_size*changes_size*100/(len(df.index)*len(df.columns)))

        dummy_df = pd.DataFrame(0, index = range(5), columns = df.columns.values)
        df = pd.concat([dummy_df, df])
        dummy_df = np.zeros(len(df))
        df.insert(0, value = dummy_df, column = '0')
        # Re-bouclage avec l'algorithme glouton sur le planning en partie rempli         
        new_indic, new_df = programme(False, df)
        step_iter += 1
        
        # si on trouve une meilleure solution on sort de la boucle et on renvoit la solution
        if is_better(parent, new_indic, ope):
            changes = True
            break
    
    print(time.time() - tt, "secondes pour la mutation arrière !")
    return changes


def mutation_avant(parents_gen, parent_num, child_num, ope, nb_iter):
    
    tt = time.time()
    parent = "solution"+parent_num+".csv"     
    changes = False
    step_iter = 1
    
    for iteration in range(nb_iter):
        # Recuperation de la solution parente sous forme d'un dataframe
        df = pd.read_csv(paths.solutions_path + parent, sep=';', \
                         header=0, index_col=0)        
        # Choix aléatoire oriente de la taille de la zone des mutations
        changes_size = np.random.randint(40,min(len(df.index),len(df.columns)))
        kept_height_size = len(df.index) - changes_size
        # Choix aléatoire de la position de la zone de mutation
        offset = np.random.randint(0,kept_height_size+1)                    
        
        # Mutation part : ici, mutation en début de planning
        df.iloc[offset:offset+changes_size, :changes_size] = pd.DataFrame(index=df.iloc[offset:offset+changes_size, \
              :changes_size].index, columns=df.iloc[offset:offset+changes_size, :changes_size].columns)                
        print("Pourcentage de mutation :", changes_size*changes_size*100/(len(df.index)*len(df.columns)))
        
        dummy_df = pd.DataFrame(0, index = range(5), columns = df.columns.values)
        df = pd.concat([dummy_df, df])
        dummy_df = np.zeros(len(df))
        df.insert(0, value = dummy_df, column = '0')
        # Re-bouclage avec l'algorithme glouton sur le planning en partie rempli         
        new_indic, new_df = programme(False, df)
        step_iter += 1
        
        # si on trouve une meilleure solution on sort de la boucle et on renvoit la solution
        if is_better(parent, new_indic, ope):
            changes = True
            break
        
    print(time.time() - tt, "secondes pour la mutation avant ! ")
    return changes

def mutation_del_some_planes(parents_gen, parent_num, child_num, ope, nb_iter):
    
    tt = time.time()
    parent = "solution"+parent_num+".csv"     
    changes = False
    step_iter = 1
    
    for iteration in range(nb_iter):
        # Recuperation de la solution parente sous forme d'un dataframe
        df = pd.read_csv(paths.solutions_path + parent, sep=';', \
                         header=0, index_col=0)        
                    
        # Mutation part : ici, mutation sur un nombre aléatoire d'avions choisis 
        # également de façon aléatoire. La mutation est réalisée sur l'intégralité 
        # des chromosomes des avions sélectionnés
        
        # Choix aléatoire du nombre d'avions à faire muter
        nb_avions = np.random.randint(30,len(df.index))
        list_position = []
        for k in range(nb_avions):
            # Choix aléatoire de la position du k-eme avion qui va muter
            position_mutation = np.random.randint(0, len(df.index))
            while position_mutation in list_position :
                position_mutation = np.random.randint(0, len(df.index))
            list_position.append(position_mutation)
            # Ajout de "NaN" sur la ligne de l'avion (ou chromosome) k
            df.iloc[position_mutation-1:position_mutation, :] = pd.DataFrame(index=df.iloc[position_mutation-1:position_mutation, \
                   :].index, columns=df.iloc[position_mutation-1:position_mutation, :].columns)
                
        print("Pourcentage de mutation :", nb_avions*len(df.columns)*100/(len(df.index)*len(df.columns)))

        dummy_df = pd.DataFrame(0, index = range(5), columns = df.columns.values)
        df = pd.concat([dummy_df, df])
        dummy_df = np.zeros(len(df))
        df.insert(0, value = dummy_df, column = '0')
        # Re-bouclage avec l'algorithme glouton sur le planning en partie rempli         
        new_indic, new_df = programme(False, df)        
        step_iter += 1
        
        # si on trouve une meilleure solution on sort de la boucle et on renvoit la solution
        if is_better(parent, new_indic, ope):
            changes = True
            break
    
    print(time.time() - tt, "secondes pour la mutation del_some_planes !")
    return changes

def mutation_i_aleatoire(parents_gen, parent_num, child_num, ope, nb_iter):
    # Ici, la mutation est réalisée sur l'intégralité des avions (ou 
    # chromosomes). Pour un avion A donné on choisit aléatoirement un pas de
    # temps "i_A" à partir duquel s'opère la mutation du chromosome "A"
        
    tt = time.time()
    parent = "solution"+parent_num+".csv"     
    changes = False
    step_iter = 1
    
    for iteration in range(nb_iter):
        # Recuperation de la solution parente sous forme d'un dataframe
        df = pd.read_csv(paths.solutions_path + parent, sep=';', \
                         header=0, index_col=0)         
        
        # Initialisation de la mutation de l'avion d'index 0
        i_list = [np.random.randint(1, len(df.columns))]
        df.iloc[0:0, i_list[0]:] = pd.DataFrame(index=df.iloc[0:0, i_list[0]:].index, \
               columns=df.iloc[0:0, i_list[0]:].columns)
        # On calcule au fur et à mesure le nombre de gène impliqué dans la mutation
        quantite_mutation = len(df.columns) - i_list[0]
        
        # Pour tout avion "A", on choisit la position de début de mutation puis
        # on ajoute des NaN dans la ligne du chromosome "A" à partir de cet 
        # indice "i_A" jusqu'au dernier pas de temps
        for A in range(1,len(df.index)):
            i_list.append(np.random.randint(1, len(df.columns)))
            df.iloc[A-1:A, i_list[A]:] = pd.DataFrame(index=df.iloc[A-1:A, i_list[A]:].index, \
                   columns=df.iloc[A-1:A, i_list[A]:].columns)
            quantite_mutation += len(df.columns) - i_list[A]
        
        print("Pourcentage de mutation :", quantite_mutation*100/(len(df.index)*len(df.columns)))

        dummy_df = pd.DataFrame(0, index = range(5), columns = df.columns.values)
        df = pd.concat([dummy_df, df])
        dummy_df = np.zeros(len(df))
        df.insert(0, value = dummy_df, column = '0')
        # Re-bouclage avec l'algorithme glouton sur le planning en partie rempli         
        new_indic, new_df = programme(False, df)        
        step_iter += 1
        
        # si on trouve une meilleure solution on sort de la boucle et on renvoit la solution
        if is_better(parent, new_indic, ope):
            changes = True
            break
    
    print(time.time() - tt, "secondes pour la mutation_i_aleatoire !")
    return changes

            
def is_better(parent_name, indics_enfant, operationnel):
    # répond au sens de l'indicateur opérationnel (ope = True) ou de maintenance 
    # (ope = False si operateur de lissage) si l'enfant est plus performant que le parent
    # output = True si l'enfant a un meilleur score et False sinon

    if operationnel == True : 
        print("OPE : parent = ",fitness_ope_indiv(parent_name), " enfant = ", fitness_ope_indiv(indics_enfant))
        if fitness_ope_indiv(parent_name) <= fitness_ope_indiv(indics_enfant):
            return True
        else:
            return False
    else:
        print("LIS : parent = ",fitness_lis_indiv(parent_name), " enfant = ", fitness_lis_indiv(indics_enfant))
        if fitness_lis_indiv(parent_name) <= fitness_lis_indiv(indics_enfant):
            return True
        else:
            return False
        
def type_mutation(num):  
    # Fonction appelant la mutation choisie pour le test
    if num == 0 :
        return mutation_arriere
    elif num == 1 :
        return mutation_del_some_planes
    elif num == 2 :
        return mutation_i_aleatoire
    elif num == 3 :
        return mutation_avant
    else : 
        return mutation_arriere