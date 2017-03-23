# -*- coding: utf-8 -*-

class gameDecorator(object):
    def __init__(self, p, sensors, maxSensorDistance, maxRotationSpeed):
        self.p = p
        self.sensors = sensors
        self.senseur_info = sensors[p]
        self.distDroite = self.senseur_info[4].dist_from_border
        self.distGauche = self.senseur_info[3].dist_from_border
        self.gauche = self.senseur_info[0:4]
        self.droite = self.senseur_info[3:8]
        self.senseurAvant = self.senseur_info[2:6]
        self.senseurArriere = self.senseur_info[0] + self.senseur_info[7]
        self.senseurCote =self.senseur_info[1] + self.senseur_info[6]
        self.senseurDevant = self.senseur_info[3] + self.senseur_info[4]
        self.maxSensorDistance = maxSensorDistance
        self.maxRotationSpeed = maxRotationSpeed

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
        if senseur.dist_from_border > self.maxSensorDistance:
            return True
        return False

    def liste_senseur_detecte_objet(self,Lsenseur):
        for senseur in Lsenseur:
            if self.senseur_detecte_objet(senseur):
                return True
        return False
        

    

    def est_obstacle(self,senseur):
        return self.senseur.layer != "joueur"

    

    
    
