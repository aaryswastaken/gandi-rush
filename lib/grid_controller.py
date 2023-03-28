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

    def __init__(self, difficulty, event_pool, generator):
        super().__init__(self)
        self.grid = []
        self.grid_size = ()

        self.difficulty = difficulty
        self.event_pool = event_pool
        self.generator = generator

        self.thread_stop_flag = False

    def init_grid(self, size_x, size_y):
        """
            Generates a grid of requested dimentions

            Parameters:
                size_x (int)
                size_y (int)

            Returns:
                None
        """

        self.grid_size = (size_x, size_y)

        # TODO : to implement when @dchevalier69 will be finished with his code

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

    def detecte_combinaison(self, i, j):
        """
            detecte_combinaison: Renvoie True si une combinaison horizontale
                ou verticale est présente

            Parametres:
                grille (Grille): la grille
                i (int): coordonnees en x
                j (int): coordonnees en y

            Renvoie:
                res (bool): Le resultat
        """

        actual_type = self.grid[j][i]

        # print(f"Testing for ({i}, {j})")

        if explore_adj(self.grid, i-1, j, actual_type) and \
                explore_adj(self.grid, i+1, j, actual_type):
            return True

        if explore_adj(self.grid, i, j-1, actual_type) and \
                explore_adj(self.grid, i, j+1, actual_type):
            return True

        return False

    def tick_gravitee(self):
        """
            tick_gravitee: Effectue la gravité (fait tomber les trucs)

            Parametres:
                None

            Renvoie:
                None

            Notes:
                -1 dans self.grid indique une case vide qu'il faut combler
        """

        transposed = self.grid.transpose()

        mutated_transposed = []

        for line in transposed:
            if -1 in line: # If not, skip
                i = len(line) - 1
                n_occurences = sum(int(e == -1) for e in line)

                # Migrates values:
                # [2, -1, 4, 5, -1, 6] -> [-1, -1, 2, 4, 5, 6]
                while i > (n_occurences-1):
                    while line[i] == -1:
                        new_line = [-1, *line[0:i], *line[(i+1):]]
                        line = new_line
                    i -= 1

                # Repopulate

                # This method doesnt work because of an index error on line[i]

                # i = 0
                # while i < len(line) and line[i] == -1:
                #     line[i] = self.grid.genere_case()
                #     i += 1

                # This method works only if EVERY -1 has been displaced:
                new_line = [self.grid.genere_case() if e == -1 else e for e in line]
                line = new_line

            mutated_transposed.append(line)

        self.grid.from_transposed(mutated_transposed)

        return 0

    def __routine_tick_mode_3(self, permutation, solo=False):
        """
            __routine_tick_mode_3 (private): Tick mais pour le mode 3
        """

        to_delete_array = []

        if not solo:
            # Permutations
            self.grid.permute(permutation)

            to_delete0 = self.detecte_coordonnees_combinaison(permutation[0][0],
                                                              permutation[0][1])
            to_delete1 = self.detecte_coordonnees_combinaison(permutation[1][0],
                                                              permutation[1][1])

            # Can be optimized
            is_detected0 = any(self.detecte_combinaison(coords[0], coords[1])
                               for coords in to_delete0)
            is_detected1 = any(self.detecte_combinaison(coords[0], coords[1])
                               for coords in to_delete1)

            # This line has been removed because if there is an alignement, there must be
            # more than 3 tangent pieces

            # if len(to_delete0) < 3 and len(to_delete1) < 3:

            if not (is_detected0 or is_detected1): # If there is no alignement on both permuted
                # Pas possible
                self.grid.permute(permutation) # On remets comme de base
                return 2

            # to_delete_array = [to_delete0, to_delete1]
            if is_detected0:
                to_delete_array.append(to_delete0)
            if is_detected1:
                to_delete_array.append(to_delete1)

        else:
            # Utilisé dans le check global pour le refresh de la grille
            to_delete_array = [
                self.detecte_coordonnees_combinaison(permutation[0][0], permutation[0][1])
            ]

        for to_delete in to_delete_array:
            if len(to_delete) >= 3:
                for coords in to_delete:
                    self.grid[coords[1]][coords[0]] = -1

        return 0

    def __refresh_mode_3(self, animation_tick=lambda: None):
        """
            __refresh_mode_3 (private): Routine de rafraichissement par le mode 3
        """

        ancienne_grille = self.grid.clone()
        premiere = True

        while self.grid.do_compare(ancienne_grille) or premiere:
            premiere = False

            ancienne_grille = self.grid.clone()
            for (pos_y, grille_sl) in enumerate(self.grid):
                for (pos_x, _e) in enumerate(grille_sl):
                    # If there is a horizontal or vertical alignement
                    if self.detecte_combinaison(pos_x, pos_y):
                        self.__routine_tick_mode_3([(pos_x, pos_y)], solo=True)

            animation_tick()

            self.tick_gravitee()

            animation_tick()

        return 0


    def __tick_mode_3(self, permutation, animation_tick):
        """
            __tick_mode_3 (private): Wrapper pour __routine_tick_mode_3
        """

        res = self.__routine_tick_mode_3(permutation)
        if res != 0:
            return res

        animation_tick()

        self.tick_gravitee()

        animation_tick()

        # Doit refresh toute la grille (doit opti)
        res = self.__refresh_mode_3(animation_tick)

        return res


    def is_legal_permutation(self, permutation):
        """
            is_legal_permutation: Indique si la permutation est légale d'un point de vue
                grille (ne peut dépasser les bornes)

            Parametres:
                permutation (tuple<tuple<int>>): deux cases a tester

            Renvoie:
                possible (bool): si la permutation est possible
        """

        for permut in permutation:
            if permut[0] < 0 or permut[1] < 0 or \
                permut[0] >= self.grid_size[0] or permut[1] >= self.grid_size[1]:
                return False

        distance_manhattan = abs(permutation[0][0] - permutation[1][0]) + \
            abs(permutation[0][1] - permutation[1][1])

        return distance_manhattan == 1

    def tick(self, permutation, animation_tick=lambda: None):
        """
            tick: Actualise la grille selon le mode de jeu

            Parametres:
                permutation (tuple<tuple<int>>): deux cases permutées

            Renvoie:
                state (int): Le code de retour

            Note:
                state:
                    - 0 = ok
                    - 1 = illégal
                    - 2 = légal mais aucun résultat (annulé)
        """

        if not self.is_legal_permutation(permutation):
            return 1

        return self.__tick_mode_3(permutation, animation_tick)
