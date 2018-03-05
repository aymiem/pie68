from objects import *
from algorithme import *
import pandas as pd
from lecture import *
from ecriture import *
from constantes import *
from indicateur import *
import numpy as np
from sklearn import decomposition
from sklearn.decomposition import PCA
import time

def programme(is_init, dataframe_gen):
    print(' Execution de l algo glouton avec typechoix ', constantes.typechoix)
    
    tt = time.time()
    x=constantes.path # Nom du fichier contenant la liste des autres CSV
    d=lectureEntrees(x)# Lecture des fichiers d'entrées
    if is_init == False :
        d["df1"] = dataframe_gen.transpose()
    #print("creation df")
    df=dataframe(d)  # Création du dataframe
    
    mission_heures = {m.nom: m.pu for m in d["listeMission"]} # Dico des missions et leur potentiel horaire
    indic = dict()
    indic = Init_Indicateurs(d, indic)
    indic = remplir(d,df,indic, mission_heures) # remplissage du dataframe
    
    df = ecriture(d,df,indic) # export des données en CSV
#        with open('dict.csv', 'rb') as csv_file:
#        reader = csv.reader(csv_file)
#        MpotH = dict(reader)
    print("Execution glouton et creation solutionXX en", time.time() - tt )
    return indic, d

def remplir(d, df, indic, mission_heures): # Fonction pour remplir le dataframe
    
    # Initialisation du dataframe d'affectation avions en mission
    avions_affectes = pd.DataFrame(np.zeros((d['temps'],len(d["listeMission"]))), columns = [m.nom for m in d["listeMission"]])
    # boucle de parcourt nécessaire pour lecture d'une éventuelle modif manuelle de sitInit
    tt = time.time()
    for avion in d["listeAvion"]:
        for t in range(d['temps']):
            if isinstance(df.xs(t+1)[avion],str):
                if df.xs(t+1)[avion][0] != "V" and df.xs(t+1)[avion][0] != "-":
                    avions_affectes[df.xs(t+1)[avion]][t] += 1
                    
    #print("init avions_affectes",time.time() - tt)

    for t in range(1, d["temps"] - 3):
        
        print(str(int(t / (d["temps"] - 3) * 100)) + '% ')  # Pourcentage avancement dans les calculs
        
        h,mi,mip= 0,0,0
        # h: nombre d'heures de vol à l'instant t
        # mi: nombre d'avions en stockage à l'instant t
        # mip: nombre les nouvelles entrées en stockage à l'instant t

        #print(str(int(t / (d["temps"] - 3) * 100)) + '% ')  # Pourcentage avancement dans les calculs

        # gestion des affectations missions
        Remplir_Indicateurs_temporels(d, df, indic, t) #remplissage des indicateurs
        opex = 1
        remplir_mission(d, t, df, opex, indic, avions_affectes) # Affectation des opex
        opex = 0
        remplir_mission(d, t, df, opex, indic, avions_affectes) # Affectation des missions en métrople
        modif_mission(d, t, df, indic, mission_heures) # modification des potentiels missions
        remplir_maintenance(d, t, df, mi, mip) # Affectations des maintenances
        remplir_autres(d, t, df, h, indic, mission_heures) # Gestion des avions qui ne sont ni en maint ni en mission
        
    Remplir_Indicateurs_globaux(d, df, indic)
    
    return indic

def lectureEntrees(path):
    # Appel de la fonction lecture, en paramètre :path
    lectureCSV = lecture(path) #lectureCSV est une liste, on la transforme en dictionnaire pour une meilleure lisibilité
    dictionnaire = {"listeAvion": lectureCSV[0], "listeMission": lectureCSV[1], "listeMaintenance": lectureCSV[2],
                    "df1": lectureCSV[3], "nom_ficher": lectureCSV[4]}

    # definitions des unités temporelles et du pas de temps
    mois, annee = parametre.moisInit, parametre.anInit
    dictionnaire["temps"] = 12 * (parametre.anFin - annee) + (parametre.moisFin - mois)        

    return dictionnaire


def modif_mission(d,t,df, indic, m_h):
    for a in d["listeAvion"]:
        for m in d["listeMission"]:
            modifPot(m, df, a, t, indic, m_h)  # modification des potentiels (avions affectés manuellement inclus)


