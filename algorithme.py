import pandas as pd

# creation d'une liste des avions pouvant accomplir la mision
def besoinEnMission(m,l_m, l_a, nbmiss, affect,nb,t,i):
    liste = []
    for a in l_a:
        #nb mois * potdemandé/mois + 100 à la place des 600 (demande DGA)
        if (m.opex == i and m.type_avion == a.type_avion and capaciteMission(a,m)
            and a.pot_horaire >=(nb*m.pu+100)  and isFree(a,t,nb,affect) and isFree(a,t,-2,affect)):
            if t<=2:
                liste.append(a)
                break
            h=0
            for k in l_m:
                if (affect(t-1)[a]==k.nom or affect(t-2)[a]==k.nom):
                    h=1
            if h==0:
                liste.append(a)
    return liste
# fonction pour verifier si les capacites necessaires pour la mission sont satisfaites par l'avion
# set(a)<set(b) permet  verifier si tt element de la liste a est dans la liste b
def capaciteMission(a,m):
    l2=m.capa_avion
    l1=a.capacite
    return set(l2)<=set(l1)

# creation d'une liste ordonnée des avions pouvant accomplir la mision (CRITERE: CRAVATE)
def choixAvion(liste):
    l_cravate = sorted(liste, key=cravate)
    return l_cravate


# Troncature de la liste choixAvions au nombre necessaire d'avions pour la mission m
# puis affectation des missions dans le dataframe sous le format (nom_mission$pot_utilisé)
# la modification du potentiel de l'avion est ralisé avec la fonction modifPot.
def affectationMission(m, listeAvion, nbmiss, data, nb, t,listeMission,i):
    listeAlpha = besoinEnMission(m,listeMission, listeAvion, nbmiss, data,nb,t,i)
    listeBeta = choixAvion(listeAlpha)
    listeGamma = listeBeta[0:m.nb_avion - nbmiss]
    for i in range(0, nb):
        data(t + i)[listeGamma] = (m.nom+"$"+str(int(m.pu)))
    return

# la modification des potentiels s'effectue separement de l'affectation (pour prendre en compte le rebouclage)
# la fonction modifPot permet de modifier le pot. Elle enlève du potentiel la valeur indiquée dans la cellule
# correspandate dans le dataframe.
def modifPot(m,data,a,t, indic):
    #for a in listeAvion:
    if str(data.xs(t)[a]).split("$")[0] == m.nom:
        a.pot_horaire -= int((data.xs(t)[a]).split("$")[1])
        a.pot_mois -= 1
        indic["nbrAvionMission"][t-1] += 1 
            #if (a.nom)=='D602':
            #    print(a.nom,"", a.pot_horaire," ",t, " ")

def listeMaint(listeMaintenance,a): # renvoie la liste des maintenances correspondantes à l'avion
    if a.type_avion == "2000_C":
        l_maint = listeMaintenance[0:6]
    if a.type_avion == "2000_D":
        l_maint = listeMaintenance[6:12]
    if a.type_avion == "2000_5":
        l_maint = listeMaintenance[12:18]
    if a.type_avion == "2000_B":
        l_maint = listeMaintenance[18:24]
    return l_maint

def affectMaint(a, t, df, listeMaintenance):
    if t > 1:
        if str(df.xs(t)[a])[0] == "V" and str(df.xs(t - 1)[a])[0] != "V": # maintenance à la main
            l_maint=listeMaint(listeMaintenance, a)
            for i in range(0, len(l_maint)):
                if a.proch_maint == l_maint[i].nom:
                    a.pot_mois = l_maint[i].gain_mois
                    a.pot_horaire = l_maint[i].gain_heures
                    a.proch_maint = l_maint[(i + 1) % len(l_maint)].nom
                    break
        else:  # maintenance programmé par l'algorithme
            l_maint=listeMaint(listeMaintenance, a)
            for i in range(0,len(l_maint)):
                if a.proch_maint == l_maint[i].nom:
                    for j in range(0, int(l_maint[i].duree)):
                        df.xs(t + j)[a] = l_maint[i].nom
                    a.pot_mois = l_maint[i].gain_mois
                    a.pot_horaire = l_maint[i].gain_heures
                    a.proch_maint = l_maint[(i+1)%len(l_maint)].nom
                    break
    if t==1 :
        if str(df.xs(t)[a])[0] == "V": # maintenance à la main
            l_maint=listeMaint(listeMaintenance, a)
            for i in range(0, len(l_maint)):
                if a.proch_maint == l_maint[i].nom:
                    a.pot_mois = l_maint[i].gain_mois
                    a.pot_horaire = l_maint[i].gain_heures
                    a.proch_maint = l_maint[(i + 1) % len(l_maint)].nom
                    break
        else: # maintenance programmé par l'algorithme
            l_maint=listeMaint(listeMaintenance, a)
            for i in range(0, len(l_maint)):
                if a.proch_maint == l_maint[i].nom:
                    for j in range(0, int(l_maint[i].duree)):
                        df.xs(t + j)[a] = l_maint[i].nom
                    a.pot_mois = l_maint[i].gain_mois
                    a.pot_horaire = l_maint[i].gain_heures
                    a.proch_maint = l_maint[(i + 1) % len(l_maint)].nom
                    break

# pour un avion donnée a, la fonction calcule le rapport entre les potentiels calendaire et horaire.
def cravate(a):
    return float(a.pot_mois) / a.pot_horaire


def lissage(d): # fonction qui envoie en sortie la liste des avions classés par potentiel calendaire croissant
    # fonction utilisée lors de l'affectation en maintenance et non en mission. Elle ne remplace pas la cravate
    liste = sorted(d["listeAvion"], key=lambda avion: avion.pot_mois)
    return liste

# Cette fonction vérifié si les cellules de la matrice entre [t][a] et [t+n][a] sont vides, n peut etre négatif
def isFree(a,t,n,df):
    b=True
    j = max(t,t+n)
    k = min(t,t+n) if t>abs(n) else 1
    for i in range(k,j+1):
        b=b*pd.isnull(df(i)[a])
    return b
