# Decoupage du level 1

## gen\_grille(size\_x: int, size\_y: int, nb\_type\_bonbons: int) -> grid: int[][]

Génère la grille de taille x et y


## affichage\_grille(grid: int[][], nb\_type\_bonbons: int) -> None

Affiche la grille à l'utilisateur


## detecte\_coordonnees\_combinaison(grid: int[][], i: int, j: int) -> combinaisons: tuple[]

Renvoie une liste des coordonnees des combinaisons que font les bonbons adjacents a la case (i, j)


## detecte\_bonbons\_supprimables(grid: int[][]) -> supprimables: int[][]

Renvoie une liste des bonbons qui peuvent etre supprimés


## update\_grid(grid: int[][], deletable: int[][], nb\_type\_bonbons: int) -> grid: int[][]

Update la grille en fonction de ce qui est supprimable


## ask\_permutation(size\_x: int, size\_y: int) -> permutation: tuple[]

Demande a l'utilsateur quel bonbon il veut permuter


## permute(grid: int[][], permutation: tuple[]) -> grid: int[][]

Permute en fonction de ce que l'utilisateur a demandé