def remplir_mission(d,t,df,opex,indic, avions_affectes):

    for m in d["listeMission"]:
        # calcul des dates de début et de fin de la mission
        t_deb = 12 * (m.annee_debut - parametre.anInit) + (m.mois_debut - parametre.moisInit)
        t_fin = 12 * (m.annee_fin - parametre.anInit) + (m.mois_fin - parametre.moisInit) +1
                  
        if (t_deb <= t <= t_fin):
           
            #for a in d["listeAvion"]: # On parcourt le dataframe pour calculer nbmiss
            #   if str(df.xs(t)[a]).split("$")[0] == m.nom:
            #       nbmiss = nbmiss + 1

            if avions_affectes[m.nom][t-1] < m.nb_avion:
                # Si le le nombre d'avions en missions est inférieur au besoin,
                # choix de la durée de l'affectation en mission. De quatre à un mois
                affectationChoix = constantes.typechoix
                
                if t_fin - t >= 5:
                    avions_aj = affectationMission(m, d["listeAvion"], int(avions_affectes[m.nom][t-1]), df.xs, 4, t, d["listeMission"], opex,affectationChoix)
#                    indic["tauxRempMission"][m.nom][t] += 1 #on ajoute 1 au remplissage de la mission m pour toute la durée de la mission 
#                    indic["tauxRempMission"][m.nom][t+1] += 1
#                    indic["tauxRempMission"][m.nom][t+2] += 1
#                    indic["tauxRempMission"][m.nom][t+3] += 1
                    avions_affectes[m.nom][t-1] += avions_aj
                    avions_affectes[m.nom][t] += avions_aj
                    avions_affectes[m.nom][t+1] += avions_aj
                    avions_affectes[m.nom][t+2] += avions_aj
#                     
                if (t_fin - t == 4 or t_fin - t == 2):
                    avions_aj = affectationMission(m, d["listeAvion"], int(avions_affectes[m.nom][t-1]), df.xs, 3, t, d["listeMission"], opex,affectationChoix)
                    avions_affectes[m.nom][t-1] += avions_aj
                    avions_affectes[m.nom][t] += avions_aj
                    avions_affectes[m.nom][t+1] += avions_aj    
                    
                if (t_fin - t == 3 or t_fin - t == 1):
                    avions_aj = affectationMission(m, d["listeAvion"], int(avions_affectes[m.nom][t-1]), df.xs, 2, t, d["listeMission"], opex,affectationChoix)
                    avions_affectes[m.nom][t-1] += avions_aj
                    avions_affectes[m.nom][t] += avions_aj
                    
                if t_fin - t == 0:
                    avions_aj = affectationMission(m, d["listeAvion"], int(avions_affectes[m.nom][t-1]), df.xs, 1, t, d["listeMission"], opex,affectationChoix)
                    avions_affectes[m.nom][t-1] += avions_aj
                    
        #nbmiss = 0           
        #for a in d["listeAvion"]: # On reparcourt le dataframe pour recalculer le nombre affectés
        #        if str(df.xs(t)[a]).split("$")[0] == m.nom:
        #            nbmiss = nbmiss + 1
                    
        indic["tauxRempMission"][m.nom][t] = avions_affectes[m.nom][t-1]/m.nb_avion #on enregistre le remplissage de la mission

