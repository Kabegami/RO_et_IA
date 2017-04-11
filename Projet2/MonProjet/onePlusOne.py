#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multirobot.py
# Contact (ce fichier uniquement): nicolas.bredeche(at)upmc.fr
#
# Description:
#   Template pour robotique evolutionniste simple
#   Ce code utilise pySpriteWorld, développé par Yann Chevaleyre (U. Paris 13)
#
# Dépendances:
#   Python 2.x
#   Matplotlib
#   Pygame
#
# Historique:
#   2016-03-28__23:23 - template pour 3i025 (IA&RO, UPMC, licence info)
#
# Aide: code utile
#   - Partie "variables globales"
#   - La méthode "step" de la classe Agent
#   - La fonction setupAgents (permet de placer les robots au début de la simulation)
#   - La fonction setupArena (permet de placer des obstacles au début de la simulation)
#   - il n'est pas conseillé de modifier les autres parties du code.
#

from robosim import *
from random import *
import math
import time
import sys
import atexit
import pickle
from itertools import count
from gameDecorator import *

'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Aide                 '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

#game.setMaxTranslationSpeed(3) # entre -3 et 3
# size of arena:
#   screenw,screenh = taille_terrain()
#   OU: screen_width,screen_height

'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  variables globales   '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

game = Game()

agents = []
screen_width=512 #512,768,... -- multiples de 32
screen_height=512 #512,768,... -- multiples de 32
nbAgents = 1

maxSensorDistance = 30              # utilisé localement.
maxRotationSpeed = 5
maxTranslationSpeed = 3
SensorBelt = [-170,-80,-40,-20,+20,40,80,+170]  # angles en degres des senseurs

#On reset tout les 200 itérations donc il faut mettre un multiple de 200. ici on a 60 000 = 200 * 300
maxIterations = 60000 # infinite: -1

showSensors = True
frameskip = 200   # 0: no-skip. >1: skip n-1 frames
verbose = True

'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Classe Agent/Robot   '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

def mutation_gaussienne(x,sigma=1):
    fils = []
    for gene in x:
        r = gene + gauss(0,1)*sigma
        #on verifie que r n'explose pas
        while r < -10 or r > 10:
            r = gene + gauss(0,1)*sigma
        fils.append(r)
    return fils


def onePlusOne(x,sensor_info, sigma, epsilon):
    #on génère x
    while sigma > epsilon:
        xPrime = []
        for i in range(len(x)):
            r = x[i] + gauss(0,1)*sigma
            xPrime.append(r)
            if f_objectif(xPrime,sensor_info) > f_objectif(x,sensor_info):
                x = xPrime
                sigma = 2*sigma
            else:
                sigma = (2**(-1/4.0))*sigma
    #print("xPrime : {}".format(xPrime))
    return x

def onePlusOne_sigmaFixe(x,sensor_info, sigma):
    #on génère x
    cpt = 0
    while cpt < 25:
        xPrime = []
        for i in range(len(x)):
            #N(mu,sigma) = mu + sigma*N(0,1)
            #N(o,I) = 0 + sigma*N(0,I)
            r = x[i] + gauss(0,1)*sigma

            #print("valeur de r : ", r)
            xPrime.append(r)
        v1 = f_objectif(xPrime, sensor_info)
        v2 = f_objectif(x, sensor_info)
        #print("x prime : {}".format(v1))
        #print("x : {}".format(v2))
        if fonction_obj(xPrime, sensor_info) >= fonction_obj(x, sensor_info):
            #print("x prime est meilleur que x ", xPrime)
            x = xPrime
                #sigma = 2*sigma
            #else:
             #   sigma = (2**(-1/4.0))*sigma
        cpt += 1
    #print("xPrime : {}".format(xPrime))
    return x


def normalise(valeur, mini , maxi):
    if maxi == mini:
        return 0
    n = (valeur - mini) / ((maxi - mini)*1.0)
    return n

