"""
Ce programme demande le nom d'un fichier txt dans le dossier "grilles"
et renvoie une solution du probleme sous forme liste d'entiers.

La liste contient les n ou -n avec n allant de 1 à dimension^2
(la case n=1 represente la case (0,0) de la grille et la case n=dimension^2 
represente la case (dimension-1,dimension-1) de la grille).

Par exemple, la solution [1,2,-3,-4,-5,-6,-7,-8,-9] represente une grille de dimension 3
dont la solution comporte seulement les 2 premieres cases (0,0) et (0,1) coloriees:

##.
...
...


"""

import os
import instance_en_DIMACS as id
from pysat.solvers import Minisat22
#on utilise le solveur minisat 2.2.0:


def solveur(nom):
    """
    Cette fonction prend en argument le nom d'un fichier representant une grille (sans l'extension)
    et renvoie une solution du probleme sous forme liste d'entiers. 
    """
    solveur = Minisat22()

    #creation du fichier DIMACS:
    dimension, zones = id.fichier_instance_en_zones(nom+".txt")
    id.probleme_en_DIMACS(dimension, zones, nom+".cnf")


    # lecture du fichier DIMACS:
    with open(nom+".cnf", 'r') as f:
        cnf = f.readlines()
        f.close()

    for ligne in cnf:
        if ligne.startswith('c') or ligne.startswith('p'):
            continue
        clause = [int(lit) for lit in ligne.split() if lit != '0']
        solveur.add_clause(clause)

    # affichage de la solution:
    sat = solveur.solve()
    if sat:
        print('La grille a une solution:')
        solution = solveur.get_model()

        return solution

    else:
        print('La grille n\'a pas de solution.')
        return []




def main():
    print("\033c")
    nom = input("Entrez le nom du fichier representant la grille: ")
    if nom.endswith(".txt"):
        nom = nom[:-4]

    while nom+".txt" not in os.listdir("grilles"):
        print("Le fichier n'existe pas!")
        nom = input("Entrez le nom du fichier representant la grille: ")
        if nom.endswith(".txt"):
            nom = nom[:-4]

    nom = "grilles/"+nom
    solution = solveur(nom)
    print(solution)

if __name__ == "__main__":
    main()
