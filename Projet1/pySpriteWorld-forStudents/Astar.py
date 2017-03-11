# -*- coding: utf-8 -*-

import heapq

def distance_Manhattan(etat,etat_final):
    """(tuple)*(tuple) -> int"""
    x = etat[0]
    y = etat[1]
    xF = etat[0]
    yF = etat[1]
    return abs(xF - x) + abs(yF - y)

class Noeud(object):
    def __init__(self,position):
        self.position = position
        self.pere = None
        self.fils = []
        self.distance = 0

    def ajoute_fils(self, fils):
        self.fils.append(fils)

    def ajoute_pere(self,pere):
        self.pere = pere
        self.distance = self.pere.distance + 1 
        

def exploreNoeud(noeud, final, wallStates,frontiere):
    """ Retourne l'ensemble des cases à ajouter dans la frontière depuis notre case ajouté"""
    x = noeud.position[0]
    y = noeud.position[1]
    if (x+1,y) not in wallStates and x+1 >= 0 and y >= 0 and x+1 <= 20 and y <= 20:
        pos = (x+1,y)
        fils = Noeud(pos)
        noeud.ajoute_fils(fils)
        fils.ajoute_pere(noeud)
    if (x-1,y) not in wallStates and x-1 >= 0 and y >= 0 and x-1 <= 20 and y <= 20:
        pos = (x-1,y)
        fils = Noeud(pos)
        noeud.ajoute_fils(fils)
        fils.ajoute_pere(noeud)
    if (x,y+1) not in wallStates and x >= 0 and y+1 >= 0 and x <= 20 and y+1 <= 20:
        pos = (x,y+1)
        fils = Noeud(pos)
        noeud.ajoute_fils(fils)
        fils.ajoute_pere(noeud)
    if (x,y-1) not in wallStates and x >= 0 and y-1 >= 0 and x <= 20 and y-1 <= 20:
        pos = (x,y-1)
        fils = Noeud(pos)
        noeud.ajoute_fils(fils)
        fils.ajoute_pere(noeud)

def retrouve_chemin_noeud(final):
    noeud = final
    chemin = []
    while noeud.pere != None:
        chemin.append(noeud.position)
        noeud = noeud.pere
    chemin.reverse()
    return chemin
    
        
def Astar(init, final , wallstates, h):
    NoeudInit = Noeud(init)
    frontiere = [(NoeudInit.distance + h(NoeudInit.position, final), NoeudInit)]
    reserve = {}
    bestNoeud = NoeudInit
    while frontiere != [] and bestNoeud.position != final:
        (min_f, bestNoeud) = heapq.heappop(frontiere)
        if bestNoeud.position not in reserve:
            reserve[bestNoeud.position] = bestNoeud.distance
            exploreNoeud(bestNoeud, final, wallstates, frontiere)
            for new in bestNoeud.fils:
                heapq.heappush(frontiere, (new.distance + h(new.position, final), new))
    #print(reserve)
    chemin = retrouve_chemin_noeud(bestNoeud)
    #print("chemin : ",chemin)
    return chemin
