import csv

# Ecriture de la solution finale dans le csv de sortie
def solution_to_csv(df,nom_fichier):
    # fonction to_csv importée de Pandas. 'T' pour transposer la matrice
    df.T.to_csv(nom_fichier, sep=';')

# Creation d'un fichier indicateurs.csv
def ecriture_donnees(listMission,indic,nom_fichier):
    num = nom_fichier[8:10]
    if num == "0.":
        nom = "indicateurs0.csv"
    else:
        nom = "indicateurs"+num+".csv"
    with open(nom, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',lineterminator = '\n')
        
        spamwriter.writerow(['moy_pot_hor'] + [indic["MpotH"]["moy_somme"]]) #moyenne potentiel horaire, à maximiser
        spamwriter.writerow(['min_pot_hor'] + [indic["MpotH"]["min_somme"]])  #minimun potentiel horaire, à maximiser
        spamwriter.writerow(['var_maint'] + [indic["Maint_var"]]) #variance maint, à minimiser
        spamwriter.writerow(['delta_maint'] + [indic["delta_maint"]]) #eécart max du nombre d'avion en maintenance
        #spamwriter.writerow(['pot_cal_tot'] + [indic["PotCalTot"]]) #Disponibilité totale planifié, soit le nombre total de créneau moins le nombre de créneau occupé par une maintenance
        spamwriter.writerow(['min_pot_perdu'] + [indic["minPotPerdu"]]) #Potentiel perdu minimum 
        spamwriter.writerow(['moy_pot_perdu'] + [indic["moyPotPerdu"]]) #Potentiel perdu moyen
        spamwriter.writerow(['min_dispo'] + [indic["min_dispo"]]) # nbr d'avion dispo (mission + entrainement), à maximiser
        
        #for m in listMission:
        #           spamwriter.writerow(['remp_'+m.nom] + [indic["RempMission"][m.nom]]) # pourcentage de remplissage de la mission sur sa période, objectif = 1

def nom_fichier_sortie(generation, num_in_gen):
    # Fonction qui écrit à nouveau le fichier donnees_lecture.csv pour changer 
    # le nom du futur individu que l'on veut créer.
    # generation : dans [1..N], c'est le numéro de la génération de l'individu à créer
    # num_in_gen : dans [0..9], c'est le numéro de l'individu dans la génération    
    
    print("solution à créer :", num_in_gen, " de la generation ", generation)
        
    new_rows = [] # liste des lignes du fichier ré-écrit
    
    # création du dictionnaire du changement a effectuer
    if num_in_gen == 0:
        if generation == 1: # cas transcription de solution0 à solution10
            changes = { 
                    'solution0' : 'solution1'+str(num_in_gen)
                    }       
        else : # cas général de changement de generation
            changes = {   
                    'solution'+str(generation-1)+"9" : 'solution'+str(generation)+str(num_in_gen)
                    }        
    else: # cas entre deux individus de la meme generation
        changes = {   
            'solution'+str(generation)+str(num_in_gen - 1) : 'solution'+str(generation)+str(num_in_gen)
                }          
            
    with open('donnees_lecture.csv', 'r') as f:
        reader = csv.reader(f) 
        for row in reader:     # pour chaque ligne
            new_row = row      # on copie la ligne
            for key, value in changes.items(): 
                # et on modifie le nom du fichier enregistré
                new_row = [ x.replace(key, value) for x in new_row ] 
            new_rows.append(new_row) # ajoute les nouvelles lignes

    with open('donnees_lecture.csv', 'w', newline='') as f:
        # Ecrase les anciennes lignes par les nouvelles
        writer = csv.writer(f)
        writer.writerows(new_rows)