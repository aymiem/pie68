from objects import *
from algorithme import *
import pandas as pd
import numpy as np
from lecture import *
from ecriture import *
from constantes import *


def Init_Indicateurs(d):
    
    MpotH = dict()
    for a in d["listeAvion"]:
        nomAvion = a.nom
        MpotH[nomAvion] = [] #On crée une liste vide pour chaque avion
    MpotH["somme"] = [0] * (d["temps"] - 4) #On crée une liste qui sera la somme des pot. sur chaque période

    NbrMaint = [0] * ( d["temps"] - 4)
    
    return MpotH, NbrMaint
    
    
def Remplir_Indicateurs(d, df, MpotH, NbrMaint, t):
    for a in d["listeAvion"]:
        nomAvion = a.nom
        MpotH[nomAvion].append(a.pot_horaire) # On rajoute la dernière valeur à la liste
    
    for a in d["listeAvion"]:
        nomAvion = a.nom
        MpotH["somme"][t-1] += MpotH[nomAvion][t-1] # On fait la somme des pot. sur tous les avions à chaque période
        
    for a in d["listeAvion"]:
        if str(df.xs(t)[a])[0] == "V":
            NbrMaint[t-1] += 1          