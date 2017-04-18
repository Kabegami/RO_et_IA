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

def condition_traqueur(g):
    if g.adversaire_devant():
        #print("appel traqueur")
        return True
    return False

def condition_suivie(g):
    if g.est_suivie():
        L = g.get_adv_derriere()
        senseur = g.plus_proche(L)
        return True
    return False

def condition_adv_imobile(g):
    #print("vitesse adv_plus_proche : ",g.vitesse_adv_plus_proche)
    if g.vitesse_adv_plus_proche is None:
        return False
    #print("vitesse adv_plus_proche : ",g.vitesse_adv_plus_proche)
    if g.vitesse_adv_plus_proche < 0.1:
        #print("appel deserteur")
        return True
    return False
