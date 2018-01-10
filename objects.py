class avion:
    def __init__(self,nom, type_avion, capacite,
                 pot_mois, pot_horaire, atterissage,heures_absolues,proch_maint):
        self.nom=nom
        self.type_avion=type_avion
        self.capacite=capacite
        self.pot_mois=pot_mois
        self.pot_horaire=pot_horaire
        self.atterissage=atterissage
        self.heures_absolues=heures_absolues
        self.proch_maint=proch_maint
    def __str__(self):
        return self.nom

class type_avion:
    def __init__(self):
        pass

class maintenance:
    def __init__(self, nom, type_avion, duree, gain_mois, gain_heures, gain_stock):
        self.nom=nom
        self.type_avion=type_avion
        self.duree=duree
        self.gain_mois=gain_mois
        self.gain_heures=gain_heures
        self.gain_stock=gain_stock

class mission:
    def __init__(self,nom,opex,mois_debut,annee_debut,
                 mois_fin,annee_fin,pu,type_avion,capa_avion,nb_avion):
        self.nom=nom
        self.opex=opex
        self.mois_debut=mois_debut
        self.mois_fin=mois_fin
        self.annee_debut=annee_debut
        self.annee_fin=annee_fin
        self.pu=pu
        self.capa_avion=capa_avion
        self.nb_avion=nb_avion
        self.type_avion=type_avion

    def __str__(self):
        return self.nom

""" classes non utilisées
class ressource:
    def __init__(self,nom,capa_indus_mois,capa_indus_an,*args):
        self.nom=nom
        self.capa_indus_an=capa_indus_an
        self.capa_indus_mois=capa_indus_mois
        self.args=args

class stock:
    def __init__(self,stock_max,stock_min,capa_stock_mois):
        self.stock_max=stock_max
        self.stock_min=stock_min
        self.capa_stock_mois=capa_stock_mois

class interdiction:
    def __init__(self):
        pass
"""
