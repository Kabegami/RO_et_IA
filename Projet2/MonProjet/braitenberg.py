#!/usr/bin/env python
# -*- coding: utf-8 -*-
# On fait le comportement attiré par les obstacles

def love_obstacle(p, sensors,maxSensorDistance, maxRotationSpeed):
    senseur_info = sensors[p]
    distDroite = senseur_info[6].dist_from_border
    distGauche = senseur_info[2].dist_from_border
    if distDroite > maxSensorDistance and distGauche > maxSensorDistance:
            #si il ne detecte rien on fait l'action par default (tout droit)
            p.forward(1)
    else:
        #sinon on va vers l'obstacle
        p.forward(1)
            
        if distDroite > distGauche:
            p.rotate(-1*maxRotationSpeed)
        else:
            p.rotate(1*maxRotationSpeed)


def hate_obstacle(p, sensors, maxSensorDistance, maxRotationSpeed):
    senseur_info = sensors[p]
    distDroite = senseur_info[6].dist_from_border
    distGauche = senseur_info[2].dist_from_border
    if distDroite > maxSensorDistance and distGauche > maxSensorDistance:
            #si il ne detecte rien on fait l'action par default (tout droit)
            p.forward(1)
    else:
        #sinon on va vers l'obstacle
        p.forward(1)
            
        if distDroite > distGauche:
            p.rotate(1*maxRotationSpeed)
        else:
            p.rotate(-1*maxRotationSpeed)

def love_players(p,sensors,maxSensorDistance, maxRotationSpeed):
    senseur_info = sensors[p]
    distDroite = senseur_info[6].dist_from_border
    distGauche = senseur_info[2].dist_from_border
    droitePlayer = (senseur_info[6].layer == "joueur")
    gauchePlayer = (senseur_info[2].layer == "joueur")
    if distDroite > maxSensorDistance and distGauche > maxSensorDistance:
            #si il ne detecte rien on fait l'action par default (tout droit)
            p.forward(1)
    else:
        #sinon on va vers l'obstacle
        p.forward(1)
        if droitePlayer:
            if gauchePlayer:
                if distDroite > distGauche :
                    p.rotate(-1*maxRotationSpeed)
                else:
                    p.rotate(1*maxRotationSpeed)
            else:
                p.rotate(-1*maxRotationSpeed)
                
def hate_players(p,sensors,maxSensorDistance, maxRotationSpeed):
    senseur_info = sensors[p]
    distDroite = senseur_info[6].dist_from_border
    distGauche = senseur_info[2].dist_from_border
    droitePlayer = (senseur_info[6].layer == "joueur")
    gauchePlayer = (senseur_info[2].layer == "joueur")
    print("droitePlayer :",droitePlayer)
    if distDroite > maxSensorDistance and distGauche > maxSensorDistance:
            #si il ne detecte rien on fait l'action par default (tout droit)
            p.forward(1)
    else:
        #sinon on va vers l'obstacle
        p.forward(1)
        if droitePlayer:
            if gauchePlayer:
                if distDroite > distGauche :
                    p.rotate(-1*maxRotationSpeed)
                else:
                    p.rotate(1*maxRotationSpeed)
            else:
                p.rotate(-1*maxRotationSpeed)
        if gauchePlayer:
            p.rotate(1*maxRotationSpeed)

# ------------------------------------------------------
#                  FONCTION TEST
# ------------------------------------------------------

def tout_droit(g):
    if not(g.detecte_objet_devant):
        g.p.forward(1)
        return True
    return False
    
def evite(g):
    #si il est trop pres il fait une marche arriere
    if g.distDroite < 10 and g.distGauche < 10:
        return False
    if g.distDroite > g.distGauche:
        g.p.rotate(1*g.maxRotationSpeed)
        g.p.forward(1)
    else:
        g.p.rotate(-1*g.maxRotationSpeed)
        g.p.forward(1)
    return True

# condition

def c_tourne_droite(g):
    if not(g.detecte_objet(g.senseurDevant[1])):
        return False
    if g.distDroite > g.distGauche:
        return False
    # 10 est un epsilon fixé arbirtrairement pour voir quand on est collé à un obstacle
    if g.distDroite < 10:
        return False
    return True

def c_tourne_gauche(g):
    if not(g.detecte_objet(g.senseurDevant[0])):
        return False
    if g.distDroite < g.distGauche:
        return False
    # 10 est un epsilon fixé arbirtrairement pour voir quand on est collé à un obstacle
    if g.distGauche < 10:
        return False
    return True
        

def recule(g):
    g.p.forward(-1)
    return True

# dans la condition on met toujours une fonction qui depend de G ( il faut changer tout droit et recule)
a_tout_droit = Action(1,0, g.detecte_object_devant)
a_tourne_droite = Action(1,1,c_tourne_droite
a_recule = Action(-1,0,True,10)1
