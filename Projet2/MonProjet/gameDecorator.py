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
        self.orientation = p.orientation()
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

    def plus_proche(self, Lsenseur):
        mini = float("inf")
        s_plus_proche = None
        for senseur in Lsenseur:
            distance = abs(senseur.dist_from_border)
            if distance < mini:
                mini = distance
                s_plus_proche = senseur
        return s_plus_proche
        
        

    

    def est_obstacle(self,senseur):
        return senseur.layer != "joueur"

    def est_advsersaire(self, senseur):
        playerTMP = senseur.sprite
        print(playerTMP)
        if playerTMP is None:
            return False
        if self.est_obstacle(senseur):
            return False
        
        print(playerTMP.numero)
        #if playerTMP.name != self.p.agentType:
        #    return True
        return False

    def detecte_adversaire(self, senseur):
        if self.senseur_detecte_objet(senseur):
            if self.est_advsersaire(senseur):
                return True
        return False

    def adversaire_devant(self):
        for senseur in self.senseurDevant:
            if self.est_advsersaire(senseur):
                return True
        return False

    def get_adversaire_devant(self):
        L = []
        for senseur in self.senseurDevant:
            if self.est_advsersaire(senseur):
              L.append(senseur)
        return L

    def est_suivie(self):
        for senseur in self.senseurArriere:
            if self.est_advsersaire(senseur):
                return True
        return False

    

    
    
