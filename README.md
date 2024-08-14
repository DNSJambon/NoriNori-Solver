# Projet INF402 - Solveur de NoriNori


## Utilisation
`python main.py`

Le programme principal `main` comporte 2 modes
- à partir l'instance d'un probleme (.txt à placer dans \grilles au format indiqué ci-dessous), affiche la solution de maniere comprehensible à l'écran.

- Il est également possible de créér manuellement une instance de probleme de maniere visuelle grace à ce programme.

## format des instances
pour une grille de taille N x N, le fichier grilleN.txt est de la forme:

```
N 
a1 b1\n
...
an  bn
#
c1 d1
...
cn dn
#
```

Les `#` permettent de séparer une zone d'une autre, toute les cases d'une zone doivent donc etre inscrites à la suite sans etre séparées par un `#`.
Exemple sur une grille 4 x 4 comportant simplement 4 zones (les 4 bandes horizontales)
```
4
0 0
0 1
0 2
0 3
#
1 0
1 1
1 2
1 3
#
2 0
2 1
2 2
2 3
#
3 0
3 1
3 2
3 3
#
```


## !! IMPORTANT !!
Les modules python necessaires au bon fonctionnement de l'ensemble du projet sont:   
- pysat
- tkinter
- os
