"""
    This module is managing the window and its animations

    Author: @Byllie, @aaryswastaken
    Created Date: 03/14/2023
"""

from __future__ import absolute_import

import os
from threading import Thread
from time import sleep

from tkinter import Canvas, StringVar, Label, Tk
from random import randint
from PIL import Image, ImageTk
from lib.event_pool_controller import Event


SPRITE = {}

def load_sprites(sprite_home):
    """
        Loads the sprites
    """

    for i in os.listdir(sprite_home):
        SPRITE[i]=(ImageTk.PhotoImage(Image.open(sprite_home+i).resize((48, 48), Image.NEAREST)))

def configure_window(root):
    """
    :param Fenetre TK:
    :return None:
    Configure la fenêtre
    """

    root["bg"] = "#73c2fa"
    root.geometry("1200x800")
    root.resizable(width=False, height=False)


class MenuPrincipal:
    """
    Décrit le menu principal
    """

    # Because this class manages tkinter things
    # pylint: disable=too-many-instance-attributes

    def __init__(self, root,grille,event_pool,sprite_home="../sprite/"):
        self.root = root
        self.jeu=FenetreDeJeu(self.root, sprite_home, grille, event_pool)
        root.columnconfigure(0,)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        self.grille=grille
        # Logo
        self.original_logo = Image.open(sprite_home+'Logo.png').convert('RGB')
        self.image_logo = ImageTk.PhotoImage(self.original_logo.resize((400, 300), Image.NEAREST))
        self.logo = Canvas(root, height=300, width=400, borderwidth=0, highlightthickness=0)
        self.logo.create_image(0, 0, image=self.image_logo, anchor='nw')
        # BoutonJouer
        self.original_bouton1 = Image.open(sprite_home+"Bouton1.png")
        self.original_bouton2 = Image.open(sprite_home+"Bouton2.png")
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
        self.logo.grid(row=0, column=1, sticky="n")
        self.bouton.grid(row=1, column=1, sticky="n")

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
        self.jeu.lancer_jeu()


class FenetreDeJeu():
    """
    Decris la fenêtre de jeu
    """

    def __init__(self, root, sprite_home, grille, event_pool):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)
        root.columnconfigure(16, weight=1)
        self.score = None
        self.root = root
        self.grille_element = []
        self.focus = (None, None)
        self.grille_de_base = grille
        load_sprites(sprite_home)
        self.event_pool=event_pool

    def lancer_jeu(self):
        """
            Initialise le jeu
        """

        thread_one=Thread(target=self.event_clock)
        thread_one.start()
        self.score = StringVar()
        text_score = Label(textvariable=self.score, bg="#73c2fa", font=("TkTooltipFont",25),
                           fg='#45283c')
        self.score.set("Score : 0")
        text_score.grid(row=1, column=0)
        #where the lag is
        for (i, _element) in enumerate(self.grille_de_base):
            ligne_element = []
            for j in range(len(self.grille_de_base[0])):
                tmp = Canvas(height=50, width=50, bd=0, highlightthickness=0, bg="#73c2fa")
                tmp.create_image(0, 0, image=SPRITE["30"+str(self.grille_de_base[i][j])+".png"],
                                 anchor="nw", tag="nw")
                tmp.grid(row=i+1, column=j+1, padx=1, pady=1)
                tmp.bind("<Button-1>", lambda _x, _i=i, _j=j:
                         self.gemeclique(_i, _j))
                ligne_element.append(tmp)
            self.grille_element.append(ligne_element)

    def event_clock(self):
        """
            Function triggered to see events
        """

        while True:
            event = self.event_pool.next_and_delete(1)
            if event is not None:
                if event.msg_type==1:
                    print("REFRESH")
                if event.msg_type==2:
                    print("UPDATE",hex(event.payload['new_gem']))
                    self.grille_element \
                        [event.payload['coordinates'][1]] \
                        [event.payload['coordinates'][0]] \
                        .delete("nw")
                    self.grille_element \
                        [event.payload['coordinates'][1]] \
                        [event.payload['coordinates'][0]] \
                        .create_image(0, 0, image=SPRITE[hex(event.payload['new_gem'])[2::]+".png"],
                                      anchor="nw", tag="nw")
                if event.msg_type==4:
                    print("SCORE")
                    payload_score = event.payload["score"]
                    self.score.set(f"Score: {payload_score}")

    def backgroundclick(self):
        """
            Evenement si un clique hors grille est réalisé
        """

        if self.focus != (None, None):
            self.off_focus()
            self.focus = (None, None)

    def gemeclique(self, i, j):
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
            self.event_pool.push(Event(0,Event.TYPE_GRID_PERMUTATION,
                                       {"permutation":((j,i),(self.focus[1],self.focus[0]))}))

            self.off_focus()
            self.focus = (None, None)


    def on_focus(self, i, j):
        """
            Cette fonction va être suprimé, source: TKT
        """

        try:
            self.grille_element[i-1][j].config(bg="#FFFFFF")
            self.grille_element[i+1][j].config(bg="#FFFFFF")
            self.grille_element[i][j+1].config(bg="#FFFFFF")
            self.grille_element[i][j-1].config(bg="#FFFFFF")
        except IndexError:
            pass

    def off_focus(self):
        """
            Cette fonction va être suprimé, source: TKT
        """

        i = self.focus[0]
        j = self.focus[1]
        try:
            self.grille_element[int(i-1)][int(j)].config(bg="#73c2fa")
            self.grille_element[int(i+1)][int(j)].config(bg="#73c2fa")
            self.grille_element[int(i)][int(j+1)].config(bg="#73c2fa")
            self.grille_element[int(i)][int(j-1)].config(bg="#73c2fa")
        except IndexError:
            pass

    def regenere(self, liste_pos):
        """
            Liste de coordonné à actualiser ((1,2)(3,4))...
            Actualise les visuelles par rapport à la liste
        """

        for i, j in liste_pos:
            self.grille_element[i][j].delete("nw")
            self.grille_element[i][j].create_image(0, 0,
                                                   image=SPRITE["00"+
                                                                str(self.grille_de_base[i][j])+
                                                                ".png"],
                                                   anchor="nw", tag="nw")


def genere_alea(nb_max):
    """
        Fonction temporaire
    """

    return [[randint(1, nb_max+1) for i in range(15)] for j in range(15)]

def main_loop(event_pool, sprite_home, _grid_manager):
    """
        Main loop of the file
    """

    window = Tk()
    configure_window(window)
    event_pool.push(Event(0,Event.TYPE_GEN_TRIGGER,{"grid_size":(15,15)}))
    sleep(0.5)
    tab = event_pool.next_and_delete(1).payload["grid"]
    menu = MenuPrincipal(window, tab, event_pool, sprite_home=sprite_home)
    menu.root.mainloop()
