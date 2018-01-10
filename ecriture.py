import csv

# Ecriture de la solution finale dans le csv de sortie
def solution_to_csv(df,nom_fichier):
    # fonction to_csv importée de Pandas. 'T' pour transposer la matrice
    df.T.to_csv(nom_fichier, sep=';')

# Creation d'un fichier indicateurs.csv # NON utilisé
def ecriture_donnees(indic,nom_fichier):
    num = nom_fichier[8:10]
    nom = "indicateurs"+num+".csv"
    with open(nom, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',lineterminator = '\n')
        #spamwriter.writerow(['pas de temps']+list(range(1, t-3)))
        #spamwriter.writerow(['nombre d\'avions en maintenance']+ l1)
        #spamwriter.writerow(['mip']+ l3)
        spamwriter.writerow(['moy_pot_hor'] + [indic["MpotH"]["moy_somme"]]) #moyenne potentiel horaire, à maximiser
        spamwriter.writerow(['min_pot_hor'] + [indic["MpotH"]["min_somme"]])  #minimun potentiel horaire, à maximiser
        spamwriter.writerow(['var_maint'] + [indic["Maint_var"]]) #variance maint, à minimiser
        spamwriter.writerow(['max_maint'] + [indic["Max_maint"]]) #max maint, contrainte de capacité à ne pas dépasser
        spamwriter.writerow(['pot_cal_tot'] + [indic["PotCalTot"]]) #Disponibilité totale planifié, soit le nombre 
                                                         #total de créneau moins le nombre de créneau occupé par une maintenance
        #spamwriter.writerow(['nombre d\'heures en metropole']+ l2)
        spamwriter.writerow(['min_dispo'] + [indic["min_dispo"]]) # nbr d'avion dispo (mission + entrainement), à maximiser