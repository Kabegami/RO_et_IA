# -*- coding: utf-8 -*-

from Astar import *
import random


# -----------------------------------------------------------------------------------

def choisit_couleur_pref(fioles):
    """ Prend un dictionnaire de fiole en entrée et retourne un tuple avec les couleurs par ordre de préférance et 
    un dictionnaire avec la récompense associé à chaque fioles """
    color = ["r","j","b"]
    random.shuffle(color)
    dico = {}
    for f in fioles:
        if fioles[f] == color[0]:            
            dico[f] = 10
        elif fioles[f] == color[1]:
            dico[f] = 7
        else:
            dico[f] = 2
    return (color, dico)


# -------------------------------------------------------------------------------------
#                        ESPACE DEDIE AU STRATEGIE
#-------------------------------------------------------------------------------------

#remarque : les strategies retournes un tuple (row, col) correspondant au prochain coup a jouer


def strategie_naive(dicoValFioles, positionJoueur, wallStates):
    """ Chaque fiole a une valeur : valFiole - distFiole et on prend la fiole avec la plus grande valeur. Ainsi notre algo va prendre les fioles a poximité avant d'aller vers celle loin
-> DicoValFioles a comme clef les fioles et comme valeur la récompense associé a la fiole"""
    posJ = Etat(positionJoueur)
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dicoValFioles:
     #   print("f : {}".format(f))
        goal = Etat(f)
        distance = len(Astar(posJ,goal,wallStates,distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        if dicoFiole[f] > maxVal:
            maxVal = dicoFiole[f]
            maxf = f
    #print("sortie du parcours des fioles de strategie_naive")
    #print("maxf : {}".format(maxf))
    chemin = Astar(posJ, Etat(maxf), wallStates, distance_Manhattan)
    return chemin[0]
        


