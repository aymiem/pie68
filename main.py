from objects import *
from algorithmeGlouton import *
import pandas as pd
from lecture import *



def programme():

    # saisie des avions
    path = 'donnees_lecture.csv'


    lectCSV=lecture(path)

    nom_ficher= lectCSV[5];
    for i in nom_ficher:
        print(i)

    listeAvion=lectCSV[0]
    listeMission=lectCSV[1]

    listeMaintenance = lectCSV[2]  # lecture de la liste maintenances
    para_init = lectCSV[3]  # parametres de la simulation
    mois, annee = para_init.moisInit, para_init.anInit
    temps = 12 * (para_init.anFin - annee) + (para_init.moisFin - mois)

    df1=lectCSV[4]
    ndarraySitInit=df1.as_matrix()
    if ndarraySitInit.any()==True:
        df=pd.DataFrame(index=list(range(1, temps + 2)),columns=listeAvion)
    else:
        df=pd.DataFrame(ndarraySitInit,index=list(range(1, temps + 2)),columns=listeAvion)
    print(df)

    liste_nbh_metropole = []
    liste_nb_maintenance = []
    liste_nb_maintenance_p = []

    for t in range(1, temps -3):
        # print(Nancy_D.type,D601.type)
        h = 0
        mi = 0
        mip=0
        for m in listeMission:
            t_deb = 12 * (m.annee_debut - annee) + (m.mois_debut - mois)
            t_fin = 12 * (m.annee_fin - annee) + (m.mois_fin - mois)
            if (t_deb <= t and t <= t_fin):
                nbmiss = 0;
                for a in listeAvion:
                    if str(df.xs(t)[a]).split("$")[0] == m.nom:
                        nbmiss = nbmiss + 1

                if nbmiss < m.nb_avion:
                    if t_fin - t >= 5:
                        affectationMission(m, listeAvion, nbmiss, df.xs, 4, t,listeMission)

                    if (t_fin - t == 4 or t_fin - t == 2):
                        affectationMission(m, listeAvion, nbmiss, df.xs, 3, t,listeMission)

                    if (t_fin - t == 3 or t_fin - t == 1):
                        affectationMission(m, listeAvion, nbmiss, df.xs, 2, t,listeMission)

                    if t_fin - t == 0:
                        affectationMission(m, listeAvion, nbmiss, df.xs, 1, t,listeMission)
                        # df.xs(list(range(t,t+a.proch_maint.duree+1)[x] = a.proch_maint
            modifPot(m, df, listeAvion, t)
        # print(df)
        for a in listeAvion:
            if str(df.xs(t)[a])[0] == "V":
                mi=mi+1
                if t>1:
                    if str(df.xs(t - 1)[a])[0] != "V":
                        mip=mip+1
                if t==1:
                    mip=mip+1



        for a in listeAvion:
            if t > 1:
                if str(df.xs(t)[a])[0] == "V" and str(df.xs(t - 1)[a])[0] != "V":
                    affectMaint(a, t, df, listeMaintenance)
            if t ==1:
                if str(df.xs(t)[a])[0] == "V":
                    affectMaint(a, t, df, listeMaintenance)
            if (a.pot_mois <= 0 or a.pot_horaire<=17)  and pd.isnull(df.xs(t)[a]) and mi<16 and mip<3:
                affectMaint(a, t, df, listeMaintenance)
                mi = mi + 1
                mip = mip + 1

        for a in listeAvion:
            #print(a.pot_horaire)
            a.pot_mois = a.pot_mois - 1

            #abc = PU global (donnée d’entrée) – PU OPEX)/12

            if (pd.isnull(df.xs(t)[a]) and a.pot_horaire >= 18):
                a.pot_horaire = a.pot_horaire - 18
                h = h + 18
                #df.xs(t)[a] = ("$18")

        liste_nbh_metropole.append(h)
        liste_nb_maintenance.append(mi)
        liste_nb_maintenance_p.append(mip)

    df.T.to_csv(nom_ficher[3], sep=';')
    ecriture_donnees(liste_nb_maintenance,liste_nbh_metropole,liste_nb_maintenance_p,temps)
    print(df)

def ecriture_donnees(l1,l2,l3,t):
    with open('indicateurs.csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',lineterminator = '\n')
        spamwriter.writerow(['pas de temps']+list(range(1, t-3)))
        spamwriter.writerow(['nombre d\'avions en maintenance']+ l1)
        spamwriter.writerow(['mip']+ l3)

        spamwriter.writerow(['nombre d\'heures en metropole']+ l2)


if __name__ == '__main__': programme()
