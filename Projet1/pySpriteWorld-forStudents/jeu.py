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
    # on tire les couleurs des joueurs aléatoirement
    couleur1 = choisit_couleur_pref(fioles)
    couleur2 = choisit_couleur_pref(fioles)
    print("La liste de préférences des couleurs du premier joueur est : {}".format(couleur1))
    print("La liste de préférence du second joueurs est : {}".format(couleur2))
    
    while fioles != {}:
        dico_pref1 = FioleValue(couleur1,fioles)
        dico_pref2 = FioleValue(couleur2,fioles)
        # on applique les strategies des joueurs
        (row1, col1) = strategie_bestValeurProche(couleur1,dico_pref1, PositionJoueurs[0], wallStates)
        (row2, col2) = strategie_bestValeurProche_possible(couleur2,fioles, PositionJoueurs[1], PositionJoueurs[0],wallStates)
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
    
    
def statistique(game, PositionJoueurs, fioles, wallStates, players, scores, nbItterations):
    with open("statistiques/stat1","w") as f:
        for i in range(nbItterations):
            jeu_par_iteration(game, PositionJoueurs, fioles, wallStates, players, scores)
        s1 = scores[0] / (1.0*nbItterations)
        s2 = scores[1] / (1.0*nbItterations)
        chaine = "Pour {} parties jouées on a : \n score moyen du joueur 1 : {} \n score moyen du joueur 2 : {}".format(nbItterations, s1,s2)
        f.write(chaine)
    
    
