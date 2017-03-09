# -*- coding: utf-8 -*-

from Astar import *
import random


# -----------------------------------------------------------------------------------

def choisit_couleur_pref(fioles):
    """ Prend un dictionnaire de fiole en entrée et retourne un tuple avec les couleurs par ordre de préférance et 
    un dictionnaire avec la récompense associé à chaque fioles """
    color = ["r","j","b"]
    random.shuffle(color)
    return color

def FioleValue(color,fioles):
    dico = {}
    for f in fioles:
        if fioles[f] == color[0]:            
            dico[f] = 10
        elif fioles[f] == color[1]:
            dico[f] = 7
        else:
            dico[f] = 2
    return  dico

def Clustering(fioles,wallStates):
    """Prend une liste de fioles et retourne une liste des clusters"""
    LFioles = fioles[::]
    for f1 in LFioles:
        for f2 in LFioles:
            distance = len(Astar(f1,f2,wallStates, distance_Manhattan))
            if distance < 3:
                LFioles[f1].append(f2)
                LFioles[f2] = None;
    return LFioles
# -------------------------------------------------------------------------------------
#                        ESPACE DEDIE AU STRATEGIE
#-------------------------------------------------------------------------------------

#remarque : les strategies retournes un tuple (row, col) correspondant au prochain coup a jouer


def strategie_naive(color,fioles, positionJoueur, wallStates):
    """ Chaque fiole a une valeur : valFiole - distFiole et on prend la fiole avec la plus grande valeur. Ainsi notre algo va prendre les fioles a poximité avant d'aller vers celle loin
-> DicoValFioles a comme clef les fioles et comme valeur la récompense associé a la fiole"""
    if fioles == {}:
        return positionJoueur
    dicoValFioles = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dicoValFioles:
     #   print("f : {}".format(f))
        distance = len(Astar(positionJoueur,f,wallStates,distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        if dicoFiole[f] > maxVal and distance != 0:
            maxVal = dicoFiole[f]
            maxf = f
    #print("sortie du parcours des fioles de strategie_naive")
    #print("maxf : {}".format(maxf))
    chemin = Astar(positionJoueur, maxf, wallStates, distance_Manhattan)
    #print("chemin : {}".format(chemin))
    return chemin[0]



