import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

###############################################################################
# création de la fenetre principale  - ne pas toucher

LARG = 300
HAUT = 300

Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("ESIEE - Morpion")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="black" )
canvas.place(x=0,y=0)


#################################################################################
#
#  Parametres du jeu
 
Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
           
PlayerTurn = True # True = joueur, False = IA

###############################################################################
def GameState():
    # Victoire de l'Humain
    if(
        Grille[0][0] == 1 and Grille[0][1] == 1 and Grille[0][2] == 1 or
        Grille[1][0] == 1 and Grille[1][1] == 1 and Grille[1][2] == 1 or
        Grille[2][0] == 1 and Grille[2][1] == 1 and Grille[2][2] == 1 or
        Grille[0][0] == 1 and Grille[1][0] == 1 and Grille[2][0] == 1 or
        Grille[0][1] == 1 and Grille[1][1] == 1 and Grille[2][1] == 1 or
        Grille[0][2] == 1 and Grille[1][2] == 1 and Grille[2][2] == 1 or
        Grille[0][0] == 1 and Grille[1][1] == 1 and Grille[2][2] == 1 or
        Grille[0][2] == 1 and Grille[1][1] == 1 and Grille[2][0] == 1
    ):
        return 1
    # Victoire de l'IA
    elif(
        Grille[0][0] == 2 and Grille[0][1] == 2 and Grille[0][2] == 2 or
        Grille[1][0] == 2 and Grille[1][1] == 2 and Grille[1][2] == 2 or
        Grille[2][0] == 2 and Grille[2][1] == 2 and Grille[2][2] == 2 or
        Grille[0][0] == 2 and Grille[1][0] == 2 and Grille[2][0] == 2 or
        Grille[0][1] == 2 and Grille[1][1] == 2 and Grille[2][1] == 2 or
        Grille[0][2] == 2 and Grille[1][2] == 2 and Grille[2][2] == 2 or
        Grille[0][0] == 2 and Grille[1][1] == 2 and Grille[2][2] == 2 or
        Grille[0][2] == 2 and Grille[1][1] == 2 and Grille[2][0] == 2
    ):
        return 2
    # Match nul
    elif(
        Grille[0][0] != 0 and Grille[0][1] != 0 and Grille[0][2] != 0 and
        Grille[1][0] != 0 and Grille[1][1] != 0 and Grille[1][2] != 0 and
        Grille[2][0] != 0 and Grille[2][1] != 0 and Grille[2][2] != 0
    ):
        return 0
    # Partie en cours
    else:
        return 3

def WinningCase(): 
    if(GameState() == 1):
        canvas.itemconfig("line", fill="red")
        messagebox.showinfo("Victoire", "Vous avez gagné !")
        Window.destroy()
    elif(GameState() == 2):
        canvas.itemconfig("line", fill="yellow")
        messagebox.showinfo("Défaite", "Vous avez perdu !")
        Window.destroy()
    elif(GameState() == 0):
        canvas.itemconfig("line", fill="white")
        messagebox.showinfo("Egalité", "Match nul !")
        Window.destroy()

def CalculCoupsPossibles(): 
    ListeCoupsPossibles = []
    for x in range (3):
        for y in range (3):
            if(Grille[x][y] == 0):
                ListeCoupsPossibles.append([x,y])

    return ListeCoupsPossibles

def JoueurSimuleIA(Grille):
    ListeCoupsPossibles = CalculCoupsPossibles()
    Resultat = []
    if(GameState() == 1 or GameState() == 2):
        return (-1,0)
    if(GameState() == 0):
        return (0,0)
    for CoupPossible in ListeCoupsPossibles:
        Grille[CoupPossible[0]][CoupPossible[1]] = 2
        R = JoueurSimuleHumain(Grille)
        Resultat.append(R[0])
        Grille[CoupPossible[0]][CoupPossible[1]] = 0
        MeilleurCoupPossible = (max(Resultat),Resultat.index(max(Resultat)))
    return MeilleurCoupPossible

def JoueurSimuleHumain(Grille):
    ListeCoupsPossibles = CalculCoupsPossibles()
    Resultat =[]
    if(GameState() == 1 or GameState() == 2):
        return (1,0)
    if(GameState() == 0):
        return (0,0)
    for CoupPossible in ListeCoupsPossibles:
        Grille[CoupPossible[0]][CoupPossible[1]] = 1
        R = JoueurSimuleIA(Grille)
        Resultat.append(R[0])
        Grille[CoupPossible[0]][CoupPossible[1]] = 0
        MeilleurCoupPossible = (min(Resultat),Resultat.index(min(Resultat)))
    return MeilleurCoupPossible

def Play(x,y):        

    if (GameState() == 3) :
        if (Grille[x][y] == 0):
            Grille[x][y] = 1
            if (GameState() == 3) :
                ListeCoupsPossibles = CalculCoupsPossibles()
                print(ListeCoupsPossibles)
                print(JoueurSimuleIA(Grille))
                Grille[ListeCoupsPossibles[JoueurSimuleIA(Grille)[1]][0]][ListeCoupsPossibles[JoueurSimuleIA(Grille)[1]][1]] = 2
    else: 
        WinningCase()
################################################################################
#    
# Dessine la grille de jeu

def Dessine(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        
        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill="blue", width="4", tag = "line" )
            canvas.create_line(0,i*100,300,i*100,fill="blue", width="4", tag = "line" )
            
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
    
####################################################################################
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
   
    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
     
    print("clicked at", x,y)
    
    Play(x,y)  # gestion du joueur humain et de l'IA
    
    Dessine()
    
canvas.bind('<ButtonPress-1>',    MouseClick)

#####################################################################################
#
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()

Window.mainloop()


































