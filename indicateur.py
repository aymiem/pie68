from objects import *
from algorithme import *
import pandas as pd
import numpy as np
from lecture import *
from ecriture import *
from constantes import *
from sklearn import decomposition
from sklearn.decomposition import PCA

def Init_Indicateurs(d, indic):
    
    MpotH = dict()
    indic["FlightTime"] = dict()
    indic["tauxRempMission"]= dict()
    indic["RempMission"] = dict()
            
    for a in d["listeAvion"]:
        nomAvion = a.nom
        MpotH[nomAvion] = [] #On crée une liste vide pour le potentiel horaire de chaque avion
        indic["FlightTime"][nomAvion] = 0 #On crée une liste vide pour le temps de vol réalisé de chaque avion
    
    for m in d["listeMission"]: #Pour chaque mission, on calculera le nombre d'avion affecter à chaque période à cette mission
        mission = m.nom
        indic["tauxRempMission"][mission] = [0] * ( d["temps"] - 3)
        indic["RempMission"][mission] = 0
        
    MpotH["somme"] = [0] * (d["temps"] - 4) #On crée une liste qui sera la somme des pot. sur chaque période

    NbrMaint = [0] * ( d["temps"] - 3)
    nbrAvionMission = [0] * ( d["temps"] - 3)
    nbrAvionFree = [0] * ( d["temps"] - 3)
    
    #PotCalTot = len(d["listeAvion"])*(d["temps"])
    

    indic["MpotH"] = MpotH
    indic["NbrMaint"] = NbrMaint
    #indic["PotCalTot"] = PotCalTot
    indic["nbrAvionMission"] = nbrAvionMission
    indic["nbrAvionFree"] = nbrAvionFree
    indic["avionDispo"]= [0] * ( d["temps"] - 4)
    indic["min_dispo"] = 0
    indic["listPotPerdu"] = []
    indic["moyPotPerdu"] = 0
    indic["minPotPerdu"] = 0
    
    return indic
    
    
def Remplir_Indicateurs_temporels(d, df, indic, t):
    
    
    for a in d["listeAvion"]:
        nomAvion = a.nom
        indic["MpotH"][nomAvion].append(a.pot_horaire) # On rajoute la dernière valeur à la liste
        
        if (t>1):
            if (indic["MpotH"][nomAvion][t-2]-a.pot_horaire > 0) :
                indic["FlightTime"][nomAvion] += indic["MpotH"][nomAvion][t-2]-a.pot_horaire 
            
        indic["MpotH"]["somme"][t-1] += indic["MpotH"][nomAvion][t-1] # On fait la somme des pot. sur tous les avions à chaque période
        #indic["PotMois"][nomAvion].append(a.pot_mois)

        if str(df.xs(t)[a])[0] == "V":
            indic["NbrMaint"][t-1] += 1
            #indic["PotCalTot"] -= 1

        if t>1:
            if indic["MpotH"][nomAvion][t-2] < indic["MpotH"][nomAvion][t-1]:
                indic["listPotPerdu"].append(indic["MpotH"][nomAvion][t-2])

def Remplir_Indicateurs_globaux(d, df, indic):
    indic["MpotH"]["min_somme"] = min(indic["MpotH"]["somme"]) # L'indicateur est le min de la somme des pot
    indic["MpotH"]["moy_somme"] = np.mean(indic["MpotH"]["somme"]) # L'indicateur est la moyenne de la somme des pot
    indic["Maint_var"] = np.var(np.asarray(indic["NbrMaint"])) #Calcul de la variance du nombre d'avion en maintenance
    indic["Min_maint"] = min(indic["NbrMaint"]) #Calcul du min d'avion en maintenanc
    indic["Max_maint"] = max(indic["NbrMaint"]) #Calcul du max d'avion en maintenance (normalement égal à la contrainte imposé au code)
    indic["delta_maint"] = indic["Max_maint"] - indic["Min_maint"]
    indic["minPotPerdu"] = min(indic["listPotPerdu"])
    indic["moyPotPerdu"] = np.mean(indic["listPotPerdu"])
    indic["FlightTime_var"] = np.var(
            np.fromiter(iter(indic["FlightTime"].values()), dtype=int)
            )
    
    for t in range(1, d["temps"]-3):
        indic["avionDispo"][t-1] = indic["nbrAvionMission"][t-1] + indic["nbrAvionFree"][t-1]
    
    indic["min_dispo"] = np.min(indic["avionDispo"])
    
    
    for m in d["listeMission"]:
        t_deb = 12 * (m.annee_debut - parametre.anInit) + (m.mois_debut - parametre.moisInit)
        t_fin = 12 * (m.annee_fin - parametre.anInit) + (m.mois_fin - parametre.moisInit) +1
        indic["RempMission"][m.nom] = np.mean(indic["tauxRempMission"][m.nom][int(t_deb) : int(t_fin)])
