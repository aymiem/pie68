import csv

# Ecriture de la solution finale dans le csv de sortie
def solution_to_csv(df,nom_fichier):
    # fonction to_csv importée de Pandas. 'T' pour transposer la matrice
    df.T.to_csv(nom_fichier, sep=';')

# Creation d'un fichier indicateurs.csv # NON utilisé
def ecriture_donnees(indic):
    with open('indicateurs.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',lineterminator = '\n')
        #spamwriter.writerow(['pas de temps']+list(range(1, t-3)))
        #spamwriter.writerow(['nombre d\'avions en maintenance']+ l1)
        #spamwriter.writerow(['mip']+ l3)
        spamwriter.writerow(['moyenne potentiel horaire, à maximiser'] + [indic["MpotH"]["moy_somme"]])
        spamwriter.writerow(['minimun potentiel horaire, à maximiser'] + [indic["MpotH"]["min_somme"]])
        spamwriter.writerow(['variance maint, à minimiser'] + [indic["Maint_var"]])
        spamwriter.writerow(['max maint, contrainte de capacité à ne pas dépasser'] + [indic["Max_var"]])
        
        #spamwriter.writerow(['nombre d\'heures en metropole']+ l2)