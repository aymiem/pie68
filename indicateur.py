from objects import *
from algorithme import *
import pandas as pd
import numpy as np
from lecture import *
from ecriture import *
from constantes import *


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
        
    MpotH["somme"] = [0] * (d["temps"] - 3) #On crée une liste qui sera la somme des pot. sur chaque période

    NbrMaint = [0] * ( d["temps"] - 3)
    nbrAvionMission = [0] * ( d["temps"] - 3)
    nbrAvionFree = [0] * ( d["temps"] - 3)
    
    PotCalTot = len(d["listeAvion"])*(d["temps"])
    

    indic["MpotH"] = MpotH
    indic["NbrMaint"] = NbrMaint
    indic["PotCalTot"] = PotCalTot
    indic["nbrAvionMission"] = nbrAvionMission
    indic["nbrAvionFree"] = nbrAvionFree
    indic["avionDispo"]= [0] * ( d["temps"] - 3)
    indic["min_dispo"] = 0
    indic["PotPerdu"] = 0
    
    
    return indic
    
    
def Remplir_Indicateurs(d, df, indic, t):
    
    
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
            indic["PotCalTot"] -= 1

        if t>1:
            if indic["MpotH"][nomAvion][t-2] < indic["MpotH"][nomAvion][t-1]:
                indic["PotPerdu"] += indic["MpotH"][nomAvion][t-2]