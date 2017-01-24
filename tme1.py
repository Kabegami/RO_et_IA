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

class Master(object):
    def __init__(self,L):
        self.nom = L[0]
        self.listPref = L[1:-1]
        self.capacite = (int) (L[-1])
        self.nombreEtudiant = 0
        self.pireEtudiant = 0

    def __repr__(self):
        return "nom : {} \n liste de preference {} \n capacite  {} \n nombre d'etudiant {} \n".format(self.nom, self.listPref, self.capacite,self.nombreEtudiant)


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

def indexMaster(M,master):
    for i in M:
       #print(i.nom)
        if i.nom == master:
            print("Master :",i.nom)
            return i
    print("Master non trouve !")
    print("master : ",master)
    print("liste master :",M)
    return []

def indexEtudiant(M, Nbetudiant):
    for i in M:
        if i.nb == Nbetudiant:
            return i
    print("Etudiant non trouve !")
    print("nb :",Nbetudiant)
    print("L : ",M)
    return []

def indexPosEtudiant(M, nb):
    for i in range(0,len(M)):
        if M[i].nb == nb:
            return i
    print("Etudiant pos non trouve !")
    return []
    

def gestionMaster(ListeEtudiant, Master, etudiant, etudiant_libre):
    if Master.nombreEtudiant < Master.capacite:
        Master.nombreEtudiant += 1
        etudiant_libre.remove(etudiant)
        etudiant.master.remove(Master.nom)
        print("l etudiant {} est ajouter dans le master {}".format(etudiant.nom,Master.nom))
        
    else:
        if etudiant.nb >= Master.pireEtudiant:
            #on ajoute le nouvelle etudiant au master
            Master.nombreEtudiant += 1
            AncienEtu = indexEtudiant(ListeEtudiant, Master.pireEtudiant)
            AncienEtu.pos = ""
            print("l etudiant {} est ajouter dans le master {}".format(etudiant.nom,Master.nom))
            Master.pireEtudiant = etudiant.nb
            etudiant.pos = Master.nom
            etudiant.master.remove(Master.nom)
            etudiant_libre.remove(etudiant)
            # et on rajoute l'ancien dans etudiant_libre
            etudiant_libre.append(AncienEtu)
            i = indexPosEtudiant(ListeEtudiant, AncienEtu)
            etudiant_libre[-1] = ListeEtudiant[i]
    ListeEtudiant[etudiant.nb] = etudiant
            
            
            
        
        
        

def GaleShapley(M1,M2):
    ListeEtudiant = []
    ListeMaster = []
    for i in M1:
        ListeEtudiant.append(Etudiant(i))
    print(ListeEtudiant)
    for i in M2:
        ListeMaster.append(Master(i))
    print(ListeMaster)
    
    #on veut travailler sur une unique instance de la classe etudiant pour qu'elle soit a jour 
    #etudiant_libre = []
    #for i in ListeEtudiant:
     #   etudiant_libre.append(i.nb)
    etudiant_libre = ListeEtudiant[::]    
    while etudiant_libre != []:
        print("---------------------------------------------- ")
        print("             NOUVEAU TOUR DE BOUCLE            ")
        print("---------------------------------------------- ")
        e = etudiant_libre[0]
        print("numero de l'etudiant : ",e.nb)
        master = e.master[0]
        print("master de l'etudiant : ",master)
        m = indexMaster(ListeMaster,master)
        print("cherche a integrer ", m.nom)
        print("Liste des etudiants libre", etudiant_libre)
        gestionMaster(ListeEtudiant,m,e, etudiant_libre)
        
        
    
M1 = PrefEtu('TestPrefEtu.txt')
M2 = PrefSpe('TestPrefSpe.txt')
print(M1)
print(M2)
GaleShapley(M1,M2)
