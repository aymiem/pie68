import csv
from objects import *
from constantes import *
import pandas as pd

def lecture(pathCSV):
    # le chemin du fichier csv à lire
    source = pathCSV
    nom_fichier = lecture_fichier(source)
    path = nom_fichier[1]
    # Lecture des données de chaque categorie dans le fichier csv
    listeInd=indexCategories(path)
    lecture_l_p = lectureCategorie(path, listeInd, "parametres")
    lecture_l_a = lectureCategorie(path, listeInd, "avion")
    lecture_l_m = lectureCategorie(path, listeInd, "mission")
    lecture_l_mt = lectureCategorie(path, listeInd, "maintenance")

    # creation des objets à partir des données récupérées
    affectationParam(lecture_l_p)    # dates de la simulation et autres paramètres
    l_a=creationListeAvion(lecture_l_a)    # liste des avions
    l_m=creationListeMission(lecture_l_m)   # liste des missions
    l_mt = creationListeMaintenance(lecture_l_mt)   # liste des maintenances

    # Lecture csv de la situation initiale / rebouclage
    df= lectureDF(nom_fichier[2])
    y=df.as_matrix()
    index=df.index
    df1=pd.DataFrame(y,index=index,columns=l_a)


    return [l_a,l_m,l_mt,df1,nom_fichier]

# lectures des indices des différentes catégories du CSV (n de la prmiere et dernire ligne de la catégorie dans le csv)
def indexCategories(path):
    listeIndex=[]
    with open(path) as f:
        reader = f.readlines()
        for line in reader:
           if line[:9] == "categorie" or line[:3]=="fin":
               nb = reader.index(line)
               listeIndex.append(nb)
    return listeIndex

# lectures des différentes catégories du CSV (lecture brute des données)
def lectureCategorie(path,listeIndices,categorie):
    liste1=[]
    with open(path, newline='') as f:
        reader=csv.reader(f,delimiter=';')
        next(reader)
        for row in reader:
           liste1.append(row)
        if categorie=="mission":
            liste2=liste1[listeIndices[2]:listeIndices[3]-1]
        if categorie=="maintenance":
            liste2=liste1[listeIndices[3]:listeIndices[4]-1]
        if categorie=="parametres":
            liste2=liste1[listeIndices[0]:listeIndices[1]-1]
        if categorie=="avion":
            liste2=liste1[listeIndices[1]:listeIndices[2]-1]
    return liste2

# creation de la liste des objets avions
def creationListeAvion(l):
    listeAvion=[]
    for i in l:
        j=len(i)
        listeCapa =[]
        for k in range(7,j):
            if i[k] != '' or i[k] != '0':
                listeCapa.append(i[k])
        listeCapa=list(filter(None, listeCapa))
        listeAvion.append(avion(i[0],i[1],listeCapa,float(i[2]),float(i[3]),float(i[4]),float(i[5]),i[6]))
    return listeAvion

# Creation de la liste des objets maintenances
def creationListeMaintenance(l):
    listeMaintenance=[]
    for i in l:
        listeMaintenance.append(maintenance(i[1],i[2],float(i[4]),float(i[5]),float(i[6]),float(i[7])))
    return listeMaintenance

# Creation de la liste des objets missions
def creationListeMission(l):
    listeMission=[]
    for i in l:
        listeCapa = []
        for k in range(9, len(i)):
            if i[k]!='99'and i[k]!='':
                listeCapa.append(i[k])
        listeCapa = list(filter(None, listeCapa))
        listeMission.append(mission(i[0],int(i[1]),int(i[2]),float(i[3]),float(i[4]),float(i[5]),float(i[6]),i[8],listeCapa,int(i[7])))
    return listeMission

# Creation de l'objet paramètre
def affectationParam(l):
    listeParam=[]
    for i in l:
        listeParam.append(int(i[1]))
    parametre.moisInit = listeParam[0]
    parametre.anInit=listeParam[1]
    parametre.moisFin=listeParam[2]
    parametre.anFin=listeParam[3]
    parametre.puParMois=listeParam[4]
    parametre.stockageTotal=listeParam[5]
    parametre.entreeSTKparMois=listeParam[6]
    parametre.strategie=listeParam[7]
    parametre.anticipMaint=listeParam[8]

# lecture CSV de la situation initiale / rebouclage
def lectureDF(path):
    dataframeInit=pd.read_csv(path,sep=';',header=0,index_col=0,skiprows=[0,1,2,3])
    t=dataframeInit.T
    return t

# lecture fichier qui contient les noms des différents csv
def lecture_fichier(p):
    liste_nom=[]
    with open(p, newline='') as f:
        reader = csv.reader(f,delimiter=';')
        for row in reader:
            liste_nom.append(row[1])
    return liste_nom
