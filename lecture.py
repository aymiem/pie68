import csv
from objects import *
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
    param_init=affectationParam(lecture_l_p)    # dates de la simulation ****Done****
    l_a=creationListeAvion(lecture_l_a)    # liste des avions ****Done****
    l_m=creationListeMission(lecture_l_m)   # liste des missions ****Done****
    l_mt = creationListeMaintenance(lecture_l_mt)   # liste des maintenances
    for a in l_a:
        print(a.nom,a.capacite)
    for m in l_m:
        print(m.nom, m.capa_avion)
    df= lectureDF(l_a,nom_fichier[2])
    #print(df.index)
    y=df.as_matrix()
    #y[0][0]='valeur'
    #print(type(y))
    index=df.index
    df1=pd.DataFrame(y,index=index,columns=l_a)
    #print(type(df1.columns[0]))
    #print(df1)
    capaciteMission(l_a[0],l_m[0])

    return [l_a,l_m,l_mt,param_init,df1,nom_fichier]

def indexCategories(path):
    listeIndex=[]
    with open(path) as f:
        reader = f.readlines()
        for line in reader:
           if line[:9] == "categorie" or line[:3]=="fin":
               nb = reader.index(line)
               listeIndex.append(nb)
    return listeIndex

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

def creationListeAvion(l):
    #bonjour
    listeAvion=[]
    for i in l:
        j=len(i)
        listeCapa =[]
        for k in range(8,j):
            if i[k] != '':
                listeCapa.append(i[k])
        listeAvion.append(avion(i[0],i[1],listeCapa,float(i[2]),float(i[3]),float(i[4]),float(i[5]),i[6]))
    return listeAvion

def creationListeMaintenance(l):
    listeMaintenance=[]
    for i in l:
        listeMaintenance.append(maintenance(i[1],i[2],float(i[4]),float(i[5]),float(i[6]),float(i[7])))
    return listeMaintenance

def creationListeMission(l):
    listeMission=[]
    for i in l:
        listeCapa = []
        for k in range(9, len(i)):
            if i[k]!='99':
                listeCapa.append(i[k])
        listeMission.append(mission(i[0],int(i[1]),int(i[2]),float(i[3]),float(i[4]),float(i[5]),float(i[6]),i[8],listeCapa,int(i[7])))
    return listeMission
def affectationParam(l):

    listeParam=[]
    for i in l:
        listeParam.append(i[1])
    p=parametre(int(listeParam[0]),int(listeParam[1]),int(listeParam[2]),int(listeParam[3]))
    return p

def lectureDF(l,s):
    path=s
    dataframeInit=pd.read_csv(path,sep=';',header=0,index_col=0,skiprows=[0,1,2,3])
    t=dataframeInit.T
    return t
def capaciteMission(a,m): # checks if the capacities required by a mission are satisfied by the airplane
    l2=m.capa_avion
    l1=a.capacite
    if set(l1)<set(l2):
        v=True
    else: v=False
    print(v)

def lecture_fichier(p):
    liste_nom=[]
    with open('donnees_lecture.csv', newline='') as f:
        reader = csv.reader(f,delimiter=';')
        for row in reader:
            liste_nom.append(row[1])
    return liste_nom

if __name__ == '__main__':lecture('donnees_lecture.csv')
