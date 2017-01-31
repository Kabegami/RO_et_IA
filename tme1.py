import os
import numpy

#--------------------------------------------------
#                 CLASSES
#--------------------------------------------------
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

    def ChangerMaster(self, m):
        ancienMaster = self.master.index(self.pos)
        nouveauMaster = self.master.index(m.nom)
        if nouveauMaster < ancienMaster:
            return True
        return False
            

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
        self.listPref = (L[1:-1])
        for i in range(len(self.listPref)):
            self.listPref[i] = (int) (self.listPref[i])
        self.capacite = (int) (L[-1])
        self.nombreEtudiant = 0
        self.pireEtudiant = None
        self.etudiants = []

    def __repr__(self):
        return "nom : {} \n liste de preference {} \n capacite  {} \n nombre d'etudiant {} \n etudiants {} \n le pire etudiant est {} \n".format(self.nom, self.listPref, self.capacite,self.nombreEtudiant, self.etudiants, self.pireEtudiant)

    def etudiant_pref(self,e1,e2):
        print("e1",e1)
        print("e2",e2)
        for i in self.listPref:
            #print(type(i))
            if i == e1:
                pos1 = i
            if i == e2:
                pos2 = i
        print("pos 1", pos1)
        print("pos 2", pos2)
        if pos1 < pos2:
            return pos1
        return pos2

    def change_etu(self,e1, MatriceEtudiant):
        e2 = self.pireEtudiant
        for i in self.listPref:
            if i == e1:
                pos1 = i
            if i == e2:
                pos2 = i
        if pos1 < pos2:
            print("l'etudiant {} rentre dans le master {}".format(e1, self.nom))
            print("l'etudiant {} sort du le master {}".format(e2, self.nom))
            print("pire etudiant",self.pireEtudiant)
            indice = indexEtu(self.etudiants, self.pireEtudiant)
            del self.etudiants[indice]
            MatriceEtudiant[self.pireEtudiant].pos = ""
            del MatriceEtudiant[self.pireEtudiant].master[0]
            self.pireEtudiant = e1
            self.etudiants.append(e1)
            MatriceEtudiant[e1].pos = self.nom
        else:
            print("l'etudiant {} est refuser par le master {}".format(e1, self.nom))
            #print(MatriceEtudiant)
            del MatriceEtudiant[e1].master[0]
            


#--------------------------------------------------
#                 Fonctions
#--------------------------------------------------

            
def indexEtu(ListeEtudiant, nb):
    print("nb ;",nb)
    print("liste etudiant",ListeEtudiant)
    for i in range(len(ListeEtudiant)):
        if ListeEtudiant[i] == nb:
            return i
    print("erreur indexEtu")
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
        #cas du premier etu
        if M.nombreEtudiant == 0:
            M.pireEtudiant = e.nb
        print("l'etudiant {} rentre dans le master {}".format(e.nb, M.nom))
        M.etudiants.append(e.nb)
        MatriceEtudiant[e.nb].pos = M.nom
        M.nombreEtudiant += 1
        if M.etudiant_pref(e.nb, M.pireEtudiant) == M.pireEtudiant:
            M.pireEtudiant = e.nb
    else:
        print("le master est plein")
        M.change_etu(e.nb, MatriceEtudiant)
            
            
            
        
        
        

def GaleShapleyEtudiant(M1,M2):
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
    print("----------------------------------------------")
    print("                RESULTAT FINAL                ")
    print("----------------------------------------------")
    for i in MatriceEtu.matrice:
        print("l'etudiant {} est dans le master {}".format(i.nb, i.pos))

def MasterLibre(MatriceMaster):
    for master in MatriceMaster:
        if master.nombreEtudiant < master.capacite:
            return True
    return False

def PremierMasterLibre(MatriceMaster):
    for master in MatriceMaster:
        if master.nombreEtudiant < master.capacite:
            return master
    print("Erreur PremierMasterLibre")
    return None

def TrouveMaster(ListeMaster, master):
    for m in ListeMaster:
        if m.nom == master:
            return m

def MasterProposeEtu(ListeMaster, master, etu):
    if etu.pos == "":
        #si l'etudiant n'a pas de master il accepte, on le supprimer de la liste de preference
        print("l'etudiant {} n'est dans aucun master et rentre dans le master {}".format(etu.nom, master.nom))
        etu.pos = master.nom
        del master.listPref[0]
        master.etudiants.append(etu.nb)
        master.nombreEtudiant += 1
    else:
        print("l'etudiant {} a un master".format(etu.nom))
        if etu.ChangerMaster(master):
            #on supprime l'etudiant de l'ancien master
            AncienMaster = TrouveMaster(ListeMaster, etu.pos)
            print("l'etudiant {} quitte le master {} ".format(etu.nom, AncienMaster.nom))
            del AncienMaster.etudiants[AncienMaster.etudiants.index(etu.nb)]
            AncienMaster.nombreEtudiant -= 1
            # on ajoute l'etudiant au nouveau master
            print("l'etudiant {} rentre dans le master {} ".format(etu.nom,master.nom))
            etu.pos = master.nom
            del master.listPref[0]
            master.etudiants.append(etu.nb)
            master.nombreEtudiant += 1
        else:
            print("l'etudiant {} ne change pas de master".format(etu.nom))
            del master.listPref[0]
            
            
        

def GaleShapleyMaster(M1,M2):
    ListeEtudiant = []
    ListeMaster = []
    for i in M1:
        ListeEtudiant.append(Etudiant(i))
    for i in M2:
        ListeMaster.append(Master(i))
    print(ListeMaster)
    print(ListeEtudiant)
    while MasterLibre(ListeMaster):
        print("---------------------------------------------- ")
        print("             NOUVEAU TOUR DE BOUCLE            ")
        print("---------------------------------------------- ")
        master = PremierMasterLibre(ListeMaster)
        #attention e est un nb
        Nbe = master.listPref[0]
        e = ListeEtudiant[Nbe]
        print("le master {} veut avoir l'etudiant {}".format(master.nom, e.nom))
        MasterProposeEtu(ListeMaster, master, e)
    print("----------------------------------------------")
    print("                RESULTAT FINAL                ")
    print("----------------------------------------------")
    for master in ListeMaster:
        print("le master {} a les etudiants {}".format(master.nom, master.etudiants))
        
    
M1 = PrefEtu('TestPrefEtu.txt')
M2 = PrefSpe('TestPrefSpe.txt')
#print(M1)
#print(M2)
#GaleShapley(M1,M2)
GaleShapleyMaster(M1,M2)