def remplir_maintenance(d,t,df,mi,mip):
    # Calcul nb de maintenance à i'intant t (affectation à la main ou algo)
    #for a in d["listeAvion"]:
        #if isinstance(df.xs(t)[a],str):
            #if df.xs(t)[a][0] == "V": #str
             #   mi = mi + 1
             #   if t > 1:
               #     if df.xs(t - 1)[a][0] != "V": #str
                #        mip = mip + 1
                #if t == 1:
                 #   mip = mip + 1
    # gestion des affectations maintenances
    for a in d["listeAvion"]:
        if isinstance(df.xs(t)[a],str): #!
            if df.xs(t)[a][0] == "V": #str
                mi = mi + 1
                if t == 1 :
                    mip = mip + 1
                    affectMaint(a, t, df, d["listeMaintenance"])
                elif t > 1 :
                    if isinstance(df.xs(t-1)[a],str):
                        if df.xs(t - 1)[a][0] != "V": #str
                            mip = mip + 1
                            affectMaint(a, t, df, d["listeMaintenance"])
                    else :
                        mip = mip + 1
                        affectMaint(a, t, df, d["listeMaintenance"])                        
                    #print(a, "affecté", df.xs(t)[a][0])

           #    if t == 1:
           #        mip = mip + 1
           #        affectMaint(a, t, df, d["listeMaintenance"])
           # if t > 1: # gestion des affectations manuelles en maintenance pour t>1
           #     if df.xs(t)[a][0] == "V" and df.xs(t - 1)[a][0] != "V":
           #         affectMaint(a, t, df, d["listeMaintenance"])
           #if t == 1: # gestion des affectations manuelles en maintenance pour t=1
           #     if df.xs(t)[a][0] == "V":
           #         affectMaint(a, t, df, d["listeMaintenance"])
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
                    
def remplir_autres(d,t,df,h, indic, mission_heures):
    # fonction pour gerer les avions ni en mission ni en maintenances
    for a in d["listeAvion"]:
        if (df.xs(t)[a]) == 'BL':
            a.pot_mois = a.pot_mois - 1
        if pd.isnull(df.xs(t)[a]) : # les avions dont le potentiel calendaire change
            a.pot_mois = a.pot_mois - 1
            if a.pot_horaire >= parametre.puParMois : # les avions dont le potentiel horaire change
                a.pot_horaire = a.pot_horaire - parametre.puParMois
                h = h + parametre.puParMois
                indic["nbrAvionFree"][t-1] += 1
            elif a.pot_horaire < parametre.puParMois : # les avions qui n'ont plus de potentiel horaire
                # sont marqué dans le dataframe par '-'
                df.xs(t)[a] = ("-")
        #if (pd.isnull(df.xs(t)[a]) and a.pot_horaire >= parametre.puParMois): # les avions dont le potentiel horaire change
        #    a.pot_horaire = a.pot_horaire - parametre.puParMois
        #    h = h + parametre.puParMois
        #    indic["nbrAvionFree"][t-1] += 1
        #elif (pd.isnull(df.xs(t)[a]) and a.pot_horaire < parametre.puParMois): # les avions qui n'ont plus de potentiel horaire
        #    # sont marqué dans le dataframe par '-'
        #    df.xs(t)[a] = ("-")
        elif pd.isnull(df.xs(t)[a]) == False and df.xs(t)[a] == "": #! str(df.xs(t)[a]).split('$')[0] == "":
            # prise en compte des modifications manuelles des potentiels horaires.
            # if int(df.xs(t)[a].split('$')[1]) <= a.pot_horaire: # la valeur marqué est inférieur au pot reestant de l'avion
            if mission_heures[df.xs(t)[a]] <= a.pot_horaire : #!
                a.pot_horaire = a.pot_horaire - mission_heures[df.xs(t)[a]] #!! On soustrait la valeur précisée après le signe $
                h = h + mission_heures[df.xs(t)[a]] #! int(df.xs(t)[a].split('$')[1])
            else: # sinon, on ne prend pas en compte la valeur entrée dans le csv et on la suprrime du dataframe
                a.pot_horaire = a.pot_horaire - parametre.puParMois
                h = h + parametre.puParMois
                df.xs(t)[a] = ""
                
def ecriture(d,df,indic):
    # Appel de la fonction solution_to_csv pour exporter les donneés
    solution_to_csv(df, d["nom_ficher"][3])
    ecriture_donnees(d["listeMission"],indic,d["nom_ficher"][3])
    
    return df

def dataframe(d):
    # Association entre la matrice de rebouclage (si non  vide) et le pas de temps
    ndarraySitInit = d["df1"].as_matrix()
    ndarraySitInit.shape
    if ndarraySitInit.any() == True:
        dfrm = pd.DataFrame(index=list(range(1, d["temps"] + 2)), columns=d["listeAvion"])
    else:
        d_temps = d["temps"] + 2
        dfrm = pd.DataFrame(ndarraySitInit[1:d_temps,5:], index=list(range(1, d_temps)), columns=d["listeAvion"])
    return dfrm

if __name__ == '__main__':
    programme(True,0)