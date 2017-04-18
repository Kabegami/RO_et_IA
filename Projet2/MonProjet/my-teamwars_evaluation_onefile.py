#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multirobot_teamwars.py
# Contact (ce fichier uniquement): nicolas.bredeche(at)upmc.fr
# Ce code utilise pySpriteWorld, développé par Yann Chevaleyre (U. Paris 13)
# 
# Description:
#   Template pour projet multi-robots "MULTIROBOT WARS"
#       But du jeu: posséder le maximum de cases!
#           Chaque joueur dispose de quatre robots
#           Le monde est divisé en 1024 cases (ie. 32x32 cases de 16x16 pixels)
#           Le jeu tourne pendant 4000 itérations
#           Une case "appartient" à la dernière équipe qui l'a visitée
#       Ce que vous avez le droit de faire:
#           Vous ne pouvez modifier que la méthode step(.) de la classe AgentTypeA
#           Les vitesses de translation et rotation maximales sont données par maxTranslationSpeed et maxRotationSpeed
#           La distance maximale autorisée des senseurs est maxSensorDistance
#       Recommandations:
#           Conservez intact multirobot_teamwars.py (travaillez sur une copie!)
#           Pour faire vos tests, vous pouvez aussi modifier (si vous le souhaitez) la méthode step() pour la classe AgentTypeB. Il ne sera pas possible de transmettre cette partie là lors de l'évaluation par contre.
#           La manière dont vous construirez votre fonction step(.) est libre. Par exemple:
#               code écrit à la main, code obtenu par un processus d'apprentissage ou d'optimisation préalable, etc.
#               comportements individuels, collectifs, parasites (p.ex: bloquer l'adversaire), etc.
#       Evaluation:
#           Soutenance devant machine (par binome, 15 min.) lors de la dernière séance de TP (matin et après-midi)
#               Vous devrez montrer votre résultat sur trois arènes inédites
#               Vous devrez mettre en évidence la réutilisation des concepts vus en cours
#               Vous devrez mettre en évidence les choix pragmatiques que vous avez du faire
#               Assurez vous que la simple copie de votre fonctions step(.) dans le fichier multirobots_teamwars.py suffit pour pouvoir le tester
#           Vous affronterez vos camarades
#               Au tableau: une matrice des combats a mettre a jour en fonction des victoires et défaites
#               Affrontement sur les trois arènes inédites
#               vous pouvez utiliser http://piratepad.net pour échanger votre fonction step(.))
#       Bon courage!
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
import time
import sys
import atexit
import math
from gameDecorator import *
from action import *
from condition import *
from subsomption import *


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  variables globales   '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

game = Game()
agents = []

arena = 0

nbAgents = 8 # doit être pair et inférieur a 32
maxSensorDistance = 30              # utilisé localement.
maxRotationSpeed = 5
maxTranslationSpeed = 1
SensorBelt = [-170,-80,-40,-20,+20,40,80,+170]  # angles en degres des senseurs

screen_width=512 #512,768,... -- multiples de 32  
screen_height=512 #512,768,... -- multiples de 32

maxIterations = 6000 # infinite: -1
showSensors = False
frameskip = 4   # 0: no-skip. >1: skip n-1 frames
verbose = True

occupancyGrid = []
for y in range(screen_height/16):
    l = []
    for x in range(screen_width/16):
        l.append("_")
    occupancyGrid.append(l)



'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Agent "A"            '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

