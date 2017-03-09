# -*- coding: utf-8 -*-

from Astar import *
from strategies import *


def jeu(Init, game, fioles, wallStates, player, numPlayer, score):
    """ Souvant quand il y  a des téléportations c'est du a la derniere position d'un des chemin precedant
    Il y a la valeurs de certain etat qui ne se reinitialise pas"""
    etat = Init
    fiolesPrises = dict()
    for f in fioles:
        if f not in fiolesPrises:
            c =  Astar(etat, f, wallStates, distance_Manhattan)
            print(c)
            etat = deplace(etat, c, game, player,numPlayer,fioles,score,fiolesPrises)
            #print("le nouvel etat initial est {}".format(position_precedante))
            print("le nouvel etat initial est : {}".format(etat))

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

def jeu_par_iteration(game, PositionJoueurs, fioles, wallStates, players, scores):
    couleur1 = choisit_couleur_pref(fioles)
    for iteration in range(200):
        dico_pref1 = FioleValue(couleur1,fioles)
        (row, col) = strategie_naive(couleur1,dico_pref1, PositionJoueurs[0], wallStates)
        print("strat 1 : {} ,{}".format(row,col))
        players[0].set_rowcol(row,col)
        if (row,col) in fioles:
            o = players[0].ramasse(game.layers)
            fioles.pop((row,col))
            scores[0] += 1
        game.mainiteration()
        print("position precedante : {}, position actuelle : {}".format(PositionJoueurs[0],(row,col)))
        PositionJoueurs[0] = (row,col)
        print("Fin de l'ittération : {}".format(iteration))
    
    
    
        
    
