# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

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



    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'match2'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 200 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()


    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    fioles = {} # dictionnaire (x,y)->couleur pour les fioles
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets ramassables
    #goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    #print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    #-------------------------------
    # Placement aleatoire des fioles de couleur 
    #-------------------------------
    
    for o in game.layers['ramassable']: # on considère chaque fiole
        
        #on détermine la couleur
    
        if o.tileid == (19,0): # tileid donne la coordonnee dans la fiche de sprites
            couleur = 'r'
        elif o.tileid == (19,1):
            couleur = 'j'
        else:
            couleur = 'b'

        # et on met la fiole qqpart au hasard

        x = random.randint(1,19)
        y = random.randint(1,19)

        while (x,y) in wallStates: # ... mais pas sur un mur
            x = random.randint(1,19)
            y = random.randint(1,19)
        o.set_rowcol(x,y)
        # on ajoute cette fiole 
        fioles[(x,y)]=couleur

        game.layers['ramassable'].add(o)
        game.mainiteration()                

    print("Les fioles ont été placées aux endroits suivants: \n", fioles)


    
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
        
    # bon ici on fait juste plusieurs random walker pour exemple...
    
    posPlayers = initStates
    print(fioles)
    for f in fioles:
        print(fioles[f])
    print("score",score)
    print(type(score))
    #reserve = Astar_v2(posPlayers[0], f, wallStates, distance_Manhattan)
    #print("reserve : {}".format(reserve))
    #jeu(posPlayers[0],game,fioles,wallStates, players[0],0,score)

    # bestValeurProche VS strategie contre
    jeu_par_iteration_contre(game, posPlayers, fioles, wallStates, players, score,strategie_bestValeurProche)
    
    # bestValeurProche VS naif
    #jeu_par_iteration(game, posPlayers, fioles, wallStates, players, score, strategie_bestValeurProche,strategie_naive)

    #bestValeurProche VS bestVale_proximité
    #jeu_par_iteration(game, posPlayers, fioles, wallStates, players, score, strategie_bestValeurProche,strategie_bestVal_proximite)

   
    



    
def jeu(strategie1,strategie2):
    game = Game()
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])

    init()

    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    fioles = {} # dictionnaire (x,y)->couleur pour les fioles
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)

        #-------------------------------
    # Placement aleatoire des fioles de couleur 
    #-------------------------------
    
    for o in game.layers['ramassable']: # on considère chaque fiole
        
        #on détermine la couleur
    
        if o.tileid == (19,0): # tileid donne la coordonnee dans la fiche de sprites
            couleur = 'r'
        elif o.tileid == (19,1):
            couleur = 'j'
        else:
            couleur = 'b'

        # et on met la fiole qqpart au hasard

        x = random.randint(1,19)
        y = random.randint(1,19)

        while (x,y) in wallStates: # ... mais pas sur un mur
            x = random.randint(1,19)
            y = random.randint(1,19)
        o.set_rowcol(x,y)
        # on ajoute cette fiole 
        fioles[(x,y)]=couleur

        game.layers['ramassable'].add(o)
        game.mainiteration()

    jeu_par_iteration(game,initStates, fioles, wallStates, players, score , strategie1,strategie2)
    return score

if __name__ == '__main__':
    main()
    


