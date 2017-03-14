# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys
from Astar import *
from strategies import *
from jeu import *
from DiscreteWorld_FaceAFace import *

def jeuXOXO(Init, game, fioles, wallStates, player, numPlayer, score):
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


def jeu_par_iteration(game, PositionJoueurs, fioles, wallStates, players, scores,strategie1,strategie2):
    # on tire les couleurs des joueurs aléatoirement
    couleur1 = choisit_couleur_pref(fioles)
    couleur2 = choisit_couleur_pref(fioles)
    print("La liste de préférences des couleurs du premier joueur est : {}".format(couleur1))
    print("La liste de préférence du second joueurs est : {}".format(couleur2))
    
    while fioles != {}:
        #joueur 1 : fille, joueur 2 : garçon
        dico_pref1 = FioleValue(couleur1,fioles)
        dico_pref2 = FioleValue(couleur2,fioles)
        # on applique les strategies des joueurs
        (row1, col1) = strategie1(couleur1,fioles, PositionJoueurs,0, wallStates)
        (row2, col2) = strategie2(couleur2,fioles, PositionJoueurs,1,wallStates)
        #(row2, col2) = strategie_bestValeurProche_possible(couleur2,fioles, PositionJoueurs[1],PositionJoueurs[0],wallStates)
        #on bouge les joueurs
        players[0].set_rowcol(row1,col1)
        players[1].set_rowcol(row2,col2)

        #on ramasse les fioles
        if (row1,col1) in fioles:
            o = players[0].ramasse(game.layers)
            fioles.pop((row1,col1))
            scores[0] += dico_pref1[(row1,col1)]

        if (row2,col2) in fioles:
            o = players[1].ramasse(game.layers)
            fioles.pop((row2,col2))
            scores[1] += dico_pref2[(row2,col2)]

        #on actualise l'état du jeu
        game.mainiteration()
        #update de la position des joueurs
        PositionJoueurs[0] = (row1, col1)
        PositionJoueurs[1] = (row2, col2)

    print("Le score du joueur 1 est : {}".format(scores[0]))
    print("Le score du joueur 2 est : {}".format(scores[1]))

def jeu_par_iteration_contre(game, PositionJoueurs, fioles, wallStates, players, scores,strategie1):
    # on tire les couleurs des joueurs aléatoirement
    couleur1 = choisit_couleur_pref(fioles)
    couleur2 = choisit_couleur_pref(fioles)
    print("La liste de préférences des couleurs du premier joueur est : {}".format(couleur1))
    print("La liste de préférence du second joueurs est : {}".format(couleur2))
    b = False
    chemin = None

    while fioles != {}:
        #joueur 1 : fille, joueur 2 : garçon
        dico_pref1 = FioleValue(couleur1,fioles)
        dico_pref2 = FioleValue(couleur2,fioles)
        # on applique les strategies des joueurs
        (row1, col1) = strategie1(couleur1,fioles, PositionJoueurs,0, wallStates)
        print(" b = ",b)
        reponce = strategie_contre(couleur2,fioles, PositionJoueurs,1,wallStates,b,chemin)
        (row2, col2) = reponce[0]
        b = reponce[1]
        chemin = reponce[2]
        #(row2, col2) = strategie_bestValeurProche_possible(couleur2,fioles, PositionJoueurs[1],PositionJoueurs[0],wallStates)
        #on bouge les joueurs
        players[0].set_rowcol(row1,col1)
        players[1].set_rowcol(row2,col2)

        #on ramasse les fioles
        if (row1,col1) in fioles:
            o = players[0].ramasse(game.layers)
            fioles.pop((row1,col1))
            scores[0] += dico_pref1[(row1,col1)]

        if (row2,col2) in fioles:
            o = players[1].ramasse(game.layers)
            fioles.pop((row2,col2))
            scores[1] += dico_pref2[(row2,col2)]

        #on actualise l'état du jeu
        game.mainiteration()
        #update de la position des joueurs
        PositionJoueurs[0] = (row1, col1)
        PositionJoueurs[1] = (row2, col2)

    print("Le score du joueur 1 est : {}".format(scores[0]))
    print("Le score du joueur 2 est : {}".format(scores[1]))
    
    
def statistique(strategie1, strategie2):
    with open("statistiques/stat1","w") as f:
        for i in range(nbItterations):
            jeu_par_iteration(game, PositionJoueurs, fioles, wallStates, players, scores)
        s1 = scores[0] / (1.0*nbItterations)
        s2 = scores[1] / (1.0*nbItterations)
        chaine = "Pour {} parties jouées on a : \n score moyen du joueur 1 : {} \n score moyen du joueur 2 : {}".format(nbItterations, s1,s2)
        f.write(chaine)
    
    
if __name__ == "__main__":
    jeu(strategie_bestValeurProche, strategie_bestVal_proximite)
