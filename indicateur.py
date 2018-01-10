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
    
    indic["MpotH"] = MpotH
    indic["NbrMaint"] = NbrMaint
    indic["PotCalTot"] = PotCalTot
    
    
    return indic
    
    
def Remplir_Indicateurs(d, df, indic, t):
    for a in d["listeAvion"]:
        nomAvion = a.nom
        indic["MpotH"][nomAvion].append(a.pot_horaire) # On rajoute la dernière valeur à la liste
        indic["MpotH"]["somme"][t-1] += indic["MpotH"][nomAvion][t-1] # On fait la somme des pot. sur tous les avions à chaque période
        if str(df.xs(t)[a])[0] == "V":
            indic["NbrMaint"][t-1] += 1
            #PotCalTot