class gameDecorator(object):
    def __init__(self,p, sensors, maxSensorDistance, maxRotationSpeed):
        self.p = p
        self.sensors = sensors
        self.senseur_info = sensors[p]
        self.distDroite = self.senseur_info[6].dist_from_border
        self.distGauche = self.senseur_info[2].dist_from_border
        self.maxSensorDistance = maxSensorDistance
        self.maxRotationSpeed = maxRotationSpeed

    @property
    def detecte_objet(self):
        for senseur in self.senseur_info:
            if senseur.dist_from_border < self.maxSensorDistance:
                return True
        return False

    @property
    def senseur_actif(self):
        L = []
        for senseur in self.senseur_info:
            if senseur.dist_from_border < self.maxSensorDistance:
                L.append(senseur)
        return L

    def est_obstacle(self,senseur):
        return self.senseur.layer == "joueur"

    

    
    
