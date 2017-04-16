# -*- coding: utf-8 -*-
import math

def calcule_vitesseMoyenne(p1,p2):
    if len(p1) != len(p2):
        print("erreur tuple de taille diffentes")
        return None
    distance = (p2[1] - p1[1])**2 + (p2[0] - p1[0])**2
    distance = math.sqrt(distance)
    return distance

class gameDecorator(object):
    def __init__(self, p, sensors, maxSensorDistance, old_position=None):
        self.p = p
        self.sensors = sensors
        self.senseur_info = sensors[p]
        self.distDroite = self.senseur_info[4].dist_from_border
        self.distGauche = self.senseur_info[3].dist_from_border
        self.gauche = self.senseur_info[0:4]
        self.droite = self.senseur_info[3:8]
        self.senseurAvant = self.senseur_info[2:6]
        #senseur arriere
        self.senseurArriere = []
        self.senseurArriere.append(self.senseur_info[0])
        self.senseurArriere.append(self.senseur_info[7])
        #senseur latéraux
        self.senseurCote = []
        self.senseurCote.append(self.senseur_info[1])
        self.senseurCote.append(self.senseur_info[6])
        #senseur directement devant
        self.senseurDevant = []
        self.senseurDevant.append(self.senseur_info[3])
        self.senseurDevant.append(self.senseur_info[4])
        self.maxSensorDistance = maxSensorDistance
        #position du robot
        self.position = p.position()
        if old_position != None:
            self.vitesse = calcule_vitesseMoyenne(self.position, old_position)
        else:
            self.vitesse = 1

    @property
    def detecte_objet(self):
        for senseur in self.senseur_info:
            if senseur.dist_from_border < self.maxSensorDistance:
                return True
        return False

    @property
    def detecte_objet_devant(self):
        return self.liste_senseur_detecte_objet(self.senseurAvant)

    @property
    def detecte_objet_droit(self):
        Lsenseur = [self.gauche[-1], self.droite[0]]
        return self.liste_senseur_detecte_objet(Lsenseur)

    @property
    def senseur_actif(self):
        L = []
        for senseur in self.senseur_info:
            if senseur.dist_from_border < self.maxSensorDistance:
                L.append(senseur)
        return L

    def senseur_detecte_objet(self, senseur):
        #print("senseur : ",self.senseurDevant)
        if senseur.dist_from_border > self.maxSensorDistance:
            return True
        return False

    def liste_senseur_detecte_objet(self,Lsenseur):
        for senseur in Lsenseur:
            if self.senseur_detecte_objet(senseur):
                return True
        return False
        

    

    def est_obstacle(self,senseur):
        return senseur.layer != "joueur"

    def est_advsersaire(self, senseur):
        playerTMP = senseur.sprite
        if playerTMP.name != self.p.name:
            return True
        return False

    def detecte_adversaire(self, senseur):
        if self.senseur_detecte_objet(senseur):
            if self.est_advsersaire(senseur):
                return True
        return False

    

    
    
