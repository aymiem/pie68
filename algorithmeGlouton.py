from objects import *
import pandas as pd


def algo():
    # saisie des avions
    pass


# creation d'une liste des avions pouvant accomplir la mision
def besoinEnMission(m,l_m, l_a, nbmiss, affect,nb,t):
    liste = []
    for a in l_a:
        #nb mois * potdemandé/mois + 100 à la place des 600
        if (m.opex == 1 and m.type_avion == a.type_avion and capaciteMission(a,m)
            and a.pot_horaire >=(nb*m.pu+100)  and pd.isnull(
                affect(t)[a]) and (pd.isnull(
                affect(t+1)[a]) or nb<2)and (pd.isnull(
                affect(t+2)[a]) or nb<3)and(pd.isnull(
                affect(t+3)[a]) or nb<4)):
            if t<=2:
                liste.append(a)
                break
            h=0
            for k in l_m:
                if (affect(t-1)[a]==k.nom or affect(t-2)[a]==k.nom):
                    h=1
            if h==0:
                liste.append(a)

    #if (len(liste) < m.nb_avion - nbmiss and m.opex == 1):
    #    print("pas assez d'avions disponibles", m.nom, m.type_avion)
    return liste

def capaciteMission(a,m): # checks if the capacities required by a mission are satisfied by the airplane
    l2=m.capa_avion
    l1=a.capacite
    if set(l1)<set(l2):
        v=True
    else: v=False
    return v


# creation d'une liste ORDONNEE des avions pouvant accomplir la mision (CRITERE: CRAVATE)
def choixAvion(liste):
    l_cravate = sorted(liste, key=cravate)
    return l_cravate


# Troncature de la liste choixAvions au nombre necessaire d'avions pour la mission m
# ** fontion stockage des affectations à ajouter
def affectationMission(m, listeAvion, nbmiss, data, nb, t,listeMission):
    listeAlpha = besoinEnMission(m,listeMission, listeAvion, nbmiss, data,nb,t)
    listeBeta = choixAvion(listeAlpha)
    listeGamma = listeBeta[0:m.nb_avion - nbmiss]
    for i in range(0, nb):
        data(t + i)[listeGamma] = (m.nom+"$"+str(int(m.pu)))
    #for av in listeGamma:
     #   xyz = av.pot_horaire - nb * m.pu
      #  av.pot_horaire = xyz
    return

def modifPot(m,data,listeAvion,t):
    for a in listeAvion:
        if str(data.xs(t)[a]).split("$")[0] == m.nom:
            a.pot_horaire = a.pot_horaire-int((data.xs(t)[a]).split("$")[1])

def affectMaint(a, t, df, listeMaintenance):
    if t > 1:
        if str(df.xs(t)[a])[0] == "V" and str(df.xs(t - 1)[a])[0] != "V":
            if a.type_avion == "2000_C":
                l_maint = listeMaintenance[0:6]
            if a.type_avion == "2000_D":
                l_maint = listeMaintenance[6:12]
            if a.type_avion == "2000_5":
                l_maint = listeMaintenance[12:18]
            if a.type_avion == "2000_B":
                l_maint = listeMaintenance[18:24]
            for i in range(0, len(l_maint)):
                if a.proch_maint == l_maint[i].nom:
                    a.pot_mois = l_maint[i].gain_mois
                    a.pot_horaire = l_maint[i].gain_heures
                    a.proch_maint = l_maint[(i + 1) % len(l_maint)].nom
                    break
        else:
            if a.type_avion == "2000_C":
                l_maint = listeMaintenance[0:6]
            if a.type_avion == "2000_D":
                l_maint = listeMaintenance[6:12]
            if a.type_avion == "2000_5":
                l_maint = listeMaintenance[12:18]
            if a.type_avion == "2000_B":
                l_maint = listeMaintenance[18:24]
            for i in range(0,len(l_maint)):
                if a.proch_maint == l_maint[i].nom:
                    for j in range(0, int(l_maint[i].duree)):
                        df.xs(t + j)[a] = l_maint[i].nom
                    a.pot_mois = l_maint[i].gain_mois
                    a.pot_horaire = l_maint[i].gain_heures
                    a.proch_maint = l_maint[(i+1)%len(l_maint)].nom
                    break
    if t==1 :
        if str(df.xs(t)[a])[0] == "V":
            if a.type_avion == "2000_C":
                l_maint = listeMaintenance[0:6]
            if a.type_avion == "2000_D":
                l_maint = listeMaintenance[6:12]
            if a.type_avion == "2000_5":
                l_maint = listeMaintenance[12:18]
            if a.type_avion == "2000_B":
                l_maint = listeMaintenance[18:24]
            for i in range(0, len(l_maint)):
                if a.proch_maint == l_maint[i].nom:
                    a.pot_mois = l_maint[i].gain_mois
                    a.pot_horaire = l_maint[i].gain_heures
                    a.proch_maint = l_maint[(i + 1) % len(l_maint)].nom
                    break
        else:
            if a.type_avion == "2000_C":
                l_maint = listeMaintenance[0:6]
            if a.type_avion == "2000_D":
                l_maint = listeMaintenance[6:12]
            if a.type_avion == "2000_5":
                l_maint = listeMaintenance[12:18]
            if a.type_avion == "2000_B":
                l_maint = listeMaintenance[18:24]
            for i in range(0, len(l_maint)):
                if a.proch_maint == l_maint[i].nom:
                    for j in range(0, int(l_maint[i].duree)):
                        df.xs(t + j)[a] = l_maint[i].nom
                    a.pot_mois = l_maint[i].gain_mois
                    a.pot_horaire = l_maint[i].gain_heures
                    a.proch_maint = l_maint[(i + 1) % len(l_maint)].nom
                    break


# Generation d'un nombre aleatoire entre 1 et 10. Fonction à remplacer plus tard
def cravate(a):
    return float(a.pot_mois) / a.pot_horaire

# def attribution_maintenance(listeNAN):
#   for a in listeAvion:
#      if (a.pot_horaire<20 or a.pot_mois<=0):
#         for i in range(0,a.proch_maint.duree):
#            df.xs(t+i)[a] = a.proch_maint

##def listenan(dataframe,t):
#	l_nan= [];
#	for (avion in dataframe)
#		if (data[t,avion]=='Nan')
#			l=l.append(data[t,avion]])
#	return l

# if __name__ == '__main__': algo():
