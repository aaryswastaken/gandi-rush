"""
    Ce fichier complete le niveau 3 demandé

    Authors: @aaryswastaken
    Created Date: 03/14/2023
"""

from __future__ import absolute_import
from random import randint
from math import log10
import os
import sys
from time import sleep


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

    def affiche_grille(self, charset=None, default_char=" "):
        """
            affiche_grille: Affiche la grille

            Parametres:
                charset (str[]): Les caractères a afficher

            Renvoie:
                None
        """

        if charset is None:
            charset = [str(i+1) for i in range(self.nb_max)]

        charset_len = len(charset)

        height = len(self.grille)
        width = len(self.grille[0])

        for (i, slc) in enumerate(self.grille):
            print(f"{1+i: >{int(log10(height))+3}} : "+" ".join(
                [charset[e-1] if 0 < e <= charset_len else default_char for e in slc]))

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

    def clone(self):
        """
            clone: Clone la grille pour sauvegarde

            Parametres:
                None

            Renvoie:
                grille_clone (int[][]): Le clone de la grille
        """

        return [list(sl) for sl in self.grille]

    def do_compare(self, grille):
        """
            do_compare: Compare la grille a une autre pour voir si il y a une difference

            Parametres:
                grille (int[][]): La grille a comparer

            Renvoie:
                res (bool): True si différentes
        """

        return any(any(e[0] != e[1] for e in zip(*grilles_slice))
                   for grilles_slice in zip(self.grille, grille))


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
                        new_line = [-1, *line[0:i], *line[(i+1):]]
                        line = new_line
                    i -= 1

                # Repopulate

                # This method doesnt work because of an index error on line[i]

                # i = 0
                # while i < len(line) and line[i] == -1:
                #     line[i] = self.grille.genere_case()
                #     i += 1

                # This method works only if EVERY -1 has been displaced:
                new_line = [self.grille.genere_case() if e == -1 else e for e in line]
                line = new_line

            mutated_transposed.append(line)

        self.grille.from_transposed(mutated_transposed)

        return 0

    def __routine_tick_mode_3(self, permutation, solo=False):
        """
            __routine_tick_mode_3 (private): Tick mais pour le mode 3
        """

        to_delete_array = []

        if not solo:
            # Permutations
            self.grille.permute(permutation)

            to_delete0 = detecte_coordonnees_combinaison(self.grille,
                                                         permutation[0][0], permutation[0][1])
            to_delete1 = detecte_coordonnees_combinaison(self.grille,
                                                         permutation[1][0], permutation[1][1])

            if len(to_delete0) < 3 and len(to_delete1) < 3:
                # Pas possible
                self.grille.permute(permutation) # On remets comme de base
                return 2

            to_delete_array = [to_delete0, to_delete1]
        else:
            # Utilisé dans le check global pour le refresh de la grille
            to_delete_array = [
                detecte_coordonnees_combinaison(self.grille, permutation[0][0],
                                                permutation[0][1])
            ]

        for to_delete in to_delete_array:
            if len(to_delete) >= 3:
                for coords in to_delete:
                    self.grille.grille[coords[1]][coords[0]] = -1

        return 0

    def __refresh_mode_3(self, animation_tick=lambda: None):
        """
            __refresh_mode_3 (private): Routine de rafraichissement par le mode 3
        """

        ancienne_grille = self.grille.clone()
        premiere = True

        while self.grille.do_compare(ancienne_grille) or premiere:
            premiere = False

            ancienne_grille = self.grille.clone()
            for (pos_y, grille_sl) in enumerate(self.grille.grille):
                for (pos_x, _e) in enumerate(grille_sl):
                    self.__routine_tick_mode_3([(pos_x, pos_y)], solo=True)

            animation_tick()

            self.do_gravity()

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

        self.do_gravity()

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
                permut[0] >= self.max_x or permut[1] >= self.max_y:
                return False

        distance_manhattan = abs(permutation[0][0] - permutation[1][0]) + \
            abs(permutation[0][1] - permutation[1][1])

        return distance_manhattan == 1

    def refresh(self, animation_tick=lambda: None):
        """
            refresh: Rafraichit la grille en faisant en boucle des opérations de
                vérification de grille

            Parametres:
                animation_tick (function): Fonction à déclencher quand rafraichissement

            Renvoie:
                None
        """

        if self.mode == 3:
            return self.__refresh_mode_3(animation_tick)

        raise ValueError("Not implemented yet")

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

        if self.mode == 3:
            return self.__tick_mode_3(permutation, animation_tick)

        raise ValueError("Not impplemented yet")


def ask_value(query="?", q_min=None, q_max=None):
    """
        ask_value: Demande une valeur numerique au joueur

        Parametres:
            query (str, optional): La demande [default="?"]
            q_min (int, optional): Minimum [default: None]
            q_max (int, optional): Maximum [default: None]

        Renvoie
            res (int): La valeur entrée par le joueur
    """

    res = None

    while res is None:
        raw_response = input(query)
        try:
            res = int(raw_response)
        except ValueError:
            print("Valeur incorrecte, veuillez entrer un entier")
            res = None

        if res is not None:
            if q_min is not None:
                if res < q_min:
                    res = None
                    print(f"La valeur doit être au dessus de {q_min}")

        if res is not None:
            if q_max is not None:
                if res > q_max:
                    res = None
                    print(f"La valeur doit être en dessous de {q_max}")

    return res


