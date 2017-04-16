#coding: utf-8

maxSensorDistance = 30              
maxRotationSpeed = 5
maxTranslationSpeed = 1
SensorBelt = [-170,-80,-40,-20,+20,40,80,+170]  


import random
import math

class Action2(object):
    """ remarque : quand on veut faire reculer le robot, il faut qu'il fasse une suite de deplacement différents, ici ma structure ne me permet pas d'implementer cela, #todo"""
    def __init__(self,action, condition, duree=1):
        """ deplacement : [-1,1], rotation : [-1,1], condition : fonction, duree : int """
        self.action = action
        self.condition = condition
        self.duree = duree
        self.temps = duree

    def effectueAction(self, g, v=False):
        """  Prend un GameDecorator et renvoie True si la fonction est finis False sinon"""
        #if v:
        #    print("L'action {} est effecuté".format(self.nom))
        self.temps -= 1
        t,r = self.action(g)
        # si l'action est finis on réinitalise la durée et on prévient la fonction appellante
        if self.temps == 0:
            self.temps = self.duree
        return ((t,r))

    @property
    def runingAction(self):
        if self.duree != self.temps:
            return True
        return False

def normalise(valeur, mini , maxi):
    if maxi == mini:
        return 0
    n = (valeur - mini) / ((maxi - mini)*1.0)
    return n

def step_Eviteur_obstacle(g):
    params = [3.0152760807777104, -8.830826040768226, -4.099400890339526, 2.765591888837083, -3.5067873607079894, -0.7320160184030771, -9.603175827716496, -1.5717312923526583, -9.110267550441604, -4.762674315012179, -9.983225329587391, 7.216960925658631, -9.829446961001894, -8.169108816906675, 3.606184617345332, 9.978836192713795, -3.751505291904133, 0.22251212407057291]
    translation = 0
    rotation = 0

    p = g.p
    sensor_infos = g.senseur_info
    minSensorValue = float("inf")
    max_distance = -1 * float("inf")
    #on recupere le minSensor et la distance max pour normaliser
    for i in range(len(SensorBelt)):
        distance = min(maxSensorDistance, sensor_infos[i].dist_from_border)
        max_distance = max(max_distance, sensor_infos[i].dist_from_border)
        minSensorValue = min(minSensorValue, distance)
        
        
    k = 0
    #premier biais
    translation += 1 * normalise(params[k],-10,10)
    k = k + 1


    for i in range(len(SensorBelt)):
        dist = sensor_infos[i].dist_from_border/maxSensorDistance
        #print("k : {}".format(k))
        translation += dist * normalise(params[k], -10 ,10)
        k = k + 1

    #deuxieme biais
    rotation += 1 * params[k]
    k = k + 1

    for i in range(len(SensorBelt)):
        dist = sensor_infos[i].dist_from_border/maxSensorDistance
        rotation += dist * normalise(params[k], -10, 10)
        k = k + 1

    return (math.tanh(translation), math.tanh(rotation))
        
def step_tout_droit(g):
    return (1,0)

def step_random(g):
    x = random.randint(-1,1)
    y = random.randint(-1,1)
    return ((x,y))