def f_objectif(x,sensor_info):
        vt = 0
        vr = 0
        #on parcours les senseurs forward
        minSensorDist = 100000000000000
        maxSensorDist = 0
        minSensorAngle = 10000000000000
        maxSensorAngle = -170
        mini = 1000000000000000000
        for s in sensor_info:
            minSensorAngle = min(minSensorAngle, s.rel_angle_degree)
            maxSensorAngle = max(maxSensorAngle, s.rel_angle_degree)
            distance = min(maxSensorDistance, s.dist_from_border)
            mini = min(mini, distance)
        #si notre est ne bouge pas , on met sa vitesse de translation a 0
        #on ajoute le premier biais
        vt += x[0]
        for id_p in range(len(x)/2):
            for s in sensor_info:
                #print("param : {}".format(x[id_p]))
                #print(type(x[id_p]))
                distance = min(maxSensorDistance, s.dist_from_border)
                si = normalise(distance,0, maxSensorDistance)
                #x = vecteur de poids, si = neurone d'activation entre 0 et 1
                vt += x[id_p]*(si)
        vt = math.tanh(vt)

        #on rajoute le deuxième biais (dans le cas d'un biais le neurone vaut toujours 1)
        vr += x[len(x)/2]
        #on parcours les senseurs rotate
        for id_p in range(len(x)/2+1, len(x)):
            for s in sensor_info:
                si = normalise(s.rel_angle_degree, minSensorAngle, maxSensorAngle)
                vr += x[id_p]*(si)

        vr = math.tanh(vr)
        #on calcule le senseur minimal
        #min sensor distance est sense être compris entre -1 et 1

        mini = normalise(mini,0,maxSensorDistance)
        #print("mini : ",mini)
        #print("minSensorDist : {}".format(mini))
       # print("vt : {}, vr : {}, minSensorDist : {}".format(vt,vr,minSensorDist))
        return (abs(vt)*abs((1-vr))*mini)

def fonction_obj(params, sensor_info):
    #print(params)
    vt = 0
    vr = 0
    minSensorValue = float("inf")
    max_distance = -1 * float("inf")
    for sensor in sensor_info:
        distance = min(maxSensorDistance, sensor.dist_from_border)
        max_distance = max(max_distance, sensor.dist_from_border)
        minSensorValue = min(minSensorValue,distance)

    #premier biais
    vt += params[0]
    index_senseur = 0
    for i in range(1,len(params)/2):
        distance = min(maxSensorDistance, (sensor_info[index_senseur]).dist_from_border)
        #la distance est entre [0,maxSensorDistance] donc on normalise
        si = distance / (1.0 * max_distance)
        vt += si * params[i]
        index_senseur += 1

    #deuxieme biais
    vr += params[len(params)/2]
    #on reparcours les senseur pour les angles
    index_senseur = 0
    for i in range(len(params)/2 + 1, len(params)):
        #si = (sensor_info[index_senseur].rel_angle_degree + 170) / ((170 + 170)*1.0)
        si = min(maxSensorDistance, (sensor_info[index_senseur]).dist_from_border)
        si = distance / (1.0 * max_distance)
        vr += si*params[i]
        index_senseur += 1

    #on applique les fonction
    vr = math.tanh(vr)
    vt = math.tanh(vt)
    return (abs(vt)*abs(1-vr)*minSensorValue)






class Agent(object):

    agentIdCounter = 0 # use as static
    id = -1
    robot = -1
    name = "Equipe Evol" # A modifier avec le nom de votre équipe
    params = []
    fitness = bestFitness = 0

    def __init__(self,robot):
        self.id = Agent.agentIdCounter
        Agent.agentIdCounter = Agent.agentIdCounter + 1
        #print "robot #", self.id, " -- init"
        self.robot = robot
        self.oldPos = None
        self.sigma = 10**(-1)
        self.params = []
        self.best_params = None
        self.best_fitness = -1*float("inf")
        #Penser a gérer les biais
        self.nbParam = len(SensorBelt)*2+2
        #on génère x
        for i in range(self.nbParam):
            r = randrange(-10,10)
            self.params.append(r)

    def genere_params(self):
        self.params = []
        #on génère x
        for i in range(self.nbParam):
            r = randrange(-10,10)
            self.params.append(r)

    def getRobot(self):
        return self.robot

    def stoque_resultat(self):
        pickle.dump(self.bestParam[-1],file("test.pickle","w"))

    def affiche_meilleur_resultat(self):
        print("meilleur resultat : {}".format(self.best_params))


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def step(self):

        self.stepSearchMethod()
        #self.params = onePlusOne_sigmaFixe(self.params, sensors[self.robot], 10**(-2))
        #print("params : ", self.params)
        #print(self.params)
        self.updateFitness()
        self.stepController()



    def stepSearchMethod(self): # random search
        if iteration == maxIterations:
            self.affiche_meilleur_resultat()
        if iteration % 400 == 0:

            #si la mutation testé est meilleur
            if self.fitness >= self.best_fitness:
                self.best_params = self.params
                self.best_fitness = self.fitness

            # affiche la performance (et les valeurs de parametres)

            print "Fitness:",self.fitness, "(best:", self.best_fitness,")"
            print "Parameters:", str(self.params)

            print "Evaluation no.", int(iteration/200)
            # repositionne le robot
            p = self.robot
            x = screen_width/2
            y = screen_height/2
            rx = randrange(-10,10)
            ry = randrange(-10,10)
            p.set_position(x+rx,y+ry)
            p.oriente( 0 )
            #self.genere_params()

            # remet la fitness à zéro
            self.resetFitness()
            #on test une nouvelle mutation
            self.params = mutation_gaussienne(self.best_params, self.sigma)


    def stepController(self):

        #self.updateFitness()

        #print "robot #", self.id, " -- step"
        p = self.robot
        sensor_infos = sensors[p]

        translation = 0
        rotation = 0

        k = 0

        for i in range(len(SensorBelt)):
            dist = sensor_infos[i].dist_from_border/maxSensorDistance
            #print("k : {}".format(k))
            translation += dist * self.params[k]
            k = k + 1

        translation += 1 * self.params[k]
        k = k + 1

        for i in range(len(SensorBelt)):
            dist = sensor_infos[i].dist_from_border/maxSensorDistance
            rotation += dist * self.params[k]
            k = k + 1

        rotation += 1 * self.params[k]
        k = k + 1

        #print "r =",rotation," - t =",translation

        self.setRotationValue( min(max(rotation,-1),1) )
        self.setTranslationValue( min(max(translation,-1),1) )

        return

    def resetFitness(self):
        self.fitness = 0

    def updateFitness(self):
        p = self.robot
        sensor_info = sensors[p]
        self.fitness += fonction_obj(self.params, sensor_info)
        return self.fitness



        #self.fitness += math.sqrt(abs(currentPos[0]**2-(screen_width/2)**2)) + math.sqrt(abs(currentPos[1]**2-(screen_height/2)**2))

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


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Fonctions init/step  '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

