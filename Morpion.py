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
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

def Winning():
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
    elif(
        Grille[0][0] != 0 and Grille[0][1] != 0 and Grille[0][2] != 0 and
        Grille[1][0] != 0 and Grille[1][1] != 0 and Grille[1][2] != 0 and
        Grille[2][0] != 0 and Grille[2][1] != 0 and Grille[2][2] != 0
    ):
        return 0

def Play(x,y):     
    if(Grille[x][y] == 0):
        if(PlayerTurn == True):    
            Grille[x][y] = 1
        elif(PlayerTurn == False):
            #Grille[x][y] = 2
            Grille[JoueurSimuleIA[0]][JoueurSimuleIA[1]] = 2


def WinningCase(): 
    if(Winning() == 1):
        canvas.itemconfig("line", fill="red")
        messagebox.showinfo("Victoire", "Vous avez gagné !")
        Window.destroy()
    elif(Winning() == 2):
        canvas.itemconfig("line", fill="yellow")
        messagebox.showinfo("Défaite", "Vous avez perdu !")
        Window.destroy()
    elif(Winning() == 0):
        canvas.itemconfig("line", fill="white")
        messagebox.showinfo("Egalité", "Match nul !")
        Window.destroy()
   
def JoueurSimuleIA(): 
    # Si la partie est finie, on retourne le résultat
    if(Winning() == 1 or Winning() == 2):
        return Winning()
    
    # Sinon, on simule tous les coups possibles
    # On définit les listes stockants tous les coups possibles et les résultats
    ListeCoupsPossibles = []
    Resultats = []
    
    # On parcourt la grille pour trouver les coups possibles
    for x in range(3):
        for y in range(3):
            if(Grille[x][y] == 0):
                ListeCoupsPossibles.append([x,y])
            
    # On parcourt tous les coups possibles 
    for CoupPossible in ListeCoupsPossibles:
        # On joue le coup K
        Grille[CoupPossible[0]][CoupPossible[1]] = 2

        # On simule le coup de l'IA
        R = JoueurSimuleHumain()

        # On stocke le résultat 
        Resultats.append([R, CoupPossible])

        # On annule le coup K (on retire le pion)
        Grille[CoupPossible[0]][CoupPossible[1]] = 0

        MeilleurCoup = (min(Resultats), Resultats.index(min(Resultats)))

    # On retourne le meilleur coup de Resultats
    return MeilleurCoup
    

def JoueurSimuleHumain():
    # Si la partie est finie, on retourne le résultat
    if(Winning() == 1 or Winning() == 2):
        return Winning()
    
    # Sinon, on simule tous les coups possibles
    # On définit les listes stockants tous les coups possibles et les résultats
    ListeCoupsPossibles = []
    Resultats = []
    
    # On parcourt la grille pour trouver les coups possibles
    for x in range(3):
        for y in range(3):
            if(Grille[x][y] == 0):
                ListeCoupsPossibles.append([x,y])
            
    # On parcourt tous les coups possibles 
    for CoupPossible in ListeCoupsPossibles:
        # On joue le coup K
        Grille[CoupPossible[0]][CoupPossible[1]] = 1

        # On simule le coup de l'IA
        R = JoueurSimuleIA()

        # On stocke le résultat 
        Resultats.append([JoueurSimuleIA(), CoupPossible])

        # On annule le coup K (on retire le pion)
        Grille[CoupPossible[0]][CoupPossible[1]] = 0

        MeilleurCoup = (min(Resultats), Resultats.index(min(Resultats)))


    # On retourne le meilleur coup
    return MeilleurCoup




                
          
    

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
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
    global PlayerTurn
    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
     
    
    print("clicked at", x,y)
    
    Play(x,y)  # gestion du joueur humain et de l'IA
    PlayerTurn = not PlayerTurn
    
    Dessine()

    WinningCase()

canvas.bind('<ButtonPress-1>',    MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()
Window.mainloop()