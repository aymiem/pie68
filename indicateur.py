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
            
    for a in d["listeAvion"]:
        nomAvion = a.nom
        MpotH[nomAvion] = [] #On crée une liste vide pour le potentiel horaire de chaque avion
        indic["FlightTime"][nomAvion] = 0 #On crée une liste vide pour le temps de vol réalisé de chaque avion
    
    MpotH["somme"] = [0] * (d["temps"] - 4) #On crée une liste qui sera la somme des pot. sur chaque période

    NbrMaint = [0] * ( d["temps"] - 4)
    nbrAvionMission = [0] * ( d["temps"] - 4)
    nbrAvionFree = [0] * ( d["temps"] - 4)
    
    PotCalTot = len(d["listeAvion"])*(d["temps"])
    

    indic["MpotH"] = MpotH
    indic["NbrMaint"] = NbrMaint
    indic["PotCalTot"] = PotCalTot
    indic["nbrAvionMission"] = nbrAvionMission
    indic["nbrAvionFree"] = nbrAvionFree
    indic["avionDispo"]= [0] * ( d["temps"] - 4)
    indic["min_dispo"] = 0
    
    return indic
    
    
def Remplir_Indicateurs(d, df, indic, t):
    
    
    for a in d["listeAvion"]:
        nomAvion = a.nom
        indic["MpotH"][nomAvion].append(a.pot_horaire) # On rajoute la dernière valeur à la liste
        
        if (t>1):
            if (indic["MpotH"][nomAvion][t-2]-a.pot_horaire > 0) :
                indic["FlightTime"][nomAvion] += indic["MpotH"][nomAvion][t-2]-a.pot_horaire 
            
        indic["MpotH"]["somme"][t-1] += indic["MpotH"][nomAvion][t-1] # On fait la somme des pot. sur tous les avions à chaque période


        if str(df.xs(t)[a])[0] == "V":
            indic["NbrMaint"][t-1] += 1
            indic["PotCalTot"] -= 1
