# -*- coding: utf-8 -*-

from Astar import *
import copy
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
    positionAdv = abs(1 - numJoueur)
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

#------------------------------------------------------------------------------------
#                     STRATEGIE CONTRE
#------------------------------------------------------------------------------------

def chemin_bestValeur_Proche(color,dicoValFioles,joueur, wallStates):
    """ retourne le tuple avec la meilleur fiole et le chemin pour y aller"""
    if dicoValFioles == {}:
        return (None,[joueur])
    dicoFiole = dict()
    maxVal = -1000000
    maxf = None
    for f in dicoValFioles:
        distance = len(Astar(joueur,f,wallStates,distance_Manhattan))
        dicoFiole[f] = dicoValFioles[f] - distance
        if dicoFiole[f] > maxVal:
            maxVal = dicoFiole[f]
            maxf = f
    chemin = Astar(joueur, maxf, wallStates, distance_Manhattan)
    if chemin == []:
        return (maxf,[joueur])
    return (maxf,chemin)

def calcule_chemin(color, fioles, posJoueur, wallStates,distance):
    """ retourne un chemin qui est [(fiole, distance)] avec la distance pour aller a la fiole depuis la derniere position"""
    #print("Nouvel appel de calcule_cheminn valeurs de fioles intial : {}".format(fioles))
    s = []
    dico_fiole = copy.deepcopy(fioles)
    distance_precedante = 0
    #print("dico_fiole en dehors du while : {}".format(dico_fiole))
    while dico_fiole != {}:
        #Tant qu'il y a des fioles on prend la meilleur fiole possible
        f,c = chemin_bestValeur_Proche(color, dico_fiole, posJoueur, wallStates)
        posJoueur = f
        del dico_fiole[f]
        s.append((f, len(c) + distance_precedante))
        distance_precedante += len(c)
    return s

def calcule_chemin_bug(color, fioles, posJoueur, wallStates,distance):
    """ retourne un chemin qui est [(fiole, distance)] avec la distance pour aller a la fiole depuis la derniere position"""
    #print("Nouvel appel de calcule_cheminn valeurs de fioles intial : {}".format(fioles))
    s = []
    dico_fiole = copy.deepcopy(fioles)
    distance_precedant = distance
    #print("dico_fiole en dehors du while : {}".format(dico_fiole))
    while dico_fiole != {}:
        #Tant qu'il y a des fioles on prend la meilleur fiole possible
        f,c = chemin_bestValeur_Proche(color, dico_fiole, posJoueur, wallStates)
        posJoueur = f
        #print("dico_fioles : {} ".format(dico_fiole))
        #print("(f : {}, c : {})".format(f,c))
        del dico_fiole[f]
        #print("Nouvelle valeur de LFioles : {}".format(dico_fiole))
        #print("test de boucle : {}".format(dico_fiole == {}))
        #si on a deja parcours une case
        s.append((f, len(c) + distance_precedant))
    return s

def dist_fiole(chemin, fiole):
    for etat in chemin:
        if etat[0] == fiole:
            return etat[1]
    print("erreur fiole non présente")


def construit_dico_gain(color,cheminJoueur,cheminAdv,fioles, dicoValFiole):
    """ Prend 2 chemin et retourne le dictionnaire de gain de mon joueur"""
    dico_gain = dict()
    for f in fioles:
        ma_dist = dist_fiole(cheminJoueur, f)
        adv_dist = dist_fiole(cheminAdv, f)
        if ma_dist - adv_dist >= 0:
            dico_gain[f] = dicoValFiole[f]
        else:
            dico_gain[f] = -1*dicoValFiole[f]
    return dico_gain

def somme_gain(dico_gain):
    somme = 0
    for f in dico_gain:
        somme += dico_gain[f]
    return somme

def permutation(color,fiole,positionChemin, cheminJoueur,wallStates,positionJoueur):
    LFioles = {}
    old = cheminJoueur[0:positionChemin]
    new = cheminJoueur[positionChemin:]
    #Pour les fioles qu'il faut recalculer
    for etat in new:
        LFioles[etat[0]] = etat[1]
    #print("Lfiole : {}".format(LFioles))
    #print("NouveauChemin : {}".format(NouveauChemin))
    #print("changementChemin : {}".format(changementChemin))
    #si la position n'est pas la première case
    if old != []:
        derniere_case = old[-1][0]
        dist_derniere_case = old[-1][1]
    else:
        derniere_case = positionJoueur
        dist_derniere_case = 0
    #on ajoute la case a permuté dans notre chemin
    #on calcule la distance de la nouvelle fiole
    distance = len(Astar(derniere_case,fiole, wallStates, distance_Manhattan)) + dist_derniere_case
    old.append((fiole, distance))
    Suite = calcule_chemin(color,LFioles, fiole, wallStates,distance)
    #on concatene les chemins
    chemin = old + Suite
    return chemin

