# -*- coding: utf-8 -*-

from braitenberg import *
from gameDecorator import *

class Subsomption(object):
    def __init__(self,ListeAction):
        self.ListeAction = ListeAction
        self.actionEnCours = []
                
    @property
    def verif_running_action(self):
        for action in self.ListeAction:
            if action.runingAction:
                return action
        return None

    def choisit_action(self,p,sensors,maxSensorDistance, maxRotationSpeed):
        self.g = gameDecorator(p, sensors,maxSensorDistance, maxRotationSpeed)
        # si il y a une action en cours
        if self.actionEnCours != []:
            print("il y a une action en cours")
            a = self.actionEnCours[0]
            a.effectueAction(self.g.p,True)
            #si l'action est finis on la supprime de action en cours
            if not(a.runingAction):
                print("l'action est supprimé")
                self.actionEnCours.remove(a)
            return True
        else:
            for action in self.ListeAction:
                #to do 
                if action.condition(self.g):
                    action.effectueAction(self.g.p, True)
                    if action.runingAction:
                        self.actionEnCours.append(action)
                    return True
            return False

class Action(object):
    """ remarque : quand on veut faire reculer le robot, il faut qu'il fasse une suite de deplacement différents, ici ma structure ne me permet pas d'implementer cela, #todo"""
    def __init__(self, nom,deplacement, rotation, condition, duree=1):
        """ deplacement : [-1,1], rotation : [-1,1], condition : fonction, duree : int """
        self.nom = nom
        self.deplacement = deplacement
        self.rotation = rotation
        self.condition = condition
        self.duree = duree
        self.temps = duree

    def effectueAction(self, p, v=False):
        """ renvoie True si la fonction est finis False sinon"""
        if v:
            print("L'action {} est effecuté".format(self.nom))
        self.temps -= 1
        p.rotate(self.rotation)
        p.forward(self.deplacement)
        # si l'action est finis on réinitalise la durée et on prévient la fonction appellante
        if self.temps == 0:
            self.temps = self.duree
            return True
        return False

    @property
    def runingAction(self):
        if self.duree != self.temps:
            return True
        return False
        
class ArbreComportement(object):
    def __init__(self, typeNoeud, fg, fd):
        self.typeNoeud = typeNoeud
        self.fg = fg
        self.fd = fd

