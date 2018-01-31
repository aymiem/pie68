import csv

# Ecriture de la solution finale dans le csv de sortie
def solution_to_csv(df,nom_fichier):
    # fonction to_csv importée de Pandas. 'T' pour transposer la matrice
    df.T.to_csv(nom_fichier, sep=';')

# Creation d'un fichier indicateurs.csv # NON utilisé
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
        spamwriter.writerow(['max_maint'] + [indic["Max_maint"]]) #max maint, contrainte de capacité à ne pas dépasser
        spamwriter.writerow(['pot_cal_tot'] + [indic["PotCalTot"]]) #Disponibilité totale planifié, soit le nombre total de créneau moins le nombre de créneau occupé par une maintenance
        spamwriter.writerow(['pot_perdu'] + [indic["PotPerdu"]]) #Potentiel perdu total à minimiser
        spamwriter.writerow(['var_pot_perdu'] + [indic["varPotPerdu"]]) #Potentiel perdu minimum 
        spamwriter.writerow(['moy_pot_perdu'] + [indic["moyPotPerdu"]]) #Potentiel perdu moyen
        spamwriter.writerow(['min_dispo'] + [indic["min_dispo"]]) # nbr d'avion dispo (mission + entrainement), à maximiser
        
        #for m in listMission:
        #           spamwriter.writerow(['remp_'+m.nom] + [indic["RempMission"][m.nom]]) # pourcentage de remplissage de la mission sur sa période, objectif = 1