"""
    This modules focuses on the grid management

    Author: @aaryswastaken
    Created Date: 03/13/2023
"""

# Importing modules for the GridManager Thread
from __future__ import absolute_import
from threading import Thread


class GridManager(Thread):
    """
        This class manages the grid and its physics
    """

    def __init__(self):
        super().__init__(self)

    def init_grid_random(self, size_x, size_y):
        """
            /!\\ DEPRECATED /!\\

            Generates a random grid of requested dimentions

            Parameters:
                size_x (int)
                size_y (int)

            Returns:
                None
        """

    def stop(self):
        """
            Stops the thread
        """

    def run(self):
        """
            Main loop
        """

    def permute(self, permutation):
        """
            permute: Permute (assume que la permutation est légale)
            Parametres:
                permutation (tuple<tuple<int>>)
            Renvoie:
                None
        """

    def transpose(self):
        """
            transpose: Transpose la grille
            Parametres:
                None
            Renvoie:
                transposed (int[][]): La grille transposée
        """

    def from_transposed(self, transposed):
        """
            from_transposed: Remplace la grille active par la transposition inverse
            Parametres:
                transposed (int[][]): Une matrice transposée
            Renvoie:
                None
        """

    def clone(self):
        """
            clone: Clone la grille pour sauvegarde
            Parametres:
                None
            Renvoie:
                grille_clone (int[][]): Le clone de la grille
        """

    def do_compare(self, grille):
        """
            do_compare: Compare la grille a une autre pour voir si il y a une difference
            Parametres:
                grille (int[][]): La grille a comparer
            Renvoie:
                res (bool): True si différentes
        """

    def detecte_coordonnees_combinaison(self, i, j):
        """
            detecte_coordonnees_combinaison: Renvoie une liste des item adjacent de meme nature
            Note: Il est absurde d'écrire cette fonction en dehors d'une classe mais c'est pour
            le respect du sujet
            Parametres:
                grille (Grille): la grille
                i (int): coordonnees en x
                j (int): coordonnees en y
            Renvoie:
                out (tuple<int>[]): les cases adjacentes
        """
