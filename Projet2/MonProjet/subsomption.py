# -*- coding: utf-8 -*-

from braitenberg import *
from gameDecorator import *

class Subsomption(object):
    def __init__(self,p, sensors,maxSensorDistance, maxRotationSpeed,ListeAction):
        self.g = gameDecorator(p, sensors,maxSensorDistance, maxRotationSpeed)
        self.ListeAction = ListeAction
        self.actionEnCours = []

    def choisit_action(self):
        for action in self.ListeAction:
            if action(self.g):
                return True
        return False

    @property
    def verif_running_action(self):
        for action in self.ListeAction:
            if action.runingAction:
                return Action
        return None

    def choisit_action2(self):
        a = self.verif_running_action
        if (a is not None):
            if (a.effectueAction(self.g.p)):
                self.actionEnCours.append(a)
            return True
        else:
            for action in self.ListeAction:
                #to do 
                if action.condition:
                    if (action.effectueAction(self.g.p)):
                        self.actionEnCours.append(action)
                    return True
            return False

class Action(object):
    def __init__(self, deplacement, rotation, duree=1):
        self.deplacement = deplacement
        self.rotation = rotation
        self.duree = duree
        self.temps = duree

    def effectueAction(self,p):
        """ renvoie True si la fonction est finis False sinon"""
        self.temps -= 1
        p.rorate(self.rotation)
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
