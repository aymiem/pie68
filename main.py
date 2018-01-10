from objects import *
from algorithme import *
import pandas as pd
from lecture import *
from ecriture import *
from constantes import *
from indicateur import *
import numpy as np

def programme():
    print('Lancement du programme ')

    x=constantes.path # Nom du fichier contenant la liste des autres CSV
    d=lectureEntrees(x) # Lecture des fichiers d'entrées
    df=dataframe(d) # Création du dataframe
    indicateurs = Init_Indicateurs(d)
    MpotH, NbrMaint = indicateurs
    NbrMaint, MpotH, Maint_var = remplir(d,df, MpotH, NbrMaint) # remplissage du dataframe
    indic = dict()
    indic["Min_et_moy_potH"] = [MpotH["min_somme"],MpotH["moy_somme"]]
    #indic['NbrMaint'] = NbrMaint
    indic["Maint_var"] = Maint_var
    #indic['MpotH'] = MpotH
    
    df = ecriture(d,df,indic) # export des données en CSV
#        with open('dict.csv', 'rb') as csv_file:
#        reader = csv.reader(csv_file)
#        MpotH = dict(reader)
    
    return indic, df

def remplir(d, df, MpotH, NbrMaint): # Fonction pour remplir le dataframe

    # Creation de trois listes utilisées dans le fichier indicateur de sortie 'indicateurs.csv'
    #liste_nbh_metropole = []
    #liste_nb_maintenance = []
    #liste_nb_maintenance_p = []

    for t in range(1, d["temps"] - 3):
        h,mi,mip= 0,0,0
        # h: nombre d'heures de vol à l'instant t
        # mi: nombre d'avions en stockage à l'instant t
        # mip: nombre les nouvelles entrées en stockage à l'instant t

        print(str(int(t / (d["temps"] - 3) * 100)) + '% ')  # Pourcentage avancement dans les calculs

        # gestion des affectations missions
        Remplir_Indicateurs(d, df, MpotH, NbrMaint, t)
        opex = 1
        remplir_mission(d, t, df, opex) # Affectation des opex
        opex = 0
        remplir_mission(d, t, df, opex) # Affectation des missions en métrople
        modif_mission(d, t, df) # modification des potentiels missions
        remplir_maintenance(d, t, df, mi, mip) # Affectations des maintenances
        remplir_autres(d, t, df, h) # Gestion des avions qui ne sont ni en maint ni en mission

    MpotH["min_somme"] = min(MpotH["somme"]) # L'indicateur est le min de la somme des pot
    MpotH["moy_somme"] = np.mean(MpotH["somme"]) # L'indicateur est la moyenne de la somme des pot

#    Calcul de la variance du nombre d'avions en maintenance
#    moy = mean(NbrMaint)
#    ecart = [] * ( d["temps"] - 3 )
#    for t in (1,d["temps"]-3):
#        ecart(t) = (NbrMaint(t) - moy)*(NbrMaint(t)-moy)
#    var = mean(ecart) #indicateur -> variance du nombre d'avions en maintenance
    Maint_var = np.var(np.asarray(NbrMaint))
    
    return NbrMaint, MpotH, Maint_var

def lectureEntrees(path):
    # Appel de la fonction lecture, en paramètre :path
    lectureCSV = lecture(path) #lectureCSV est une liste, on la transforme en dictionnaire pour une meilleure lisibilité
    dictionnaire = {"listeAvion": lectureCSV[0], "listeMission": lectureCSV[1], "listeMaintenance": lectureCSV[2],
                    "df1": lectureCSV[3], "nom_ficher": lectureCSV[4]}

    # definitions des unités temporelles et du pas de temps
    mois, annee = parametre.moisInit, parametre.anInit
    dictionnaire["temps"] = 12 * (parametre.anFin - annee) + (parametre.moisFin - mois)
    print("Lecture des données terminée")
    #print(parametre.strategie)
    return dictionnaire

def modif_mission(d,t,df):
    for a in d["listeAvion"]:
        for m in d["listeMission"]:
            modifPot(m, df, a, t)  # modification des potentiels (avions affectés manuellement inclus)

def remplir_mission(d,t,df,opex):
    for m in d["listeMission"]:
        #print(m)
        # calcul des dates de début et de fin de la mission
        t_deb = 12 * (m.annee_debut - parametre.anInit) + (m.mois_debut - parametre.moisInit)
        t_fin = 12 * (m.annee_fin - parametre.anInit) + (m.mois_fin - parametre.moisInit) +1
        if (t_deb <= t <= t_fin):
            nbmiss = 0 #nombre d'avions affecté à la mission m à l'instant t
            for a in d["listeAvion"]: # On parcourt le dataframe pour calculer nbmiss
                if str(df.xs(t)[a]).split("$")[0] == m.nom:
                    nbmiss = nbmiss + 1

            if nbmiss < m.nb_avion:
                # Si le le nombre d'avions en missions est inférieur au besoin,
                # choix de la durée de l'affectation en mission. De quatre à un mois
                affectationChoix = constantes.typechoix
                if t_fin - t >= 5:
                    affectationMission(m, d["listeAvion"], nbmiss, df.xs, 4, t, d["listeMission"], opex,affectationChoix)
                if (t_fin - t == 4 or t_fin - t == 2):
                    affectationMission(m, d["listeAvion"], nbmiss, df.xs, 3, t, d["listeMission"], opex,affectationChoix)
                if (t_fin - t == 3 or t_fin - t == 1):
                    affectationMission(m, d["listeAvion"], nbmiss, df.xs, 2, t, d["listeMission"], opex,affectationChoix)
                if t_fin - t == 0:
                    affectationMission(m, d["listeAvion"], nbmiss, df.xs, 1, t, d["listeMission"], opex,affectationChoix)



