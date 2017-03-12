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
    LCluster = fioles[::]
    for f1 in LFioles:
        for f2 in LFioles:
            if f1 != f2:
                distance = len(Astar(f1,f2,wallStates, distance_Manhattan))
                if distance < 3:
                    LCluster[f1].append(f2)
                    LCluster[f2] = None;
    return LCluster

def evalue_fiole(color,fiole):
    if fiole == color[0]:            
        return 10
    elif fiole == color[1]:
        return 7
    else:
        return 2

def ClusterValue(color, fioles, Lcluster):
    "Ne marche pas car un dictionnaire ne peux contenir d'objet mutable"""
    dico = {}
    for cluster in Lcluster:
        #si c'est une fioles
        if len(cluster) == 1:
            dico[cluster] = "toto"
        
def construit_dico_proximite(fioles,wallStates):
    dico = dict()
    for f1 in fioles:
        distance = 0
        for f2 in fioles:
            if f1 != f2:
                distance += len(Astar(f1,f2,wallStates, distance_Manhattan))
        dico[f1] = distance
    return dico
# -------------------------------------------------------------------------------------
#                        ESPACE DEDIE AU STRATEGIE
#-------------------------------------------------------------------------------------

#remarque : les strategies retournes un tuple (row, col) correspondant au prochain coup a jouer


def strategie_bestValeurProche(color,fioles, positionJoueurs,numJoueur, wallStates):
    """ Chaque fiole a une valeur : valFiole - distFiole et on prend la fiole avec la plus grande valeur. Ainsi notre algo va prendre les fioles a poximité avant d'aller vers celle loin
-> DicoValFioles a comme clef les fioles et comme valeur la récompense associé a la fiole"""
    if fioles == {}:
        return positionJoueurs[numJoueur]
    dicoValFioles = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dicoValFioles:
        distance = len(Astar(positionJoueurs[numJoueur],f,wallStates,distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        if dicoFiole[f] > maxVal and distance != 0:
            maxVal = dicoFiole[f]
            maxf = f
    chemin = Astar(positionJoueurs[numJoueur], maxf, wallStates, distance_Manhattan)
    if chemin == []:
        return positionJoueurs[numJoueur]
    return chemin[0]

def strategie_naive(color,fioles, positionJoueurs,numJoueur, wallStates):
    """ Strategie naive qui consiste a maximiser le nombre de fioles ramassés en allant chercher la fiole la plus proche de sa position"""
    maxd = 10000000
    maxf = None
    for f in fioles:
        distance = len(Astar(positionJoueurs[numJoueur], f, wallStates, distance_Manhattan))
        if distance < maxd:
            maxd = distance
            maxf = f
    chemin = Astar(positionJoueurs[numJoueur], maxf, wallStates, distance_Manhattan)
    #si le joueur est sur la fiole a ramasser
    if chemin == []:
        return positionJoueurs[numJoueur]
    return chemin[0]

def strategie_bestVal_proximite(color, fioles, positionJoueurs, numJoueur, wallStates,alpha=0.5,betta=1.5):
    """ Favorise les fioles proches et qui sont en groupes,
alpha est un parametre d'exploration compris entre 0 et 1"""
    dico_proximite = construit_dico_proximite(fioles,wallStates)
    dico_valeur_fiole = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dico_valeur_fiole:
        distance = len(Astar(positionJoueurs[numJoueur], f, wallStates, distance_Manhattan))
        dicoFiole[f] = betta*dico_valeur_fiole[f] - distance - alpha*dico_proximite[f]
        if dicoFiole[f] > maxVal and distance != 0:
            maxVal = dicoFiole[f]
            maxf = f
    chemin = Astar(positionJoueurs[numJoueur], maxf, wallStates, distance_Manhattan)
    if chemin == []:
        return positionJoueurs[numJoueur]
    return chemin[0]

def strategie_Cluser(color, fioles,positionJoueurs, numJoueur, wallStates):
    """ Prend en compte les cluster de taille 3 """
    dico_valeur_fiole = FioleValue(color, fioles)
    dicoFiole = dict()
    LCluster = Clustering(fioles, wallStates)
    maxVal = -1000000
    maxf = None

    

def strategie_bestValeurProche_possible(color,fioles, positionJoueurs, numJoueur, wallStates):
    """Variante de la strategie bestValeurProche qui tient compte de l'adversaire et ne vas pas chercher une
    fiole si l'adversaire est plus proche de cette fiole que lui
    rq : marche mal"""
    positionAdv = 1 - numJoueur
    if fioles == {}:
        return positionJoueurs[numJoueur]
    dicoValFioles = FioleValue(color, fioles)
    dicoFiole = dict()
    maxVal_possible = -1000000
    maxf_possible = None
    maxVal_imp = -10000000
    maxf_imp = None
    for f in dicoValFioles:
        distance = len(Astar(positionJoueurs[numJoueur], f, wallStates, distance_Manhattan))
        distance_adv = len(Astar(positionAdv, f, wallStates, distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        #si je suis plus proche de la fiole que mon adversaire
        if dicoFiole[f] > maxVal_possible and distance != 0 and (distance - distance_adv >= 0):
            maxVal_possible = dicoFiole[f]
            maxf_possible = f
        if dicoFiole[f] > maxVal_imp and distance != 0 and (distance- distance_adv < 0) and distance_adv <= 5:
            maxVal_imp = dicoFiole[f]
            maxf_imp = f
    if maxf_possible is not None:
        chemin = Astar(positionJoueurs[numJoueur], maxf_possible, wallStates, distance_Manhattan)
    else:
        chemin = Astar(positionJoueurs[numJoueur], maxf_imp, wallStates, distance_Manhattan)
    if chemin == []:
        return positionJoueurs[numJoueur]
    return chemin[0]
