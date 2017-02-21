import heapq

#creation d'un tas pour la frontiere
#operation des tas :
#ajout : heapq.headppush(Tas,x)
#Retourne premierElem : heapq.heappop(T)
#heapq.heapify

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
    if (x+1,y) not in wallStates and (x+1,y) not in reserve:
        pos = (x+1,y)
        e = Etat(pos,etat,etat.distance +1)
        e.f = e.distance + h(e.position, etatFinal.position)
        L.append(e)
    if (x-1,y) not in wallStates and (x-1,y) not in reserve:
        pos = (x-1,y)
        e = Etat(pos,etat,etat.distance +1)
        e.f = e.distance + h(e.position, etatFinal.position)
        L.append(e)
    if (x,y+1) not in wallStates and (x,y+1) not in reserve:
        pos = (x,y+1)
        e = Etat(pos,etat,etat.distance +1)
        e.f = e.distance + h(e.position, etatFinal.position)
        L.append(e)
    if (x,y-1) not in wallStates and (x,y-1) not in reserve:
        pos = (x,y-1)
        e = Etat(pos,etat,etat.distance +1)
        e.f = e.distance + h(e.position, etatFinal.position)
        L.append(e)
    reserve[etat.position] = L

def retrouve_chemin(reserve,etat_final):
    etat = etat_final
    chemin = []
    while etat.pere != None:
        chemin.append(etat.position)
        etat = etat.pere
    return chemin

def distance_Manhattan(etat,etat_final):
    """(tuple)*(tuple) -> int"""
    x = etat[0]
    y = etat[1]
    xF = etat[0]
    yF = etat[1]
    return abs(xF - x) + abs(yF - y)

def Astar(EtatInit, EtatFinal,wallStates, h):
    L = [EtatInit]
    frontiere = Frontiere()
    frontiere.ajoute(L)
    #print("frontiere : ",frontiere)
    reserve = {}
    dico_pere = {}
    bestEtat = EtatInit
    print(bestEtat)
    while frontiere != [] and bestEtat.position != EtatFinal.position:
        test = []
        bestEtat = frontiere.bestEtat()
        exploreEtat(bestEtat,EtatFinal,wallStates,reserve,h)
        #print("reserve : ",reserve[bestEtat])
        frontiere.ajoute(reserve[bestEtat.position])
        #print("frontiere : ",frontiere)
        #print("reserve : ",reserve)
        test.append(bestEtat.position)
        print("test :",test)
    chemin = retrouve_chemin(dico_pere,etatFinal)
    return chemin
    
        
    
