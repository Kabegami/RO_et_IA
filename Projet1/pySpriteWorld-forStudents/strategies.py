# -*- coding: utf-8 -*-

from Astar import *

def jeu(Init, game, fioles,wallStates, player,numPlayer,score):
    etat = Etat(Init)
    fiolesPrises = dict()
    for f in fioles:
        if f not in fiolesPrises:
            goal = Etat(f)
            print("etat, goal : {},{}".format(etat.position, f))
            c =  Astar(etat,goal,wallStates,distance_Manhattan)
            print(c)
            etat = Etat(deplace(etat, c, game,player,numPlayer,fioles,score,fiolesPrises))

def deplace(Init, chemin,game,player,numplayer,fioles,score,fiolesPrises):
    """bug(voir le fichier bug)"""
    for etat in chemin:
        row = etat[0]
        col = etat[1]
        player.set_rowcol(row,col)
        if (row, col) in fioles:
            o = game.player.ramasse(game.layers)
            fiolesPrises[(row,col)] = True
            score[numplayer] += 1
        game.mainiteration()
    print("derniere case",chemin[-1])
    return etat

def trouve_meilleur_fiole(posJ,wallStates,ListeCouleurPref, fioleRamasser):
    dbest = 1000000000
    best = None
    for Lc in ListeCouleurPref:
        for fiole in Lc:
            if fiole not in fioleRamasser:
                d = len(Astar(posJ,Etat(fiole),wallStates, distance_Manhattan))
                if d < dbest:
                    dbest = d
                    fbest = fiole
    return (dbest, fbest)
                
    

def strategie_naive(ListeCouleurPref, fioles, Init):
    """->ListeCouleurPref est une liste contenant une liste de fioles par couleur pref L[0] meilleur, ...
    ->fioles une liste contenant les fioles
    -> Init la position initiale
    
    Idée de la strategie : Il cherche en priorité ses fioles préferer sans ce soucier du jeu de l'adversaire"""
    fiolePrise = []
    posJ = Init
    while fioleRamasser != fioles:
        f = trouve_meilleur_fiole(posJ,wallStates, ListeCouleurPref, fiolePrise)
        c = Astar(posJ, etat(f), wallStates, distance_Manhattan)
        deplace(posJ,f,c)
        

def strategie_glouton(DicoValFioles, fioles, Init, wallState):
    """ Chaque fiole a une valeur : valFiole - distFiole et on prend la fiole avec la plus grande valeur. Ainsi notre algo va prendre les fioles a poximité avant d'aller vers celle loin
-> DicoValFioles a comme clef les fioles et comme valeur la récompense associé a la fiole"""
    posJ = etat(Init)
    dicoFiole = dict()
    maxD = None
    for f in DicoValFioles:
        dicoFiole[f] = DicoValFioles[f] - len(Astar(posJ, Etat(f), wallStates, distance_Manhattan))
        if minD == None:
            maxf = f
            maxD = dicoFiole[f]
        if dicoFiole[f] > maxD:
            maxf = f
            maxD = dicoFiole[f]
    return maxf
        
        


