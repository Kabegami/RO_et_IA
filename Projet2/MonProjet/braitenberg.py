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
    distDroite = senseur_info[6].di
    st_from_border
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
# les conditions dépendent toujours de g

def c_tout_droit(g):
    if not(g.detecte_objet_devant):
        return True
    return False

def c_recule(g):
    print("distance droite : {}, distance gauche {}".format(g.distDroite,g.distGauche))
    if g.distDroite < 10 or g.distGauche < 10:
        return True
    return False

def c_tourne_droite(g):
    if not(g.senseur_detecte_objet(g.senseurDevant[1])):
        return False
    if g.distDroite < g.distGauche:
        return False
    return True

def c_tourne_gauche(g):
    if not(g.senseur_detecte_objet(g.senseurDevant[0])):
        return False
    if g.distDroite > g.distGauche:
        return False
    # 10 est un epsilon fixé arbirtrairement pour voir quand on est collé à un obstacle
    return True

def par_defaut(g):
    return True

def recule(g):
    g.p.forward(-1)
    return True


    
