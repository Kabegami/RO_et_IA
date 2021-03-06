#/usr/bin/env python
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
nbAgents = 2

maxSensorDistance = 30              # utilisé localement.
maxRotationSpeed = 5
maxTranslationSpeed = 1
SensorBelt = [-170,-80,-40,-20,+20,40,80,+170]  # angles en degres des senseurs

#On reset tout les 200 itérations donc il faut mettre un multiple de 200. ici on a 60 000 = 200 * 300
maxIterations = 60000 # infinite: -1

showSensors = True
frameskip = 200   # 0: no-skip. >1: skip n-1 frames
#frameskip = 0
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
        #on verifie que r n'explose pas en le bornant
        if r < -10:
            r = -10
        if r > 10:
            r = 10

        fils.append(r)
    return fils


def normalise(valeur, mini , maxi):
    if maxi == mini:
        return 0
    n = (valeur - mini) / ((maxi - mini)*1.0)
    return n

def calcule_vitesse(p1,p2):
    if len(p1) != len(p2):
        print("erreur tuple de taille diffentes")
        return None
    a = abs(p2[1] - p1[1]) / (abs(p2[0] - p1[0])*1.0)
    return a

def calcule_vitesseMoyenne(p1,p2):
    if len(p1) != len(p2):
        print("erreur tuple de taille diffentes")
        return None
    distance = (p2[1] - p1[1])**2 + (p2[0] - p1[0])**2
    distance = math.sqrt(distance)
    return distance

def calcule_rotation(a1,a2):
    #Comme le cercle est modulo 360
    if a2 - a1 > 100:
        a1 = a1 + 360
    elif a2 - a1 < -100:
        a2 = a2 + 360
    return abs(a2 - a1)
            

class Agent(object):

    agentIdCounter = 0 # use as static
    id = -1
    robot = -1
    name = "Equipe Kabegami" # A modifier avec le nom de votre équipe
    params = []
    fitness = bestFitness = 0

    def __init__(self,robot):
        self.id = Agent.agentIdCounter
        Agent.agentIdCounter = Agent.agentIdCounter + 1
        self.robot = robot
        self.old_position = robot.position()
        self.old_orientation = robot.orientation()
        self.sigma = 10**(-2)
        self.params = []
        self.best_params = None
        #ici on veut minimiser la fitness
        self.best_fitness = -1*float("inf")
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
        self.stepController()



    def stepSearchMethod(self): 
        if iteration == maxIterations - 1:
            self.affiche_meilleur_resultat()
        if iteration % 400 == 0:

            #si la mutation testé est meilleur
            if self.fitness >= self.best_fitness:
                #c'est une liste donc on fait une copie
                self.best_params = self.params[::]
                self.best_fitness = self.fitness
                self.sigma = 2*self.sigma
            else:
                self.sigma = (2**(-1/4.0))*self.sigma

            # affiche la performance (et les valeurs de parametres)

            print "Fitness:",self.fitness, "(best:", self.best_fitness,")"
            print "Parameters:", str(self.params)

            print "Evaluation no.", int(iteration/200)
            # repositionne le robot
            p = self.robot
            x = screen_width/2
            y = screen_height/2
            rx = randrange(-5,5)
            ry = randrange(-5,5)
            p.set_position(x+rx,y+ry)
            p.oriente( 0 )
            self.old_position = p.position()
            self.old_orientation = p.orientation()
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
        self.g = gameDecorator(self.robot, sensors, maxSensorDistance, maxRotationSpeed)

        translation = 0
        rotation = 0

        minSensorValue = float("inf")
        max_distance = -1 * float("inf")
        #on recupere le minSensor et la distance max pour normaliser
        for i in range(len(SensorBelt)):
            #la distance renvoyer peut être négative
            distance = min(maxSensorDistance, abs(sensor_infos[i].dist_from_border))
            if distance < 0:
                print("distance < 0, dist : {}".format(sensor_infos[i].dist_from_border))
            max_distance = max(max_distance, sensor_infos[i].dist_from_border)
            minSensorValue = min(minSensorValue, distance)


        k = 0
        
        translation += 1 * normalise(self.params[k],-10,10)
        k = k + 1


        for i in range(len(SensorBelt)):
            dist = sensor_infos[i].dist_from_border/maxSensorDistance
            #print("k : {}".format(k))
            translation += dist * normalise(self.params[k], -10 ,10)
            k = k + 1

        rotation += 1 * self.params[k]
        k = k + 1

        for i in range(len(SensorBelt)):
            dist = sensor_infos[i].dist_from_border/maxSensorDistance
            rotation += dist * normalise(self.params[k], -10, 10)
            k = k + 1

        self.setRotationValue(math.tanh(rotation))
        self.setTranslationValue(math.tanh(translation))

        self.vitesse = calcule_vitesseMoyenne(p.position(),self.old_position)
        self.orientation = calcule_rotation(abs(p.orientation()), abs(self.old_orientation))

        self.old_position = p.position()
        self.old_orientation = p.orientation()
        minSensorValue = normalise(minSensorValue, 0, maxSensorDistance)
        #print("orientation precedante : {}".format(p.orientation()))

        self.vitesse = normalise(self.vitesse, 0, maxTranslationSpeed)
        self.orientation = normalise(self.orientation, 0, maxRotationSpeed)
        if self.vitesse * (1 - self.orientation) * minSensorValue < 0:
            print("vitesse : {}, orientation : {}, minSensorValue : {}".format(self.vitesse, self.orientation, minSensorValue))
            print("-------------------------------")
            print("old_orientation : {}".format(old))
            print("new_orientation : {}".format(p.orientation()))
            print("-------------------------------")
        self.fitness += self.vitesse * (1 - self.orientation) * (minSensorValue)
    
        return

    def resetFitness(self):
        self.fitness = 0

    def updateFitness(self):
        p = self.robot
        sensor_info = sensors[p]
        self.fitness += fonction_obj(self.params, sensor_info)
        return self.fitness
        #self.updateFitness()        #self.updateFitness()


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
