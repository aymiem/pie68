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
    MpotC = dict()
    
    indic["FlightTime"] = dict()
    indic["tauxRempMission"]= dict()
    indic["RempMission"] = dict()
            
    for a in d["listeAvion"]:
        nomAvion = a.nom
        MpotH[nomAvion] = [] #On crée une liste vide pour le potentiel horaire de chaque avion
        MpotC[nomAvion] = [] #On crée une liste vide pour le potentiel calendaire de chaque avion
        indic["FlightTime"][nomAvion] = 0 #On crée une liste vide pour le temps de vol réalisé de chaque avion
    
    for m in d["listeMission"]: #Pour chaque mission, on calculera le nombre d'avion affecter à chaque période à cette mission
        mission = m.nom
        indic["tauxRempMission"][mission] = [0] * ( d["temps"] - 3)
        indic["RempMission"][mission] = 0
        
    MpotH["somme"] = [0] * (d["temps"] - 4) #On crée une liste qui sera la somme des pot. sur chaque période

    #PotCalTot = len(d["listeAvion"])*(d["temps"])
    

    indic["MpotH"] = MpotH
    indic["MpotC"] = MpotC
    
    indic["NbrMaint"] = [0] * ( d["temps"] - 6)
    #indic["PotCalTot"] = PotCalTot
    indic["nbrAvionMission"] = [0] * ( d["temps"] - 3)
    indic["nbrAvionFree"] = [0] * ( d["temps"] - 3)
    indic["avionDispo"]= [0] * ( d["temps"] - 4)
    indic["min_dispo"] = 0
    indic["listPotPerdu"] = []
    indic["last_cravate"] = 0
    indic["moy_pot_perdu"] = 0
    indic["min_pot_perdu"] = 0
    
    return indic
    
    
def Remplir_Indicateurs_temporels(d, df, indic, t):
    
    for a in d["listeAvion"]:
        nomAvion = a.nom
        indic["MpotH"][nomAvion].append(a.pot_horaire) # On rajoute la dernière valeur de pot horaire à la liste
        indic["MpotC"][nomAvion].append(a.pot_mois) # On rajoute la dernière valeur de pot calendaire à la liste
        
        if (t>1):
            if (indic["MpotH"][nomAvion][t-2]-a.pot_horaire > 0) :
                indic["FlightTime"][nomAvion] += indic["MpotH"][nomAvion][t-2]-a.pot_horaire #heures volées
            
        indic["MpotH"]["somme"][t-1] += indic["MpotH"][nomAvion][t-1] # On fait la somme des pot. sur tous les avions à chaque période
        #indic["PotMois"][nomAvion].append(a.pot_mois)

        if (t>3):
            if str(df.xs(t)[a])[0] == "V":
                indic["NbrMaint"][t-4] += 1 #on compte un avion en maintenance
                #indic["PotCalTot"] -= 1

        if t>1:
            if indic["MpotH"][nomAvion][t-2] < indic["MpotH"][nomAvion][t-1]:
                indic["listPotPerdu"].append(indic["MpotH"][nomAvion][t-2])
                
                if indic["MpotC"][nomAvion][t-2] > 0: 
                    if (float((indic["MpotH"][nomAvion][t-2])/(indic["MpotC"][nomAvion][t-2])) < 10 ): #avions avec un potentiel horaire/calendaire faible (inf à 10) au dernier pas de temps, et qui devraient donc être en maintenance
                               #peu après le dernier pas de temp
                        indic["last_cravate"]+= 1
                
def Remplir_Indicateurs_globaux(d, df, indic):
    indic["MpotH"]["min_somme"] = min(indic["MpotH"]["somme"]) # L'indicateur est le min de la somme des pot
    indic["MpotH"]["moy_somme"] = np.mean(indic["MpotH"]["somme"]) # L'indicateur est la moyenne de la somme des pot
    indic["var_maint"] = np.var(np.asarray(indic["NbrMaint"])) #Calcul de la variance du nombre d'avion en maintenance
    indic["Min_maint"] = min(indic["NbrMaint"]) #Calcul du min d'avion en maintenanc
    indic["Max_maint"] = max(indic["NbrMaint"]) #Calcul du max d'avion en maintenance (normalement égal à la contrainte imposé au code)
    indic["delta_maint"] = indic["Max_maint"] - indic["Min_maint"]
    indic["min_pot_perdu"] = min(indic["listPotPerdu"])
    indic["moy_pot_perdu"] = np.mean(indic["listPotPerdu"])
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
