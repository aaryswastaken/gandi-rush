""" Utilisation de ce module pour la génération aléatoire """
from random import randint
from math import log10

class Grille():
    """
        Classe de gestion de la grille
    """

    def __init__(self):
        self.grille = []
        self.nb_max = 0

    def genere_alea(self, taille_x, taille_y, nb_max):
        """
            genere_alea: Génère aléatoirement une nouvelle grille

            Parametres:
                taille_x (int): la largeur
                taille_y (int): la hauteur
                nb_max (int): le nombre de bonbons

            Renvoie:
                None
        """
        self.grille = [[randint(1, nb_max) for j in range(taille_y)] for i in range(taille_x)]
        self.nb_max = nb_max

    def affiche_grille(self, charset=None):
        """
            affiche_grille: Affiche la grille

            Parametres:
                charset (str[]): Les caractères a afficher

            Renvoie:
                None
        """

        if charset is None:
            charset = [str(i+1) for i in range(self.nb_max)]

        height = len(self.grille)
        width = len(self.grille[0])

        for (i, slc) in enumerate(self.grille):
            print(f"{height-i: >{int(log10(height))+3}} : "+" ".join([charset[e-1] for e in slc]))

        print()

        n_lines = int(log10(width))+1

        for i in range(n_lines):
            print(" "*(int(log10(height))+6), end="")
            for j in range(width):
                n_to_print = ((j+1) // (10**(n_lines - i - 1))) % 10

                print(n_to_print, end=" ")

            print("", end="\n")


class Physique():
    """
        Classe qui gère la physique du jeu
    """

    def __init__(self, grille, mode=3):
        self.grille = grille
        self.mode = mode

    def get_mode(self):
        """
            get_mode: Pour rendre pylint content

            Parametres:
                None

            Renvoie:
                mode (int): mode de physique
        """
        return self.mode

    def __tick_mode_3(self):
        """
            tick_mode_3 (private): Tick mais pour le mode 3
        """


    def tick(self):
        """
            tick: Actualise la grille selon le mode de jeu

            Parametres:
                None

            Renvoie:
                None
        """

        if self.mode == 3:
            self.__tick_mode_3()

        return None


if __name__ == "__main__":
    grid = Grille()

    grid.genere_alea(5, 5, 4)
    grid.affiche_grille(charset=["-", "+", "*", "o"])
