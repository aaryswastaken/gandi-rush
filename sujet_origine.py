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

    def genere_case(self):
        """
            genere_case: Génère une nouvelle case avec les bons paramètres de génération

            Parametres:
                None

            Renvoie:
                out (int): L'id
        """

        return randint(1, self.nb_max)

    def permute(self, permutation):
        """
            permute: Permute (assume que la permutation est légale)

            Parametres:
                permutation (tuple<tuple<int>>)

            Renvoie:
                None
        """

        # g[y1][x1], g[y2][x2] = g[y2][x2], g[y1][x1]

        self.grille[permutation[0][1]][permutation[0][0]], \
            self.grille[permutation[1][1]][permutation[1][0]] = \
            self.grille[permutation[1][1]][permutation[1][0]], \
            self.grille[permutation[0][1]][permutation[0][0]]

    def transpose(self):
        """
            transpose: Transpose la grille

            Parametres:
                None

            Renvoie:
                transposed (int[][]): La grille transposée
        """

        transposed = [[] for _i in range(len(self.grille[0]))]

        for ligne in self.grille:
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

        self.grille = [[] for _i in range(len(transposed[0]))]

        for ligne in transposed:
            for (col_id, element) in enumerate(ligne):
                self.grille[col_id].append(element)


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


def detecte_coordonnees_combinaison(grille, i, j):
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

    _grille = grille.grille
    type_to_mask = _grille[j][i]

    mask = [[int(_e == type_to_mask) for _e in s] for s in _grille]

    scanned = [[0 for _e in s] for s in _grille]
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
                    # Here is a little hack to simplify a safe version of "if scanned[y][x] == 1"
                    if explore_adj(scanned, pos_x, pos_y, 0):
                        scanned[pos_y][pos_x] = 1
                        iterations[-1].append((pos_x, pos_y))

                        stop = False # But if we find something then we don't exit


    return [item for sub_list in iterations for item in sub_list if len(item) == 2]


class Physique():
    """
        Classe qui gère la physique du jeu
    """

    def __init__(self, grille, mode=3):
        self.grille = grille
        self.mode = mode

        self.max_x = 0
        self.max_y = 0

        self.refresh_grid_info()

    def refresh_grid_info(self):
        """
            refresh_grid_info: Actualise le cache sur le paramètre de la grille (x / y)

            Parametres:
                None

            Renvoie:
                None
        """
        self.max_y = len(self.grille.grille)

        if self.max_y != 0:
            self.max_x = len(self.grille.grille[0])
        else:
            self.max_x = 0

    def do_gravity(self):
        """
            do_gravity: Effectue la gravité

            Parametres:
                None

            Renvoie:
                None

            Notes:
                -1 dans self.grille.grille indique une case vide qu'il faut combler
        """

        transposed = self.grille.transpose()

        mutated_transposed = []

        for line in transposed:
            if -1 in line: # If not, skip
                i = len(line) - 1
                n_occurences = sum(int(e == -1) for e in line)

                # Migrates values:
                # [2, -1, 4, 5, -1, 6] -> [-1, -1, 2, 4, 5, 6]
                while i > (n_occurences-1):
                    while line[i] == -1:
                        new_line = [-1, *line[0:i], line[i:]]
                        line = new_line
                    i -= 1

                # Repopulate
                i = 0
                while i < len(line) and line[i] == -1:
                    line[i] = self.grille.genere_case()

            mutated_transposed.append(line)

        self.grille.from_transposed(mutated_transposed)

        return 0



    def __tick_mode_3(self, permutation):
        """
            tick_mode_3 (private): Tick mais pour le mode 3
        """

        # Permutation
        self.grille.permute(permutation)

        to_delete0 = detecte_coordonnees_combinaison(self.grille, permutation[0][0],
                        permutation[0][1])
        to_delete1 = detecte_coordonnees_combinaison(self.grille, permutation[1][0],
                        permutation[1][1])

        if len(to_delete0) < 3 and len(to_delete1) < 3:
            # Pas possible
            self.grille.permute(permutation) # On remets comme de base
            return 2

        for to_delete in [to_delete0, to_delete1]:
            if len(to_delete) >= 3:
                for coords in to_delete:
                    self.grille.grille[coords[1]][coords[0]] = -1

        self.do_gravity()

        return 0


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
                permut[0] >= self.max_x or permut[1] >= self.max_y:
                return False

        distance_manhattan = abs(permutation[0][0] - permutation[1][0]) + \
            abs(permutation[1][0] - permutation[1][1])

        return distance_manhattan == 1

    def tick(self, permutation):
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

        if self.mode == 3:
            return self.__tick_mode_3(permutation)

        raise TypeError("Not impplemented yet")

# TODO : test_detecte_coordonnees_combinaison


if __name__ == "__main__":
    grid = Grille()

    grid.genere_alea(5, 5, 4)
    grid.affiche_grille(charset=["-", "+", "*", "o"])
    print("\n")

    _out = detecte_coordonnees_combinaison(grid, 2, 2)

    print(_out)
