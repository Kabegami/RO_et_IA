from braitenberg import *
from gameDecorator import *

class Subsomption(object):
    def __init__(self,p, sensors,maxSensorDistance, maxRotationSpeed,ListeAction):
        self.g = gameDecorator(p, sensors,maxSensorDistance, maxRotationSpeed)
        self.ListeAction = ListeAction

    def choisit_action(self):
        for action in self.ListeAction:
            if action(self.g):
                return True
        return False
        
        
