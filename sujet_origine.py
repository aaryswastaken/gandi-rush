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


if __name__ == "__main__":
    grid = Grille()

    grid.genere_alea(5, 5, 4)
    grid.affiche_grille(charset=["-", "+", "*", "o"])
    print("\n")

    _out = detecte_coordonnees_combinaison(grid, 2, 2)

    print(_out)
