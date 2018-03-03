import os

class constantes:
    path = 'donnees_lecture.csv'
    strategie_cravate = 1
    strategie_lissage = 2
    typechoix = 1

class parametre:
    # initialisation des parametres du programme
    # les valeurs seront ensuite modifié avec la fonction affectationParam dans lecture.py
    moisInit = 0
    anInit = 0
    moisFin = 0
    anFin = 0
    puParMois = 0
    stockageTotal = 0
    entreeSTKparMois = 0
    strategie = 0
    anticipMaint = 0
    
class paths:
    solutions_path = os.getcwd() + "\solutions\ ".replace(" ","")
    indicateurs_path = os.getcwd() + "\indicateurs\ ".replace(" ","")
    solutions_final_path = os.getcwd() + "\solutions_final\ ".replace(" ","")
    indicateurs_final_path = os.getcwd() + "\indicateurs_final\ ".replace(" ","")
    sitInits_path = os.getcwd() + "\sitInits\ ".replace(" ","")    