from objects import *
from algorithme import *
import pandas as pd
import numpy as np
from lecture import *
from ecriture import *
from constantes import *


def Init_Indicateurs(d, indic):
    
    MpotH = dict()
    for a in d["listeAvion"]:
        nomAvion = a.nom
        MpotH[nomAvion] = [] #On crée une liste vide pour chaque avion
    MpotH["somme"] = [0] * (d["temps"] - 1) #On crée une liste qui sera la somme des pot. sur chaque période

    NbrMaint = [0] * ( d["temps"] - 1)
    
    PotCalTot = len(d["listeAvion"])*d["temps"]
    
    
    PotPerdu = 0
    
    indic["MpotH"] = MpotH
    indic["NbrMaint"] = NbrMaint
    indic["PotCalTot"] = PotCalTot
    indic["PotPerdu"] = PotPerdu
    
    
    return indic
    
    
def Remplir_Indicateurs(d, df, indic, t):
    for a in d["listeAvion"]:
        nomAvion = a.nom
        indic["MpotH"][nomAvion].append(a.pot_horaire) # On rajoute la dernière valeur à la liste
        indic["MpotH"]["somme"][t-1] += indic["MpotH"][nomAvion][t-1] # On fait la somme des pot. sur tous les avions à chaque période
        indic["PotMois"][nomAvion].append(a.pot_mois)
        if str(df.xs(t)[a])[0] == "V":
            indic["NbrMaint"][t-1] += 1
            #PotCalTot
        if t>1:
            if indic["MpotH"][nomAvion][t-2] < indic["MpotH"][nomAvion][t-1]:
                indic["PotPerdu"] += indic["MpotH"][nomAvion][t-2]