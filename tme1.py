import os
import numpy

class Etudiant(object):
    def __init__(self, L):
        self.nom = L[0]
        self.master = L[1:]
        self.pos = ""
        self.nb = (int)(self.nom[3:])

    def __repr__(self):
        return "Nom : {} \n Liste master : {} \n est pris dans le master : {} \n numero etudiant : {} \n".format(self.nom, self.master,self.pos, self.nb)

    def positionMaster(self, master):
        return self.master.index(master)

class MatriceEtudiant(object):
    def __init__(self,matrice):
        self.matrice = matrice

    def __repr__(self):
        return "Matrice Etudiant : \n {}".format(self.matrice)

    def etudiant_libre(self):
        for etudiant in self.matrice:
            if etudiant.pos == "":
                return True
        return False

    def premier_etu_libre(self):
        for etudiant in self.matrice:
            if etudiant.pos == "":
                return etudiant
        print("erreur premier_etu_libre")
        return None

class Master(object):
    def __init__(self,L):
        self.nom = L[0]
        self.listPref = L[1:-1]
        self.capacite = (int) (L[-1])
        self.nombreEtudiant = 0
        self.pireEtudiant = self.listPref[-1]
        self.etudiants = []

    def __repr__(self):
        return "nom : {} \n liste de preference {} \n capacite  {} \n nombre d'etudiant {} \n etudiants {} \n le pire etudiant est {} \n".format(self.nom, self.listPref, self.capacite,self.nombreEtudiant, self.etudiants, self.pireEtudiant)

    def etudiant_pref(e1,e2):
        for i in self.listPref:
            if i == e1:
                pos1 = i
            if i == e2:
                pos2 = i
        if pos1 < pos2:
            return pos1
        return pos2

    def change_etu(e1, MatriceEtudiant):
        e2 = self.pireEtudiant
        for i in self.listPref:
            if i == e1:
                pos1 = i
            if i == e2:
                pos2 = i
        if pos1 < pos2:
            indice = indexEtudiant(self.etudiants, self.pireEtudiant)
            del self.etudiants[indice]
            MatriceEtudiant[self.pireEtudiant].pos = ""
            del MatriceEtudiant[self.pireEtudiant].master[0]
            self.pireEtudiant = e1
            self.etudiants.append(e1)
            MatriceEtudiant[e1.nb].pos = self.nom
            
        

def indexEtu(ListeEtudiant, nb):
    for i in ListeEtudiant:
        if i.nb == nb:
            return i.nb
    return None

def indexMaster(ListeMaster, master):
    for i in range(len(ListeMaster)):
        if ListeMaster[i].nom == master:
            return i
    print("erreur index Master ")
    return None

def lectureFichier(s):
    os.chdir('fichier_test')
    monFichier = open(s, "r") # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines() # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne
    monFichier.close() #Fermeture du fichier
    contenu[0]=contenu[0].split()     # ligne.split() renvoie une liste de toutes les chaines contenues dans la chaine ligne (separateur=espace)
    os.chdir('..')
    return contenu

def PrefEtu(fichier):
    s = lectureFichier('TestPrefEtu.txt')
    n = int(s[0][0])
    print(n)
    M = []
    for i in range(1,n+1):
        M.append(s[i].split())
    return M

def PrefSpe(fichier):
    s = lectureFichier('TestPrefSpe.txt')
    n = int(s[0][1])
    cap = s[1].split()
    M = []
    for i in range(2,n):
        l = s[i].split()
        l.append(cap[i-1])
        M.append(l)
    return M


def gestionMaster(M, e, MatriceEtudiant):
    #le master est libre
    if M.capacite > M.nombreEtudiant:
        M.etudiants.append(e.nb)
        MatriceEtudiant[e.nb].pos = M.nom
        M.nombreEtudiant += 1
        if M.etudiant_pref(e, M.pireEtudiant) == M.pireEtudiant:
            master.pireEtudiant = e
    else:
        print("etudiant ", e)
        print("MAtrice Etudiant :", MatriceEtudiant.matrice)
        Master.change_etu(e.nb, MatriceEtudiant.matrice)
            
            
            
        
        
        

def GaleShapley(M1,M2):
    ListeEtudiant = []
    ListeMaster = []
    for i in M1:
        ListeEtudiant.append(Etudiant(i))
    MatriceEtu = MatriceEtudiant(ListeEtudiant)
    for i in M2:
        ListeMaster.append(Master(i))
    print(MatriceEtu)
    print(ListeMaster)
    while MatriceEtu.etudiant_libre():
        print("---------------------------------------------- ")
        print("             NOUVEAU TOUR DE BOUCLE            ")
        print("---------------------------------------------- ")
        e = MatriceEtu.premier_etu_libre()
        print("numero de l'etudiant : ",e.nb)
        master = e.master[0]
        idMaster = indexMaster(ListeMaster, master)
        print("master de l'etudiant : ",master)
        gestionMaster(ListeMaster[idMaster], e, MatriceEtu.matrice)
        
        
    
M1 = PrefEtu('TestPrefEtu.txt')
M2 = PrefSpe('TestPrefSpe.txt')
print(M1)
print(M2)
GaleShapley(M1,M2)