class AgentTypeA(object):

    agentIdCounter = 0 # use as static
    id = -1
    robot = -1
    agentType = "A"
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

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-= JOUEUR A -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    teamname = "Equipe Alpha" # A modifier avec le nom de votre équipe

    def step(self):
        color( (255,0,0) )
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
        self.old_rotation = rotation
        self.setRotationValue(rotation)
        self.setTranslationValue(translation)

        return

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
'''  Agent "B"            '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

class AgentTypeB(object):
    
    agentIdCounter = 0 # use as static
    id = -1
    robot = -1
    agentType = "B"


    def __init__(self,robot):
        self.id = AgentTypeB.agentIdCounter
        AgentTypeB.agentIdCounter = AgentTypeB.agentIdCounter + 1
        #print "robot #", self.id, " -- init"
        self.robot = robot
        self.memoireCoord =  []
    def getType(self):
        return self.agentType

    def getRobot(self):
        return self.robot


    teamname = "Equipe Beta" # A modifier avec le nom de votre équipe

    def step(self):
        if(iteration == 0):
            self.previous0X = None
            self.previous1X = None
            self.previous2X = None
            self.revious3X = None
            self.previous4X = None
        if(self.id == 0):
            color((0,0,255))
            posX,posY =self.robot.get_centroid()
        elif (self.id == 1):
            color((0,0, 255))
            posX,posY = self.robot.get_centroid()
        elif (self.id == 2):
            color((0, 0, 255)) #jaune
            posX,posY = srelf.obot.get_centroid()
    elif (self.id == 3):
        color((0, 0, 255))
        posX,posY = self.robot.get_centroid()
    else:
        color((0, 0, 0))
        posX, posY = self.robot.get_centroid()



    circle(*self.getRobot().get_centroid(), r=22)  # je dessine un rond bleu autour de ce robot
    p=self.robot
    sensor_infos = sensors[p]
    previouspos = (0,0)

    if(self.id == 0): # marche tres bien 1 +1 es de base couleur cyan

        params = \
            [0.1172769256085655, 0.027468689602350813, 0.011398372890395775, 0.09341119787122486,
             -0.03754198455716175,
             0.058088366556120624, 0.18351580392027833, 0.3038344530029045, 0.1985654640994996, 0.18491213822979372,
             -0.3834453871545748, -0.1492279440791229, -0.055155905313094424, 0.24432062785033867,
             0.12317275239124321,
             0.12910864054561286, -0.08920806662575052, -0.06759853972855828]

        translation = 0
        rotation = 0

        k = 0

        for i in range(len(SensorBelt)):
            dist = sensor_infos[i].dist_from_border / maxSensorDistance
            translation += dist * params[k]
            k = k + 1

        translation += 1 * params[k]
        k = k + 1

        for i in range(len(SensorBelt)):
            dist = sensor_infos[i].dist_from_border / maxSensorDistance
            rotation += dist * params[k]
            k = k + 1

        rotation += 1 * params[k]
        k = k + 1

        # print "r =",rotation," - t =",translation
        self.r = abs(min(max(rotation, -1), 1))
        self.setRotationValue(min(max(rotation, -1), 1))
        self.setTranslationValue(min(max(translation, -1), 1))

        thisX, thisY = self.robot.get_centroid()

    if (self.id == 1): #IA subsomption normal couleur vert
        joueurdist = list()
        murdist = list()
        for i in range(0, len(sensor_infos)):
            if sensor_infos[i].layer == 'joueur':
                joueurdist.append((i, sensor_infos[i].dist_from_border))
            elif (sensor_infos[i].dist_from_border < 30):
                murdist.append((i, sensor_infos[i].dist_from_border))
        if (len(joueurdist) > 0):
            minDistance = (joueurdist[0])
            for j in range(0, len(joueurdist)):
                if joueurdist[j][1] < minDistance[1]:
                    minDistance = (joueurdist[j])
            if (minDistance[0] == 1 or minDistance[0] == 2 or minDistance[0] == 3):
                p.rotate(1)
            elif (minDistance[0] == 4 or minDistance[0] == 5 or minDistance[0] == 6):
                p.rotate(-1)
        elif (len(murdist) > 0):
            minDistance = (murdist[0])
            for j in range(0, len(murdist)):
                if murdist[j][1] < minDistance[1]:
                    minDistance = (murdist[j])
            if (minDistance[0] == 1 or minDistance[0] == 2 or minDistance[0] == 3):
                p.rotate(1)
            elif (minDistance[0] == 4 or minDistance[0] == 5 or minDistance[0] == 6):
                p.rotate(-1)
        thisX,thisY=self.robot.get_centroid()
        if(self.previous1X != None):
            Vtrans = math.sqrt((thisX - self.previous1X) ** 2 + (thisY - self.previous1Y) ** 2) / maxTranslationSpeed
            if(Vtrans == 0):
                p.rotate(-4)
        p.forward(1)
        self.previous1X = thisX
        self.previous1Y = thisY

    if (self.id == 2): #comportement : longer les murs couleur rouge
        joueurdist = list()
        murdist = list()
        for i in range(0, len(sensor_infos)):
            if sensor_infos[i].layer == 'joueur':
                joueurdist.append((i, sensor_infos[i].dist_from_border))
            elif (sensor_infos[i].dist_from_border < 30):
                murdist.append((i, sensor_infos[i].dist_from_border))
        if (len(joueurdist) > 0):
            minDistance = (joueurdist[0])
            for j in range(0, len(joueurdist)):
                if joueurdist[j][1] < minDistance[1]:
                    minDistance = (joueurdist[j])
            if (minDistance[0] == 1 or minDistance[0] == 2 or minDistance[0] == 3):
                p.rotate(1)
            elif (minDistance[0] == 4 or minDistance[0] == 5 or minDistance[0] == 6):
                p.rotate(-1)
        elif (len(murdist) > 0):
            minDistance = (murdist[0])
            for j in range(0, len(murdist)):
                if murdist[j][1] < minDistance[1]:
                    minDistance = (murdist[j])
            if (minDistance[0] == 3 or minDistance[0] == 4):
                if (minDistance[1] > 5):
                    p.forward(0)
                else:
                    p.rotate(-5)
            elif (minDistance[0] == 1 or minDistance[0] == 2):
                if (minDistance[1] > 5):
                    p.rotate(-5)
                else:
                    p.rotate(5)
            elif (minDistance[0] == 5 or minDistance[0] == 6):
                if (minDistance[1] > 5):
                    p.rotate(5)
                else:
                    p.rotate(-5)

        thisX,thisY=self.robot.get_centroid()
        if (self.previous2X != None):
            Vtrans = math.sqrt((thisX - self.previous2X) ** 2 + (thisY - self.previous2Y) ** 2) / maxTranslationSpeed
            if (Vtrans == 0):
                p.rotate(-2)
        p.forward(1)
        self.previous2X = thisX
        self.previous2Y = thisY
        
        if(iteration > 3000):
            self.id = 1

    if (self.id == 3):

        params = \
            [-0.03680722524074011, -0.31695745843247425, 0.0600528482412522, -0.16416499947717247,
             -0.03066013797849438, -0.14634425143062044, -0.11222421362460736, -0.05054001993692516,
             -0.2022348693322451, 0.3525712909861245, 0.038353152180470494, 0.21528862766699267,
             0.006384996562816884, -0.6478525246324305, 0.22371137471136973, -0.2466541395650095,
             -0.16976954169416375, 0.265709881413874]

        params = \
                    [0.002699745512749375, 0.08057158885496114, 0.20704857359908257, 0.24044810362682134,
                     0.15585078746522926, 0.36653012431036236, 0.07251125564668084, -0.2261649863044871,
                     0.10490887391523035, -0.07726168293440477, -0.2919159103602223, 0.026289825683322356,
                     0.012649256993894764, 0.09380673640333623, 0.2106903551241851, 0.13836537377424174,
                     -0.08936405383922516, -0.1455085276856592]



        translation = 0
        rotation = 0

        k = 0

        for i in range(len(SensorBelt)):
            dist = sensor_infos[i].dist_from_border / maxSensorDistance
            translation += dist * params[k]
            k = k + 1

        translation += 1 * params[k]
        k = k + 1

        for i in range(len(SensorBelt)):
            dist = sensor_infos[i].dist_from_border / maxSensorDistance
            rotation += dist * params[k]
            k = k + 1

        rotation += 1 * params[k]
        k = k + 1

        # print "r =",rotation," - t =",translation
        self.r = abs(min(max(rotation, -1), 1))
        self.setRotationValue(min(max(rotation, -1), 1))
        self.setTranslationValue(min(max(translation, -1), 1))
    return


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def setTranslationValue(self,value):
        if value > 1:
#            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxTranslationSpeed
        elif value < -1:
#            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxTranslationSpeed
        else:
            value = value * maxTranslationSpeed
        self.robot.forward(value)

    def setRotationValue(self,value):
        if value > 1:
#            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = maxRotationSpeed
        elif value < -1:
#            print "[WARNING] translation value not in [-1,+1]. Normalizing."
            value = -maxRotationSpeed
        else:
            value = value * maxRotationSpeed
        self.robot.rotate(value)



    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=



'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Fonctions init/step  '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''


def setupAgents():
    global screen_width, screen_height, nbAgents, agents, game

    # Make agents

    nbAgentsTypeA = nbAgentsTypeB = nbAgents / 2
    nbAgentsCreated = 0

    for i in range(nbAgentsTypeA):
        p = game.add_players( (16 , 200+32*i) , None , tiled=False)
        p.oriente( 0 )
        p.numero = nbAgentsCreated
        nbAgentsCreated = nbAgentsCreated + 1
        agents.append(AgentTypeA(p))

    for i in range(nbAgentsTypeB):
        p = game.add_players( (486 , 200+32*i) , None , tiled=False)
        p.oriente( 180 )
        p.numero = nbAgentsCreated
        nbAgentsCreated = nbAgentsCreated + 1
        agents.append(AgentTypeB(p))

    game.mainiteration()


def setupArena0():
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

def setupArena1():
    return

def setupArena2():
    for i in range(0,8):
        addObstacle(row=i,col=7)
    for i in range(8,16):
        addObstacle(row=i,col=8)

def setupArena3(): # exit the vault
    for i in range(0,5):
        addObstacle(row=11,col=i)
        addObstacle(row=4,col=i)
        addObstacle(row=11,col=11+i)
        addObstacle(row=4,col=11+i)
    for i in range(1,3):
        addObstacle(row=11-i,col=11)
        addObstacle(row=4+i,col=4)
    addObstacle(row=5,col=11)
    addObstacle(row=10,col=4)
    return

def setupArena4(): # corridors
    for i in range(0,15):
        for j in range(2,7,2):
            addObstacle(row=(j/2)%2+i,col=j)
    for i in range(0,15):
        for j in range(9,15,2):
            addObstacle(row=(j/2)%2+i,col=j)
    return

def setupArena5(): # two small passages
    for i in range(0,8):
        if i != 1:
            addObstacle(row=i,col=7)
    for i in range(8,16):
        if i != 14:
            addObstacle(row=i,col=8)

def stepWorld():

    efface()
        
    # chaque agent se met à jour. L'ordre de mise à jour change à chaque fois (permet d'éviter des effets d'ordre).
    shuffledIndexes = [i for i in range(len(agents))]
    shuffle(shuffledIndexes)     ### TODO: erreur sur macosx
    for i in range(len(agents)):
        agents[shuffledIndexes[i]].step()
        # met à jour la grille d'occupation
        coord = agents[shuffledIndexes[i]].getRobot().get_centroid()
        occupancyGrid[int(coord[0])/16][int(coord[1])/16] = agents[shuffledIndexes[i]].getType() # first come, first served
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

def displayOccupancyGrid():
    global iteration
    nbA = nbB = nothing = 0

    for y in range(screen_height/16):
        for x in range(screen_width/16):
            sys.stdout.write(occupancyGrid[x][y])
            if occupancyGrid[x][y] == "A":
                nbA = nbA+1
            elif occupancyGrid[x][y] == "B":
                nbB = nbB+1
            else:
                nothing = nothing + 1
        sys.stdout.write('\n')

    sys.stdout.write('Time left: '+str(maxIterations-iteration)+'\n')
    sys.stdout.write('Summary: \n')
    sys.stdout.write('\tType A: ')
    sys.stdout.write(str(nbA))
    sys.stdout.write('\n')
    sys.stdout.write('\tType B: ')
    sys.stdout.write(str(nbB))
    sys.stdout.write('\n')
    sys.stdout.write('\tFree  : ')
    sys.stdout.write(str(nothing))
    sys.stdout.write('\n')
    sys.stdout.flush() 

    return nbA,nbB,nothing

def onExit():
    ret = displayOccupancyGrid()
    print "\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
    if ret[0] > ret[1]:
        print "Robots type A (\"" + str(AgentTypeA.teamname) + "\") wins!"
    elif ret[0] < ret[1]:
        print "Robots type B (\"" + str(AgentTypeB.teamname) + "\") wins!"
    else: 
        print "Nobody wins!"
    print "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
    print "\n[Simulation::stop]"


'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''
'''  Main loop            '''
'''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''

init('vide3',MyTurtle,screen_width,screen_height) # display is re-dimensioned, turtle acts as a template to create new players/robots
game.auto_refresh = False # display will be updated only if game.mainiteration() is called
game.frameskip = frameskip
atexit.register(onExit)

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) > 1:
    arena = int(sys.argv[1])
    print "Arena: ", str(arena), "(user-selected)"
else:
    print "Arena: ", str(arena), "(default)"

if arena == 0:
    setupArena0()
elif arena == 1:
    setupArena1()
elif arena == 2:
    setupArena2()
elif arena == 3:
    setupArena3()
elif arena == 4:
    setupArena4()
elif arena == 5:
    setupArena5()



setupAgents()
game.mainiteration()

iteration = 0
while iteration != maxIterations:
    # c'est plus rapide d'appeler cette fonction une fois pour toute car elle doit recalculer le masque de collision,
    # ce qui est lourd....
    sensors = throw_rays_for_many_players(game,game.layers['joueur'],SensorBelt,max_radius = maxSensorDistance+game.player.diametre_robot() , show_rays=showSensors)
    stepWorld()
    game.mainiteration()
    if iteration % 200 == 0:
        displayOccupancyGrid()
    iteration = iteration + 1

