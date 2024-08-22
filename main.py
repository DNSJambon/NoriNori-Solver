"""
Programme principal:
Interface graphique avec tkinter qui permet de creer une grille de jeu et de la resoudre 
ou de resoudre une grille existante.
"""



import tkinter as tk
import SAT_solve as sat
import instance_en_DIMACS as id
import argparse
global zone
global compteur
global fichier
zone=[]
compteur=0


#fonctions d'evenements interface
def ajouter(event):
   global zone
   x, y = root.winfo_pointerx()-root.winfo_rootx(), root.winfo_pointery()-root.winfo_rooty()
   if x<80 or x>620 or y<30 or y>570:
      return
   case = canvas.find_closest(x, y)[0]

   # si la case est desactivée, elle est déjà dans une zone, donc on ne peut pas la modifier
   if canvas.itemcget(case, 'state') != 'disabled':
      canvas.itemconfigure(case, fill=cases)
      if case not in zone:
         zone.append(case)


def retirer(event):
   global zone
   x, y = root.winfo_pointerx()-root.winfo_rootx(), root.winfo_pointery()-root.winfo_rooty()
   if x<80 or x>620 or y<30 or y>570:
      return
   case = canvas.find_closest(x, y)[0]
   
   if canvas.itemcget(case, 'state') != 'disabled':
      canvas.itemconfigure(case, fill=bg)
      if case in zone:
         zone.remove(case)

#ajouter une zone:
def valider_zone():
   if fichier.closed:
      return

   global zone
   global compteur
   for case in zone:
      compteur+=1
      canvas.itemconfigure(case, fill=bg)

      #on ecrit les bonnes coordonnées dans le fichier
      x1, y1, x2, y2 = canvas.coords(case)
      i,j = d[(x1,y1)]
      fichier.write(str(i)+" "+str(j)+"\n")

      #on trace le contour de la zone:
      if case-1 not in zone:
         canvas.create_line(x1, y1, x1, y2, width=5, fill=bord, state="disabled")
      if case+1 not in zone:
         canvas.create_line(x2, y1, x2, y2, width=5, fill=bord, state="disabled")
      if case-n not in zone:
         canvas.create_line(x1, y1, x2, y1, width=5, fill=bord, state="disabled")
      if case+n not in zone:
         canvas.create_line(x1, y2, x2, y2, width=5, fill=bord, state="disabled")

      #marquer la case comme desactivée:
      canvas.itemconfigure(case, state="disabled")


   fichier.write("#\n")
   zone=[]


#afficher la solution:
def afficher_solution():
   if fichier.closed:
      return

   if compteur != n*n:
      print("Vous n'avez pas fini de remplir la grille")   
      #on affiche les cases manquantes en rouge:
      for i in range(1,n*n+1):
         if canvas.itemcget(i, 'state') != 'disabled' and canvas.itemcget(i, 'fill') != cases:
            canvas.itemconfigure(i, fill='#FFA2A2') 
      return
   
   fichier.close()
   solution = sat.solveur("grilles_made/grille"+str(n))
   #on colorie les cases de la solution:
   for case in solution:
      if case>0:
         canvas.itemconfigure(case, fill=cases)
   if solution == []:
      for i in range (n**2):
         canvas.itemconfigure(i+1, fill='#FFA2A2')
      

#fonction pour remmetre a zero la grille:
def reset():
   global fichier
   global zone
   global compteur
   zone=[]
   compteur=0
   fichier.close()
   fichier = open("grilles_made/grille"+str(n)+".txt", "w")
   fichier.write(str(n)+"\n")
   #supprimer tous les objets crées apres la grille:
   for i in range(n*n+2, canvas.find_all()[-1]+1):
      canvas.delete(i)
   #remettre les cases en blanc:
   for i in range(1,n*n+1):
      canvas.itemconfigure(i, fill=bg)
      canvas.itemconfigure(i, state="normal")



if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Solveur NoriNori')
   parser.add_argument('grid_size', type=int, help='Taille de la grille')
   
   args = parser.parse_args()
   
   n = args.grid_size

   #couleurs interface:
   cases = '#15699F'
   bg = '#DDE6ED'
   bord = '#203046'


   taille = 550 / n
   fichier = open("grilles_made/grille"+str(n)+'.txt' , "w")
   fichier.write(str(n)+"\n")


   # Crée la fenêtre principale et le canevas pour la grille
   root = tk.Tk()
   root.title("Solveur NoriNori")
   root.geometry("700x700+{}+{}".format(root.winfo_screenwidth()//2-350, root.winfo_screenheight()//2-450))
   root.attributes('-topmost', 1)
   canvas = tk.Canvas(root, width=700, height=700, bg=bg)
   canvas.pack()


   #dict pour associer les coordonnées des cases sur la fenetre a leur coordonnées dans la grille:
   #(la premiere case est en (0,0) sur la grille mais l'objet est en (75,25) sur la fenetre graphique)
   d={}
   # Dessine la grille
   for i in range(n):
      for j in range(n):
            x1, y1 = j*taille+75 , i*taille+25
            x2, y2 = x1+taille, y1+taille
            d[(x1,y1)] = (i,j)       

            case = canvas.create_rectangle(x1, y1, x2, y2, fill=bg, width=1, outline=bord )
            #effet de grossissement de la case au survol:
            canvas.tag_bind(case, '<Enter>', lambda event, case=case: canvas.itemconfigure(case, width=2))
            canvas.tag_bind(case, '<Leave>', lambda event, case=case: canvas.itemconfigure(case, width=1))
   canvas.create_rectangle(75, 25, 625, 575, width=5, outline=bord)




   #bouton pour valider la zone:

   canvas.bind('<B1-Motion>', lambda event: ajouter(event))
   canvas.bind('<B3-Motion>', lambda event: retirer(event))
   canvas.bind('<Button-1>', lambda event: ajouter(event))
   canvas.bind('<Button-3>', lambda event: retirer(event))

   bouton = tk.Button(root, text="Créér une zone" , width=15, height=3, bg="#2F4767", fg="#F1F6F9", relief="flat")
   bouton.pack()
   bouton.place(x=90, y=610)
   bouton.bind('<Button-1>', lambda event: valider_zone())

   #bouton pour valider la grille:
   bouton2 = tk.Button(root, text="Afficher la solution", width=15, height=3, bg="#2F4767", fg="#F1F6F9", relief="flat")
   bouton2.pack()
   bouton2.place(x=292, y=610)
   bouton2.bind('<Button-1>', lambda event: afficher_solution())

   #bouton reset:
   bouton3 = tk.Button(root, text="Recommencer", width=15, height=3, bg="#2F4767", fg="#F1F6F9", relief="flat")
   bouton3.pack()
   bouton3.place(x=500, y=610)
   #bind pour appeler la fonction reset et reinitialiser le fichier:
   bouton3.bind('<Button-1>', lambda event: reset())


   root.mainloop()

"""
bleu:
cases = '#125887'
bg = '#DCEFFC'
bord = '#1B262C'
"""

