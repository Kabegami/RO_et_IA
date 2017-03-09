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
    
    def ajoute(self, L):
        for etat in L:
            heapq.heappush(self.TasF, etat.f)
            self.ListeEtat.append(etat)
   
def exploreEtat(etat, etatFinal, wallStates, h):
    """ Retourne l'ensemble des cases à ajouter dans la frontière depuis notre case ajouté"""
    L = []
    x = etat.position[0]
    y = etat.position[1]
    if (x+1,y) not in wallStates and x+1 >= 0 and y >= 0 and x+1 <= 20 and y <= 20:
        pos = (x+1,y)
        #format position, pere, distance
        e = Etat(pos, etat.position , etat.distance + 1)
        e.f = e.distance + h(e.position, etatFinal)
        L.append(e)
    if (x-1,y) not in wallStates and x-1 >= 0 and y >= 0 and x-1 <= 20 and y <= 20:
        pos = (x-1,y)
        e = Etat(pos,etat.position,etat.distance + 1)
        e.f = e.distance + h(e.position, etatFinal)
        L.append(e)
    if (x,y+1) not in wallStates and x >= 0 and y+1 >= 0 and x <= 20 and y+1 <= 20:
        pos = (x,y+1)
        e = Etat(pos,etat.position,etat.distance + 1)
        e.f = e.distance + h(e.position, etatFinal)
        L.append(e)
    if (x,y-1) not in wallStates and x >= 0 and y-1 >= 0 and x <= 20 and y-1 <= 20:
        pos = (x,y-1)
        e = Etat(pos,etat.position,etat.distance + 1)
        e.f = e.distance + h(e.position, etatFinal)
        L.append(e)
    return L

def retrouve_chemin(etat_final):
    #print("appel de la fonction retrouve_chemin")
    etat = etat_final
    chemin = []
    while etat.pere is not None:
        chemin.append(etat.position)
        etat = etat.pere
    chemin.reverse()
    return chemin

def retrouve_chemin_reserve(final,reserve):
    etat = final
    chemin = []
    while reserve[etat] is not None:
        chemin.append(etat)
        etat = reserve[etat]
        print("retrouve_chemin_reserve", etat)
    chemin.reverse()
    return chemin

def distance_Manhattan(etat,etat_final):
    """(tuple)*(tuple) -> int"""
    x = etat[0]
    y = etat[1]
    xF = etat[0]
    yF = etat[1]
    return abs(xF - x) + abs(yF - y)

def Astar_bug(EtatInit, EtatFinal, wallStates, h):
    """ Bug car le joueur ce téléportee, la première case du chemin ne correspond pas a Etat Init
    Normalement seul l'etat Initial a comme pere None mais on ce retrouve avec plusieurs case sans pere"""
    L = [EtatInit]
    frontiere = Frontiere()
    frontiere.ajoute(L)
    reserve = {}
    bestEtat = EtatInit
    print(bestEtat)
    while frontiere != [] and bestEtat.position != EtatFinal.position:
        bestEtat = frontiere.bestEtat()
        if bestEtat.position not in reserve:
            #on ajoute dans la reserve
            reserve[bestEtat.position] = True
            nouvelle_cases = exploreEtat(bestEtat, EtatFinal, wallStates, h)
            frontiere.ajoute(nouvelle_cases)
    if frontiere == []:
        print("il n'existe pas de chemin")
        return []
    chemin = retrouve_chemin(bestEtat)
    return chemin
    
        

def Astar(init, final, wallStates, h):
    """ Calcule la distance vis a vis de toutes les cases"""
    #convertis en Etat
    EtatInit = Etat(init)
    L = []
    L.append(EtatInit)
    frontiere = Frontiere()
    frontiere.ajoute(L)
    reserve = {}
    bestEtat = EtatInit
    while frontiere.TasF != [] and bestEtat.position != final:
        bestEtat = frontiere.bestEtat()
        if bestEtat.position not in reserve:
            #on ajoute a la reserve
            reserve[bestEtat.position] = bestEtat.pere
            nouvelle_cases = exploreEtat(bestEtat, final, wallStates, h)
            frontiere.ajoute(nouvelle_cases)
    chemin = retrouve_chemin_reserve(final, reserve)
    return chemin

