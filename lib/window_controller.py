"""
    This module is managing the window and its animations
"""

from __future__ import absolute_import
from tkinter import Tk, Canvas
from random import randint
from PIL import Image, ImageTk


SPRITE = []

def load_sprites():
    """
        Loads the sprites
    """

    for i in ["PierreBleu", "PierreJaune", "PierreRouge", "PierreVerte", "animation_destruction"]:
        SPRITE.append(ImageTk.PhotoImage(Image.open("../sprite/"+i+".png")
                                         .resize((48, 48), Image.NEAREST)))


class WindowController(Tk):
    """
    Objet désignant la fenêtre root
    """
    def __init__(self):
        super().__init__()
        self["bg"] = "#73c2fa"
        self.geometry("1200x800")
        self.resizable(width=False, height=False)


class MenuPrincipal:
    """
    Décrit le menu principal
    """

    # Because this class manages tkinter things
    # pylint: disable=too-many-instance-attributes

    def __init__(self , root):
        self.root = root
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        # Logo
        self.original_logo = Image.open('../sprite/Logo.png').convert('RGB')
        self.image_logo = ImageTk.PhotoImage(self.original_logo.resize((400, 300), Image.NEAREST))
        self.logo = Canvas(root, height=300, width=400, borderwidth=0, highlightthickness=0)
        self.logo.create_image(0, 0, image=self.image_logo, anchor='nw')
        # BoutonJouer
        self.original_bouton1 = Image.open("../sprite/Bouton1.png")
        self.original_bouton2 = Image.open("../sprite/Bouton2.png")
        self.image_bouton1 = ImageTk.PhotoImage(self.original_bouton1.resize((400, 200),
                                                                             Image.NEAREST))
        self.image_bouton2 = ImageTk.PhotoImage(self.original_bouton2.resize((400, 200),
                                                                             Image.NEAREST))
        self.bouton = Canvas(root, height=200, width=400, borderwidth=0, highlightthickness=0)
        self.bouton.create_image(0, 0, image=self.image_bouton1, anchor="nw", tag="IMG")
        self.bouton.bind("<Enter>", self.enter_bouton)
        self.bouton.bind("<Leave>", self.leave_bouton)
        self.bouton.bind("<Button-1>", self.bouton_jouer_click)
        self.bouton.focus_set()
        self.logo.grid(row=0, column=0, sticky="n")
        self.bouton.grid(row=1, column=0, sticky="")

    def enter_bouton(self, _):
        """
            Animation d'entrer de la souris pour le bouton
        """

        self.bouton.delete("IMG")
        self.bouton.create_image(0, 0, image=self.image_bouton2, anchor="nw", tag="IMG")

    def leave_bouton(self, _):
        """
            Animation de sortie de la souris pour le bouton
        """

        self.bouton.delete("IMG")
        self.bouton.create_image(0, 0, image=self.image_bouton1, anchor="nw", tag="IMG")

    def leave_menu(self, _):
        """
        Fonction lancé pour détruire les éléments du menu
        """

        self.bouton.destroy()
        self.logo.destroy()

    def bouton_jouer_click(self, _):
        """
        Lancement du jeu, fermeture du menu
        """

        self.leave_menu(None)
        FenetreDeJeu(self.root).lancer_jeu()


class FenetreDeJeu():
    """
    Decris la fenêtre de jeu
    """

    def __init__(self,root):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)
        root.columnconfigure(16, weight=1)
        self.root = root
        self.grille_element = []
        self.focus = (None, None)
        self.grilledebas = genere_alea(3)

        load_sprites()

    def lancer_jeu(self):
        """
        Initialise le jeu
        """

        self.root.bind("<Button-3>", lambda x: self.backgroundclick())
        for (i, _element) in enumerate(self.grilledebas):
            ligne_element = []
            for j in range(len(self.grilledebas[0])):
                tmp = Canvas( height=50, width=50, bd=0, highlightthickness=0,bg="#73c2fa")
                tmp.create_image(0, 0, image=SPRITE[self.grilledebas[i][j]], anchor="nw", tag="nw")
                tmp.grid(row=i+1, column=j+1, padx=1, pady=1)
                tmp.bind("<Button-1>", lambda x, _i=i, _j=j: self.gemeclique(_i, _j,
                                                                    self.grilledebas[_i][_j]))
                ligne_element.append(tmp)
            self.grille_element.append(ligne_element)

    def backgroundclick(self):
        """
        Evenement si un clique hors grille est réalisé
        """

        if self.focus != (None, None):
            self.off_focus()
            self.focus = (None, None)

    def gemeclique(self, i, j, value):
        """
        Evenement si une gemme est cliqué
        """

        if self.focus == (None, None):
            self.focus = (i, j)
            self.on_focus(i, j)
        elif (i-self.focus[0])**2+(j-self.focus[1])**2 != 1:
            self.off_focus()
            self.focus = (i, j)
            self.on_focus(i, j)
        else:
            self.grilledebas[i][j], self.grilledebas[self.focus[0]][self.focus[1]] = \
                    self.grilledebas[self.focus[0]][self.focus[1]], self.grilledebas[i][j]
            self.regenere([[i, j], [self.focus[0], self.focus[1]]])
            self.off_focus()
            self.focus = (None, None)

        print(f"je suis une gemme de type { {0:'Bleu',1:'Jaune',2:'Rouge',3:'Verte'}[value]} "+\
                "aux coordonné {i} {j}")

    def on_focus(self, i, j):
        """
            Cette fonction va être suprimé, source: TKT
        """

        if not(j in (0, 14) or i in (0, 14)):
            self.grille_element[i-1][j].config(bg="#FFFFFF")
            self.grille_element[i+1][j].config(bg="#FFFFFF")
            self.grille_element[i][j+1].config(bg="#FFFFFF")
            self.grille_element[i][j-1].config(bg="#FFFFFF")

    def off_focus(self):
        """
            Cette fonction va être suprimé, source: TKT
        """

        i = self.focus[0]
        j = self.focus[1]
        print(i, j)
        if not(j in (0, 14) or i in (0, 14)):
            self.grille_element[i-1][j].config(bg="#73c2fa")
            self.grille_element[i+1][j].config(bg="#73c2fa")
            self.grille_element[i][j+1].config(bg="#73c2fa")
            self.grille_element[i][j-1].config(bg="#73c2fa")

    def regenere(self, liste_pos):
        """
            Liste de coordonné à actualiser ((1,2)(3,4))...
            Actualise les visuelles par rapport à la liste
        """

        for i, j in liste_pos:
            self.grille_element[i][j].delete("nw")
            self.grille_element[i][j].create_image(0, 0, image=SPRITE[self.grilledebas[i][j]],
                                                   anchor="nw", tag="nw")

    def destroy(self, i, j):
        """
            Permet de detruire une case aux coordonnées i,j
        """

        self.grilledebas[i][j] = 4
        self.regenere([(i, j)])

def genere_alea(nb_max):
    """
    Fonction temporaire
    """
    return [[randint(0, nb_max) for i in range(15)] for j in range(15)]
if __name__ == "__main__":
    Fenetre = WindowController()
    menu = MenuPrincipal(Fenetre)
    menu.root.mainloop()
