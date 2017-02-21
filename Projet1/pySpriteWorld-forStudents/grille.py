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
import heapq

# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/pathfindingWorld_MultiPlayer2.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    print(type(player))
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Building the matrix
    #-------------------------------
       
           
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
        
    
    #-------------------------------
    # Strategies des joueurs
    #-------------------------------
    i = 0
    print("init state : ",initStates)
    EtatInit = Etat(initStates[0])
    EtatFinal = Etat(goalStates[0])
    chemin  = Astar(EtatInit, EtatFinal, wallStates, distance_Manhattan)
    print("Astar : ",chemin)
    
    #------------------------------
    # On fait bouger les joueurs
    #-----------------------------
    while i != 3:
        for etat in chemin:
            row = etat[0]
            col = etat[1]
            player.set_rowcol(row,col)
            print("position:",row,col)
            game.mainiteration()
            # si on a  trouvé l'objet on le ramasse
        
            if (row,col)==goalStates[i]:
                o = game.player.ramasse(game.layers)
                #game.mainiteration()
                print ("Objet trouvé!", o)
                i += 1
                if i != 3:
                    EtatFinal = Etat(goalStates[i])
                    chemin = Astar(Etat((row,col)), EtatFinal, wallStates, distance_Manhattan)

    pygame.quit()

    #pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