#changement etat ?
def chemin_optimal(color,fioles,positionJoueurs,numJoueur,wallStates):
    #initialisation de l'algorithme
    dico_valeur_fiole = FioleValue(color, fioles)
    supposition_color_adv = color[::]
    Jchemin = calcule_chemin(color, dico_valeur_fiole,positionJoueurs[numJoueur],wallStates,0)
    ADVchemin = calcule_chemin(supposition_color_adv,dico_valeur_fiole,positionJoueurs[abs(1 - numJoueur)], wallStates,0)
    print("le chemin de mon joueur est Jchemin : {}".format(Jchemin))
    print("le chemin de l'adversaire est ADVchemin : {}".format(ADVchemin))  
    prec = None
    #tant que notre algorithme n'a pas convergé
    while Jchemin != prec:
        prec = Jchemin
        print("appel de meilleur_permutation !")
        Jchemin = meilleur_permutation(Jchemin,ADVchemin, color,fioles,dico_valeur_fiole,wallStates,positionJoueurs[numJoueur])
    return Jchemin

def strategie_contre(color,fioles,positionJoueurs, numJoueur, wallStates,b,chemin):
    """ on ajoute un boolean pour qu'il ne recalcule pas tout à chaque fois"""
    if b == False:
        chemin = chemin_optimal(color,fioles,positionJoueurs,numJoueur,wallStates)
        print("Chemin optimal : {}".format(chemin))
    if chemin[0][0] == positionJoueurs[numJoueur]:
        del chemin[0]
    deplacement = Astar(positionJoueurs[numJoueur],chemin[0][0],wallStates,distance_Manhattan)
    if deplacement != []:
        return (deplacement[0], True, chemin)
    else:
        return (positionJoueurs[numJoueur], True, chemin)

    
def meilleur_permutation(Jchemin, ADVchemin, color, fioles, dico_valeur_fiole, wallStates,positionJoueur):
    dico_gain = construit_dico_gain(color,Jchemin, ADVchemin,fioles,dico_valeur_fiole)
    gain = somme_gain(dico_gain)
    curseur = None
    #pour les permutations utiles:
    for f in fioles:
        for positionChemin in range(len(Jchemin)):
            #distance de la position initial à  la fiole en passant par les positionChemin precedantes
            #print(Jchemin[0:positionChemin])
            #if Jchemin[0:positionChemin] == []:
            #    print("premiere case",Jchemin[0])
            #    distance = len(Astar((Jchemin[0])[0],f,wallStates,distance_Manhattan))
            #else:
            #    print(("sinon : ",Jchemin[0:positionChemin])[1])
            #    distance = (Jchemin[0:positionChemin])[1] + len(Astar((Jchemin[0])[0],f,wallStates,distance_Manhattan))
            #si on peux récupérer la fiole
            #if distance < dist_fiole(ADVchemin,f):
            new = permutation(color,f,positionChemin,Jchemin,wallStates,positionJoueur)
            new_dico_g = construit_dico_gain(color, Jchemin, ADVchemin, fioles, dico_valeur_fiole)
            new_gain = somme_gain(new_dico_g)
            new_curseur = (f,positionChemin)

                #on verifie si cela améliore la recherche
            if new_gain > gain:
                gain = new_gain
                curseur = new_curseur

    #si il n'y a aucune amélioration
    if curseur == None:
        print("il n'y a pas eu de permutation")
        return Jchemin
    else:
        f,pos = curseur
        new_chemin = permutation(f,pos,Jchemin,wallStates)
        return new_chemin

def prediction(color, fioles, PositionJoueurs, numJoueur, wallStates, EtatPrec, strategie, ListeStrat):
    if stategie(color,fiole,EtatPrec[-2],numJoueur,wallStates) == EtatPrec[-1]:
        return (True, strategie)
    for strat in ListeStrat:
        if strat(color,fiole,EtatPrec[-2],numJoueur,wallStates) == EtatPrec[-1]:
            return (True, strategie)
    return (False, None)
        