def ask_dimensions():
    """
        ask_dimensions: Premier écran, demande au joueur la taille de la grille

        Parametres:
            None

        Return:
            dimensions (tuple<int>): Les dimensions entrées
    """
    print(" *-*-*-* Bienvenue dans la version Terminal de Gandi Rush *-*-*-* ")
    print(" -> Entrez une dimension de grille pour commencer:\n")

    size_x = ask_value(query="Largeur? ", q_min=2, q_max=150)
    size_y = ask_value(query="Hauteur? ", q_min=2, q_max=150)

    return (size_x, size_y)

def os_clear():
    """
        os_clear: Efface le terminal pour plus de visibilité
    """

    os.system('cls' if os.name == 'nt' else 'clear')

def show_endgame():
    """
        show_endgame: Affiche l'écran de fin
    """
    os_clear()

    print("\n\nMerci d'avoir joué à GANDI RUSH :)\n\n")


class GameManager():
    """
        Classe de gestion du jeu
    """

    def __init__(self, animation_period=0.15):
        self.grille = Grille()
        self.physique = Physique(self.grille)
        self.animation_period = animation_period
        self.do_animation = False

    def print_grid(self, delay=0):
        """
            print_grid: Routine d'affichage de la grille

            Parametres:
                delay (int, optional): Délai d'attente (utile pour l'animation) [default=0]

            Renvoie:
                None
        """
        os_clear()
        print(" *-*-*-*-* GANDI RUN *-*-*-*-* \nAppuyez sur ctrl+c pour quitter\n\n")
        self.grille.affiche_grille(charset=["-", "+", "*", "o"])

        sleep(delay)


    def main_loop(self):
        """
            main_loop: Boucle principale du jeu
        """
        while True:
            self.print_grid()
            print("\n\n\n")
            print("1=haut / 2=droite / 3=bas / 4=gauche\n")
            print("Quelle coordonnées voulez vous permutter?")
            permut_x = ask_value(query="x? ", q_min=0)
            permut_y = ask_value(query="y? ", q_min=0)
            direction = ask_value(query="direction? ", q_min=0, q_max=5)

            permutation = [(permut_x-1, permut_y-1)]

            other = (-1, -1)

            if direction == 1:
                other = (permut_x-1, permut_y-2)
            elif direction == 2:
                other = (permut_x, permut_y-1)
            elif direction == 3:
                other = (permut_x-1, permut_y)
            elif direction == 4:
                other = (permut_x-2, permut_y-1)

            permutation.append(other)

            result = self.physique.tick(permutation,
                                        animation_tick= (lambda: self.print_grid(
                                            delay=self.animation_period)) if self.do_animation
                                        else (lambda: None))

            if result == 0:
                pass
            elif result == 1:
                input("\n\nMouvement illégal. Pressez entrée pour continuer...")
            elif result == 2:
                input("\n\nMouvement inutile. Pressez entrée pour continer...")


    def run(self):
        """
            run: Point d'entrée du jeu
        """

        dimensions = ask_dimensions()
        self.grille.genere_alea(dimensions[0], dimensions[1], 4)

        print("\nGénération de la grille... (peut prendre du temps si la grille est grande)")

        self.physique.refresh_grid_info() # Lol
        self.physique.refresh(animation_tick=lambda: None)

        print("Grille générée ^^ \n")

        raw_do_anim = ask_value("\nVoulez-vous des animations?" + \
                "\n (1=oui, 0=non)\n\n> ", q_min=-1, q_max=2)

        if raw_do_anim == 1:
            self.do_animation = True

        try:
            self.main_loop()
        except KeyboardInterrupt:
            show_endgame()

        sys.exit(0)


def test_detecte_coordonnees_combinaison():
    """
        Vague test de la fonction detecte_coordonness_combinaison
    """

    raw_grilles = [
        [[1]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[1, 1, 1], [1, 0, 0], [1, 1, 0]],
        [[1, 1, 1], [1, 0, 0], [1, 1, 0]],
    ]

    all_expected = [
        [(0, 0)],
        [(1, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (1, 2)],
        [(1, 1), (2, 1), (2, 2)],
    ]

    test_positions = [
        (0, 0),
        (1, 1),
        (0, 0),
        (1, 0),
        (2, 1)
    ]

    grille_inst = Grille()

    i = 1
    for (grille, test_pos, expected) in zip(raw_grilles, test_positions, all_expected):
        print(f"Test n. {i}")
        grille_inst.grille = grille
        _out = detecte_coordonnees_combinaison(grille_inst, test_pos[0], test_pos[1])

        if all(e in expected for e in _out) and all(e in _out for e in expected):
            print("  -> Test passed")
        else:
            print("  -> Test failed :(")
            print("\n Function returned: "+str(_out))
            sys.exit(1)

        i += 1

    print("\n\nAll test passed :)")
    sys.exit(0)


if __name__ == "__main__":
    if "--test" in sys.argv:
        test_detecte_coordonnees_combinaison()
    else:
        GAME = GameManager()
        GAME.run()
