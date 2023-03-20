"""
    This modules focuses on the grid management

    Author: @aaryswastaken
    Created Date: 03/13/2023
"""

# Importing modules for the GridManager Thread
from __future__ import absolute_import
from threading import Thread


def explore_adj(_grille, pos_x, pos_y, scanned_value):
    """
        explore_adj: Renvoie True si la valeur du tableau aux coordonnees indiquees est celle
            requise. Renvoie False si l'index existe pas
        Parametres:
            _grille (t[][]): Le tableau a chercher
            pos_x (int): la position en x
            pos_y (int): la position en y
            scanned_value (t): La valeur comparee
        Renvoie:
            out (bool): Si la condition est complete
    """

    if pos_x < 0 or pos_y < 0:
        return False

    try:
        return _grille[pos_y][pos_x] == scanned_value
    except IndexError:
        return False


class GridManager(Thread):
    """
        This class manages the grid and its physics
    """

    def __init__(self):
        super().__init__(self)
        self.grid = []

        self.thread_stop_flag = False

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

        self.grid = [[0 for i in range(size_y)] for j in range(size_x)]

    def stop(self):
        """
            Stops the thread
        """

        self.thread_stop_flag = True

    def run(self):
        """
            Main loop
        """

    # Following code is going to be yoinked from sujet_origine.py
    def permute(self, permutation):
        """
            permute: Permute (assume que la permutation est légale)
            Parametres:
                permutation (tuple<tuple<int>>)
            Renvoie:
                None
        """

        # g[y1][x1], g[y2][x2] = g[y2][x2], g[y1][x1]

        self.grid[permutation[0][1]][permutation[0][0]], \
            self.grid[permutation[1][1]][permutation[1][0]] = \
            self.grid[permutation[1][1]][permutation[1][0]], \
            self.grid[permutation[0][1]][permutation[0][0]]

    def transpose(self):
        """
            transpose: Transpose la grille
            Parametres:
                None
            Renvoie:
                transposed (int[][]): La grille transposée
        """

        transposed = [[] for _i in range(len(self.grid[0]))]

        for ligne in self.grid:
            for (col_id, element) in enumerate(ligne):
                transposed[col_id].append(element)

        return transposed

    def from_transposed(self, transposed):
        """
            from_transposed: Remplace la grille active par la transposition inverse
            Parametres:
                transposed (int[][]): Une matrice transposée
            Renvoie:
                None
        """

        self.grid = [[] for _i in range(len(transposed[0]))]

        for ligne in transposed:
            for (col_id, element) in enumerate(ligne):
                self.grid[col_id].append(element)

    def clone(self):
        """
            clone: Clone la grille pour sauvegarde
            Parametres:
                None
            Renvoie:
                grille_clone (int[][]): Le clone de la grille
        """

        return [list(sl) for sl in self.grid]

    def do_compare(self, grille):
        """
            do_compare: Compare la grille a une autre pour voir si il y a une difference
            Parametres:
                grille (int[][]): La grille a comparer
            Renvoie:
                res (bool): True si différentes
        """

        return any(any(e[0] != e[1] for e in zip(*grilles_slice))
                   for grilles_slice in zip(self.grid, grille))



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

        type_to_mask = self.grid[j][i]

        mask = [[int(_e == type_to_mask) for _e in s] for s in self.grid]

        scanned = [[0 for _e in s] for s in self.grid]
        scanned[j][i] = 1

        iterations = [[(i, j)]]

        stop = False

        # Implémentation nulle a chier mais on a pas le droit a la récursivité
        while not stop:
            stop = True # By default we're gonna stop at the end of the iterations

            iterations.append([])
            for prev_iteration in iterations[-2]:
                # Exploring adjacent cases

                for direction in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    pos_x = prev_iteration[0] + direction[0]
                    pos_y = prev_iteration[1] + direction[1]

                    if explore_adj(mask, pos_x, pos_y, 1):
                        # Here is a little hack to simplify a safe
                        # version of "if scanned[y][x] == 1"
                        if explore_adj(scanned, pos_x, pos_y, 0):
                            scanned[pos_y][pos_x] = 1
                            iterations[-1].append((pos_x, pos_y))

                            stop = False # But if we find something then we don't exit


        return [item for sub_list in iterations for item in sub_list if len(item) == 2]
