#!/usr/bin/env python
# -*- coding: utf-8 -*-

from robosim import *
from random import random, shuffle
import time
import sys
import atexit
import math
from gameDecorator import *
from action import *
from condition import *
from subsomption import *


class AgentTypeA(object):
    
    agentIdCounter = 0 # use as static
    id = -1
    robot = -1
    agentType = "A"
    #Pour savoir si un robot est equipier ou non on est obliger de garder une liste des equipier
    liste_equipier = []

    def __init__(self,robot):
        self.id = AgentTypeA.agentIdCounter
        AgentTypeA.agentIdCounter = AgentTypeA.agentIdCounter + 1
        #print "robot #", self.id, " -- init"
        self.robot = robot
        self.old_position = None
        AgentTypeA.liste_equipier.append(robot)
        #Mon robot ce comporte bizarement avec le random , il faut peut être le lancer plus longtemps avant de le lancer car des fois il fait random au lieu d'éviteur d'obstacle.
        #Idée comparer la valeur de rotation / translation donnée et la vitesse pour voir si l'action a pu être réaliser correctement
        random = Action2(step_random, condition_random)
        eviteur_obstacle = Action2(step_Eviteur_obstacle, condition_Eviteur_obstacle)
        tout_droit = Action2(step_tout_droit, condition_Tout_droit)
        traqueur = Action2(step_traqueur, condition_traqueur)
        tortue = Action2(step_suivie, condition_suivie)
        deserteur = Action2(step_Eviteur_obstacle, condition_adv_imobile, 20)
        ListeAction = [deserteur, tortue, random, traqueur, eviteur_obstacle, tout_droit]
        self.subsomption = Subsomption(ListeAction)
        self.old_position_adv_plus_proche = None
        self.vitesse_adv_plus_proche = None


        
    def getType(self):
        return self.agentType

    def getRobot(self):
        return self.robot

    def normalise(self, valeur, mini , maxi):
        if maxi == mini:
            return 0
        n = (valeur - mini) / ((maxi - mini)*1.0)
        return n

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-= JOUEUR A -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    teamname = "Equipe Lucas" # A modifier avec le nom de votre équipe

    def step(self):

        color( (0,255,0) )
        circle( *self.getRobot().get_centroid() , r = 22) # je dessine un rond bleu autour de ce robot

        #print "robot #", self.id, " -- step"
        p = self.robot
        sensor_infos = sensors[p]

        g = gameDecorator(p, sensors, maxSensorDistance, AgentTypeA.liste_equipier, self.old_position, self.old_position_adv_plus_proche, self.vitesse_adv_plus_proche)
        self.old_position = p.position()
        translation, rotation = self.subsomption.choisit_action(g)
        if g.adversaire_devant():
            self.old_position_adv_plus_proche = g.old_position_adv_plus_proche
            self.vitesse_adv_plus_proche = g.vitesse_adv_plus_proche
        else:
            self.old_position_adv_plus_proche = None
            self.vitesse_adv_plus_proche = None

        self.old_translation = translation
        self.old_rotation = translation
        self.setRotationValue(rotation)
        self.setTranslationValue(translation)

        return

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def setTranslationValue(self,value):
        if value > 1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxTranslationSpeed
        elif value < -1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxTranslationSpeed
        else:
            value = value * maxTranslationSpeed
        self.robot.forward(value)

    def setRotationValue(self,value):
        if value > 1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxRotationSpeed
        elif value < -1:
            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxRotationSpeed
        else:
            value = value * maxRotationSpeed
        self.robot.rotate(value)