def setupAgents():
    global screen_width, screen_height, nbAgents, agents, game

    # Make agents
    nbAgentsCreated = 0
    for i in range(nbAgents):
        while True:
            p = -1
            while p == -1: # p renvoi -1 s'il n'est pas possible de placer le robot ici (obstacle)
                p = game.add_players( (random()*screen_width , random()*screen_height) , None , tiled=False)
            if p:
                p.oriente( random()*360 )
                p.numero = nbAgentsCreated
                nbAgentsCreated = nbAgentsCreated + 1
                agents.append(Agent(p))
                break
    game.mainiteration()


def setupArena():
    for i in range(6,13):
        addObstacle(row=3,col=i)
    for i in range(3,10):
        addObstacle(row=12,col=i)
    addObstacle(row=4,col=12)
    addObstacle(row=5,col=12)
    addObstacle(row=6,col=12)
    addObstacle(row=11,col=3)
    addObstacle(row=10,col=3)
    addObstacle(row=9,col=3)



def stepWorld():
    # chaque agent se met à jour. L'ordre de mise à jour change à chaque fois (permet d'éviter des effets d'ordre).
    shuffledIndexes = [i for i in range(len(agents))]
    shuffle(shuffledIndexes)     ### TODO: erreur sur macosx
    for i in range(len(agents)):
        agents[shuffledIndexes[i]].step()
    return


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Fonctions internes   '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

def addObstacle(row,col):
    # le sprite situe colone 13, ligne 0 sur le spritesheet
    game.add_new_sprite('obstacle',tileid=(0,13),xy=(col,row),tiled=True)

class MyTurtle(Turtle): # also: limit robot speed through this derived class
    maxRotationSpeed = maxRotationSpeed # 10, 10000, etc.
    def rotate(self,a):
        mx = MyTurtle.maxRotationSpeed
        Turtle.rotate(self, max(-mx,min(a,mx)))
def onExit():
    print "\n[Terminated]"

'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Main loop            '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

init('vide3',MyTurtle,screen_width,screen_height) # display is re-dimensioned, turtle acts as a template to create new players/robots
game.auto_refresh = False # display will be updated only if game.mainiteration() is called
game.frameskip = frameskip
atexit.register(onExit)

setupArena()
setupAgents()
game.mainiteration()

iteration = 0
while iteration != maxIterations:
    # c'est plus rapide d'appeler cette fonction une fois pour toute car elle doit recalculer le masque de collision,
    # ce qui est lourd....
    sensors = throw_rays_for_many_players(game,game.layers['joueur'],SensorBelt,max_radius = maxSensorDistance+game.player.diametre_robot() , show_rays=showSensors)
    stepWorld()
    game.mainiteration()
    iteration = iteration + 1