def remplir_maintenance(d,t,df,mi,mip):
    # Calcul nb de maintenance à i'intant t (affectation à la main ou algo)
    for a in d["listeAvion"]:
        if str(df.xs(t)[a])[0] == "V":
            mi = mi + 1
            if t > 1:
                if str(df.xs(t - 1)[a])[0] != "V":
                    mip = mip + 1
            if t == 1:
                mip = mip + 1
    # gestion des affectations maintenances
    for a in d["listeAvion"]:
        if t > 1: # gestion des affectations manuelles en maintenance pour t>1
            if str(df.xs(t)[a])[0] == "V" and str(df.xs(t - 1)[a])[0] != "V":
                affectMaint(a, t, df, d["listeMaintenance"])
        if t == 1: # gestion des affectations manuelles en maintenance pour t=1
            if str(df.xs(t)[a])[0] == "V":
                affectMaint(a, t, df, d["listeMaintenance"])
        # gestion des affectations automatisées en maintenance
        if (a.pot_mois <= 1) and pd.isnull(df.xs(t)[a]) and mi < parametre.stockageTotal and mip < parametre.entreeSTKparMois:
            affectMaint(a, t, df, d["listeMaintenance"])
            mi = mi + 1
            mip = mip + 1

    # une fois les avions qui n'ont plus de pot calendaire affectés, on effecture un lissage supplémentaire si strategie choisie en csv
    if mip < parametre.entreeSTKparMois and mi < parametre.stockageTotal and parametre.strategie==constantes.strategie_lissage:
        liste = lissage(d)
        for a in liste:
            if a.pot_mois < parametre.anticipMaint and pd.isnull(
                    df.xs(t)[a]) and mi < parametre.stockageTotal and mip < parametre.entreeSTKparMois:
                affectMaint(a, t, df, d["listeMaintenance"])
                mi = mi + 1
                mip = mip + 1

def remplir_autres(d,t,df,h):
    # fonction pour gerer les avions ni en mission ni en maintenances
    for a in d["listeAvion"]:
        if pd.isnull(df.xs(t)[a]) or ((df.xs(t)[a]) == 'BL'): # les avions dont le potentiel calendaire change
            a.pot_mois = a.pot_mois - 1

        if (pd.isnull(df.xs(t)[a]) and a.pot_horaire >= parametre.puParMois): # les avions dont le potentiel horaire change
            a.pot_horaire = a.pot_horaire - parametre.puParMois
            h = h + parametre.puParMois
        elif (pd.isnull(df.xs(t)[a]) and a.pot_horaire < parametre.puParMois): # les avions qui n'ont plus de potentiel horaire
            # sont marqué dans le dataframe par '-'
            df.xs(t)[a] = ("-")
        elif pd.isnull(df.xs(t)[a]) == False and str(df.xs(t)[a]).split('$')[0] == "":
            # prise en compte des modifications manuelles des potentiels horaires.
            if int(df.xs(t)[a].split('$')[1]) <= a.pot_horaire: # la valeur marqué est inférieur au pot reestant de l'avion
                a.pot_horaire = a.pot_horaire - int(df.xs(t)[a].split('$')[1]) # On soustrait la valeur précisée après le signe $
                h = h + int(df.xs(t)[a].split('$')[1])
            else: # sinon, on ne prend pas en compte la valeur entrée dans le csv et on la suprrime du dataframe
                a.pot_horaire = a.pot_horaire - parametre.puParMois
                h = h + parametre.puParMois
                df.xs(t)[a] = ""

def ecriture(d,df,indic):
    # Appel de la fonction solution_to_csv pour exporter les donneés
    solution_to_csv(df, d["nom_ficher"][3])
    ecriture_donnees(indic,d["nom_ficher"][3])
    
    return df

def dataframe(d):
    # Association entre la matrice de rebouclage (si non  vide) et le pas de temps
    ndarraySitInit = d["df1"].as_matrix()
    if ndarraySitInit.any() == True:
        df = pd.DataFrame(index=list(range(1, d["temps"] + 2)), columns=d["listeAvion"])
    else:
        df = pd.DataFrame(ndarraySitInit, index=list(range(1, d["temps"] + 2)), columns=d["listeAvion"])
    return df


#if __name__ == '__main__': NbrMaint, MpotH, Maint_var, df = programme()
if __name__ == '__main__': indic, df = programme()