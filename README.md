# Project INF402 - NoriNori Solver

## Usage
`python main.py <grid_size>`

The grid will be a square of side `grid_size`

You can create and display the solution of any NoriNori instance easily using this program.

## More details : Format of Instances
For a grid of size N x N, the file `grilleN.txt` is in the following format:

```
N 
a1 b1
.
.
.
an bn
#
c1 d1
.
.
.
cn dn
#
.
.
.
#
```

The `#` symbols separate one zone from another. Therefore, all the cells in a zone must be listed consecutively without being separated by a `#`.
Example for a 4 x 4 grid with 4 zones (the 4 horizontal strips):
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
The necessary Python modules for the proper functioning of the entire project are:
- pysat
- tkinter
- os
