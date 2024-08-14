"""
Ce programme demande le nom d'un fichier txt au bon format dans le dossier "grilles"
et cree un fichier DIMACS representant le probleme SAT correspondant.
"""

import os

def voisin(x):
    """
    Cette fonction prend en argument une case de la grille et renvoie 
    ses 4 voisins (Nord, Sud, Est et Ouest).
    """
    return [(x[0]+1,x[1]),(x[0]-1,x[1]),(x[0],x[1]+1),(x[0],x[1]-1)]


def fichier_instance_en_zones(fichier_instance):
    """
    Cette fonction prend en argument le nom d'un fichier representant une grille
    et renvoie la dimension et les zones de la grille sous forme de liste.
    """

    # recuperation de toutes les lignes du fichier,
    # la premiere ligne est la dimension de la grille, les autres sont les coordonnees pour chaque zone:
    fichier = open(fichier_instance, "r")
    lignes = fichier.readlines()
    fichier.close()

    dimension = int(lignes[0])
    lignes = [line.rstrip('\n') for line in lignes]
    lignes = lignes[1:]

    # puis on separe la grille en plusieurs listes (les zones) grace aux separateurs #:
    zones=[]
    j=0
    for i in range(lignes.count("#")):
        zones.append([])

        while lignes[j]!="#":
            zones[i].append(lignes[j])
            j+=1   
        j+=1
        
    if j != dimension*dimension+lignes.count("#") or lignes.count("#")==0:
        print("Erreur de format textuel")
        exit()

    # on transforme les coordonnees des zones en tuples pour pouvoir traiter les entiers:
    for i in range(len(zones)):
        for j in range(len(zones[i])):
            zones[i][j]=tuple(map(int,zones[i][j].split()))[:2]

    return dimension,zones

def probleme_en_DIMACS(dimension,zones, nom):
    """
    cree un fichier DIMACS a partir de la dimension d'une grille, de ses zones 
    et du nom du fichier (sans l'extennsion) à créer
    """
    
    # on associe a chaque case de la grille un entier 
    # (representant les variable pour le fichier DIMAC) grace a un dictionnaire:
    d={}
    x=1
    for i in range(dimension):
        for j in range(dimension):
            d[(i,j)]=x
            x+=1
    #calcul du nombre de clauses:
    clauses=0
    #hypothese 1:
    for i in range(len(zones)):
        clauses+=len(zones[i])*(len(zones[i])-1)*(len(zones[i])-2)
        clauses+=len(zones[i])
    #hypothese 2:
    for i in d:
        #nombre de voisins effectifs de i (qui sont dans la grille):
        v=[v for v in voisin(i) if v in d]    
        clauses+=len(v)*(len(v)-1)
        clauses+=1


    #cree un fichier et ecrire "p cnf dimension*dimension clauses"
    fichier = open(nom , "w")
    fichier.write("p cnf "+str(dimension*dimension)+" "+str(clauses)+"\n")

    #hypothese 1: chaque zone contient exactement deux cases coloriees:
    for n in range(len(zones)):
        #x ∈ Zn
        for x in zones[n]:
            #y ∈ Zn-x
            for y in [y for y in zones[n] if y!=x]:
                #z ∈ Zn-x-y
                for z in [z for z in zones[n] if z!=x and z!=y]:
                    fichier.write("-"+str(d[x])+" -"+str(d[y])+" -"+str(d[z])+' 0\n')
                    
        
        #x ∈ Zn
        for x in zones[n]:
            #y ∈ Zn-x
            for y in [y for y in zones[n] if y!=x]:
                fichier.write(str(d[y])+' ')

            fichier.write('0\n')

    #hypothese 2: chaque case coloriee a exactement un voisins colorie:

    #x∈K2
    for x in d:
        #v1∈Px
        for v1 in voisin(x):
            #v2∈(Px−v1)
            for v2 in [v2 for v2 in voisin(x) if v2!=v1]:
                #on ne prend pas en compte les voisins qui ne sont pas dans la grille:
                if v1 in d and v2 in d:
                    fichier.write("-"+str(d[x])+" -"+str(d[v1])+" -"+str(d[v2])+' 0\n')
        
        
        fichier.write('-'+str(d[x])+' ')
        #v∈Px
        for v in voisin(x):
            if v in d:
                fichier.write(str(d[v])+' ')
        fichier.write('0\n')

    fichier.close()
    return


def main():
    print("\033c")
    nom = input("Entrez le nom du fichier representant la grille: ")
    if '.txt' not in nom:
        nom += '.txt'

    while nom not in os.listdir('grilles'):
        print("Le fichier n'existe pas!")
        nom = input("Entrez le nom du fichier representant la grille: ")
        if '.txt' not in nom:
            nom += '.txt'

    fichier = "grilles/"+nom

    probleme_en_DIMACS(*fichier_instance_en_zones(fichier), fichier[:-4]+".cnf")
    print("Fichier DIMACS cree avec succes!")

if __name__ == "__main__":
    main()