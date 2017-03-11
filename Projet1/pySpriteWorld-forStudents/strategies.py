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


def strategie_bestValeurProche(color,fioles, positionJoueur, wallStates):
    """ Chaque fiole a une valeur : valFiole - distFiole et on prend la fiole avec la plus grande valeur. Ainsi notre algo va prendre les fioles a poximité avant d'aller vers celle loin
-> DicoValFioles a comme clef les fioles et comme valeur la récompense associé a la fiole"""
    if fioles == {}:
        return positionJoueur
    dicoValFioles = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dicoValFioles:
        distance = len(Astar(positionJoueur,f,wallStates,distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        if dicoFiole[f] > maxVal and distance != 0:
            maxVal = dicoFiole[f]
            maxf = f
    chemin = Astar(positionJoueur, maxf, wallStates, distance_Manhattan)
    if chemin == []:
        return positionJoueur
    return chemin[0]

def strategie_naive(fioles, positionJoueur, wallStates):
    """ Strategie naive qui consiste a maximiser le nombre de fioles ramassés en allant chercher la fiole la plus proche de sa position"""
    maxd = 10000000
    maxf = None
    for f in fioles:
        distance = len(Astar(positionJoueur, f, wallStates, distance_Manhattan))
        if distance < maxd:
            maxd = distance
            maxf = f
    chemin = Astar(positionJoueur, maxf, wallStates, distance_Manhattan)
    #si le joueur est sur la fiole a ramasser
    if chemin == []:
        return positionJoueur
    return chemin[0]

def strategie_bestValeurProche_possible(color,fioles, positionJoueur, positionAdv, wallStates):
    """Variante de la strategie bestValeurProche qui tient compte de l'adversaire et ne vas pas chercher une
    fiole si l'adversaire est plus proche de cette fiole que lui
    rq : marche mal"""
    if fioles == {}:
        return positionJoueur
    dicoValFioles = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal_possible = -1000000
    maxf_possible = None
    maxVal_imp = -10000000
    maxf_imp = None
    for f in dicoValFioles:
        distance = len(Astar(positionJoueur, f, wallStates, distance_Manhattan))
        distance_adv = len(Astar(positionAdv, f, wallStates, distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        if dicoFiole[f] > maxVal_possible and distance != 0 and (distance - distance_adv >= 0):
            maxVal_possible = dicoFiole[f]
            maxf_possible = f
        if dicoFiole[f] > maxVal_imp and distance != 0 and (distance- distance_adv < 0):
            maxVal_imp = dicoFiole[f]
            maxf_imp = f
    if maxf_possible is not None:
        chemin = Astar(positionJoueur, maxf_possible, wallStates, distance_Manhattan)
    else:
        chemin = Astar(positionJoueur, maxf_imp, wallStates, distance_Manhattan)
    if chemin == []:
        return positionJoueur
    return chemin[0]
