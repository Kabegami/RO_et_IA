from gameDecorator import *

def condition_Eviteur_obstacle(g):
    if g.detecte_objet:
        return True
    return False

def condition_Tout_droit(g):
    if g.detecte_objet_droit:
        return True
    return False

def condition_random(g):
    if g.vitesse == 0:
        return True
    return False
