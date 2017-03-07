# -*- coding: utf-8 -*-

import heapq

class Etat(object):
    def __init__(self,position,pere=None,distance=0):
        self.position = position
        self.distance = distance
        self.pere = pere
        self.f = 0

    def __repr__(self):
        return "position : {}, distance : {}, pere : {}, f : {}".format(self.position, self.distance, self.pere,self.f)

class Frontiere(object):
    def __init__(self, TasF=[], ListeEtat=[]):
        self.TasF = TasF
        self.ListeEtat = ListeEtat

    def __repr__(self):
        return "Frontiere = TasF : {}, ListeEtat : {}".format(self.TasF, self.ListeEtat)

    def bestEtat(self):
        f_min = heapq.heappop(self.TasF)
        for etat in self.ListeEtat:
            if etat.f == f_min:
                e = etat
        self.ListeEtat.remove(e)
        return e

    def ajoute(self,L):
        for etat in L:
            heapq.heappush(self.TasF,etat.f)
            self.ListeEtat.append(etat)

def exploreEtat(etat,etatFinal, wallStates,reserve,h):
    L = []
    Ltuple = []
    x = etat.position[0]
    y = etat.position[1]
    if (x+1,y) not in wallStates and x+1 >= 0 and y >= 0 and x+1 <= 20 and y <= 20:
        pos = (x+1,y)
        e = Etat(pos,etat,etat.distance +1)
        e.f = e.distance + h(e.position, etatFinal.position)
        L.append(e)
    if (x-1,y) not in wallStates and x-1 >= 0 and y >= 0 and x-1 <= 20 and y <= 20:
        pos = (x-1,y)
        e = Etat(pos,etat,etat.distance +1)
        e.f = e.distance + h(e.position, etatFinal.position)
        L.append(e)
    if (x,y+1) not in wallStates and x >= 0 and y+1 >= 0 and x <= 20 and y+1 <= 20:
        pos = (x,y+1)
        e = Etat(pos,etat,etat.distance +1)
        e.f = e.distance + h(e.position, etatFinal.position)
        L.append(e)
    if (x,y-1) not in wallStates and x >= 0 and y-1 >= 0 and x <= 20 and y-1 <= 20:
        pos = (x,y-1)
        e = Etat(pos,etat,etat.distance +1)
        e.f = e.distance + h(e.position, etatFinal.position)
        L.append(e)
    reserve[etat.position] = L

def retrouve_chemin(etat_final):
    etat = etat_final
    chemin = []
    while etat.pere != None:
        chemin.append(etat.position)
        etat = etat.pere
    chemin.reverse()
    return chemin

def distance_Manhattan(etat,etat_final):
    """(tuple)*(tuple) -> int"""
    x = etat[0]
    y = etat[1]
    xF = etat[0]
    yF = etat[1]
    return abs(xF - x) + abs(yF - y)

def Astar(EtatInit, EtatFinal,wallStates, h):
    """ Dans certain cas Astar ne part pas a partir de l'étatInit"""
    L = [EtatInit]
    frontiere = Frontiere()
    frontiere.ajoute(L)
    reserve = {}
    bestEtat = EtatInit
    print(bestEtat)
    while frontiere != [] and bestEtat.position != EtatFinal.position:
        #print("etat final : {}, bestEtat : {}".format(EtatFinal.position, bestEtat.position))
        bestEtat = frontiere.bestEtat()
        if bestEtat.position not in reserve:
            exploreEtat(bestEtat,EtatFinal,wallStates,reserve,h)
            frontiere.ajoute(reserve[bestEtat.position])
    if frontiere == []:
        print("il n'existe pas de chemin")
        return []
    chemin = retrouve_chemin(bestEtat)
    return chemin
    
        
    
