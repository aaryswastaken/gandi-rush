# La doku

*@aaryswastaken, 2023*

---

Bienvenue sur la documentation de Gandi Rush, la pas du tout copie du jeu préféré des octagénaires. Dans ce fichier seront décrit la majorité des mécaniques ainsi que leur explication.

Le sujet choisi est le niveau 3 qui a été étendu pour augmenter la difficulté. Le sujet 3 classique ayant été terminé le lendemain du début du projet.

### Architecture

Gandi Rush est un programme multi thread (composé de plusieurs processus en parallèle). Pour l'instant il y en a deux:
 - MainThread: thread principal, découle de l'execution du script `gandi_rush.py`, contient la gestion de l'UI principalement,
 - GridManager: thread de gestion de la physique.

Ces deux threads communiquent au travers d'une instance commune de `EventPool`. Cette classe gère les différentes communication par le moyen d'une pile FIFO a gestion de priorité.

Lorsque `gandi_rush.py`, aussi appelé l'orchestrateur est lancé, ce script va instancier les différentes classes, initialiser la grille (le choix de la taille de la grille n'est pas encore disponible) puis lancer le thread de `GridManager` et enfin lancer l'interface.


### Les différentes classes

#### Generator

Une bonne explication du fonctionnement du générateur est détaillé dans l'issue #39, résolu par la pull request #42.

Globalement le générateur va initialiser deux grilles à deux dimensions d'entiers de même dimensions:
 - La première est la grille qui va être renvoyée. Lors de son initialisation elle est remplie une case sur deux par une valeur aléatoire, le reste reste à None. Le remplissage s'effectue dans un pattern de diagonale de sorte à ce qu'un chiffre soit systématiquement entouré de 4 chiffres horizontalement et verticalement,
 - La seconde est une matrice temporaire qui va permettre de connaitre si la cellule située sur la première matrice aux mêmes coordonnées est voisine d'une autre cellule de même type.

La deuxième phase du générateur consiste à remplir les cellules encore contenant des None. Pour ce faire on va remplir ligne par ligne en regardant la cellule du dessus et la cellule de gauche. Ce sont les cellules qui probablement ont déjà été remplies (sauf si elles n'existent pas => cas limite des bordures).

On va alors générer un tableau de "valeur adjacentes" qui est un tableau des valeurs adjacentes (lol) uniquement si la seconde matrice indique qu'elles sont deja prises.

Ceci signifie que si on prends ces valeurs, on risque de faire un alignement. On va alors générer un second tableau de "valeurs safe" de 0 au nombre de gemmes - 1 en excluant toutes les occurences présentes dans "valeurs adjacentes".

On va ensuite prendre une valeur au hasard entre 0 et la taille de ce dernier tableau - 1. Cette valeur va alors correspondre à la nouvelle valeur de la cellule.

On oublie pas d'upadate la seconde matrice et une fois que ce scan est complet, on clone la grille dans la grille tampon du gestionnaire de grille


#### Event Pool

Cette classe est assez simple dans la mesure ou c'est simplement un wrapper pour une pile FIFO (first in, first out).

Globalement cette classe contient un tableau, `stack` et pour chaque `Event` qui lui est fourni, va créer une nouvelle instance de `PooledEvent` qui globalement permets de suivre les priorité etc...

Il y a différentes methodes qui permettent de manipuler la pile mais elles sont pas particulièrement pertinents à détailler ici.

On peut noter cependant l'implémentation de listener qui pourront être utile dans de futures version, notemment pour la gestion de l'interface. Ces listener permettent de spécifier une fonction qui sera appelée avec l'evenement comme argument à chaque fois qu'un nouveau sera push.

Il est aussi important de mentionner qu'en plus de la gestion de la priorité des event, la pile gère également la directionnalité.

NOTE: Le broadcast n'est pas encore implémenté et va demander un offsetage des indices à moins d'utiliser un nombre négatif comme id


#### Window controller

Globalement c'est un peu de la bidouille informatique mais c Gwendal qui a fait donc c'est assez propre. (La bidouille vient du fait que le python c'est objectivement pas ouf)

Cette classe permet la gestion de l'interface. C'est également elle qui trigger l'evenement de fermeture des différents threads.


#### Grid Controller

Commence par prendre un doliprane, ca va être assez rude

En gros cette classe gère la totalité de la physique des gemmes ainsi que plus anechdotiquement la gestion des points.

L'enchainement désastreux des évènements suivants commence par la fonction run qui va faire du pooling sur la `EventPool`.

##### Permutation event

Cet event commence par une vérification du `payload`, contenu de l'evenement. Celui ci doit être un `tuple<tuple<int>>` de 2x2. Si cette condition n'est pas remplie, on renvoie une erreur.

Une fois cette vérification passée, on commence la vraie logique avec l'appel de `GridManager.tick`

En utilisant une distance algébrique (cf. Théorème de Manhattan), et de simple test, on vérifie que la permutation est légale (deux cases adjacentes et existantes)

Une fois ce test passé, on entre dans `GridManager.__tick`

 - Cette fonction va commencer par appeler `GridManager.__routine` qui est une fonction qui s'occupe de permuter, vérifier que le mouvement sers a quelque chose et supprime les bonnes cases (la suppression s'effectue par la cellule qui est mise à None).

Pour ce faire, la fonction va calculer pour chacune des cases du couple de cellules permutées, les cellules avec les mêmes valeurs adjacentes à celles-ci puis stocker ces adjacences dans deux tableaux séparés.
Pour chacun des tableaux, on va tester (pour chaque ensemble de cellule donc) si au moins une des cellules est alignée avec deux autres pour former un alignement de trigger.
Si aucun des ensembles ne donne de résultat, on re-permute afin de laisser la grille comme elle était avant puis on renvoie un code d'erreur 2 qui corresponds à `Legal but useless`.
Sinon, pour chaque ensemble qui a une combinaison, on envoie à l'interface un evenement de modification en spécifiant que la gemme est fissurée, signe de de sa proche destruction et on modifie la grille de telle sorte à ce que la cellule soit à None.

Cette fonction va ensuite calculer le nombre de gemmes supprimées et le transmettre à l'interface pour que le score soit modifié.

 - Ensuite, `GridManager.tick_gravity` va être appelée. Cette fonction, comme son nom l'indique sers a effectuer un tick de gravité.

A l'origine, cette fonction effectuais toute la gravité en une seule fois avec une implémentation assez élégante, encore visible dans `sujet_origine.py`

On commence par prendre la tansposée de la matrice de la grille. Ceci nous permet de travailler sur une colone (maintenant devenue une ligne) en toute tranquilité, sans avoir a jump sur plusieurs lignes au même indice de colone.

Enfin, pour chaque ligne, on cherche l'indice du None le plus en bas (i, oui on est inventifs) et à partir de là une disjonction de cas à lieu:
 - pour tout i > 0, on génère une nouvelle gemme aléatoirement puis on remonte la ligne (en utilisant j la position tel que j va de i-1 à 0) en envoyant des trigger à l'interface avec les sprite des gemmes qui descendent, en utilisant pour j = 0 la gemme nouvellement générée. La variable j balaye seulement de i-1 à 0 car la cellule en position i est traitée à part bien qu'elle pourrait être traitée normalement (permets de couvrir le cas ou `i=i_max`) puis on effectue la suppression de la cellule i avec un décalage vers le bas en utilisant des opérations sur les tableaux
 - pour tout i = 0, on ne traite que la ligne du haut pour ne pas causer de soucis lorsque `j=i-1` est négatif (et accède à la ligne du bas par boucle)

Une fois que tout cela est terminé, on collecte les lignes pour les ajoouter a la matrice à t+1 `mutated_transposed` que l'on va ensuite détransposer et copier dans la grille principale.

Une opération importante à noter est que toutes les cellules au dessus de la cellule qui remplace `None` à l'indice i sont soustraites par 1000. Ceci permets de plus tard savoir que ces cellules (affichées comme encore en train de tomber), ne sont pas a prendre en compte dans la vérification de groupe.

À ce titre, la fonction de gravité renvoie un tableau temporaire, à passer à la prochaine instance.

 - Une fois que la gravité a fait un tour, on appelle `GridManager.refresh` qui va s'occuper de boucler jusqu'à ce qu'il n'y ait plus d'update a trigger.

La fonction de refresh va lire le temporaire de `GridManager.tick_gravity` afin d'y vérifier si il y a des update a trigger.

Dans le cas ou `update_payload` est vide, on effectue une routine normale qui va vérifier chaque cellule pour une adjacence (bien que cette partie puisse avoir des optimisation, son implémentation est suffisament robuste pour suivre sans soucis).

Dans le cas contraire, on se positionne au niveau de la gemme qui vient d'être supprimée et on teste pour toutes les occurences en remontant jusqu'au nombres négatifs (comme l'implémentation est pas ouf là dessus, on le fait pas, on check juste la cellule supprimée et updatée)

Après cette phase de suppression, on reprends un tick de gravité, en updatant le payload.

On boucle jusqu'à ce que la grille soit la même une itération sur l'autre et pleine de nombres positifs.

NOTE: Au début du tick de gravité, on appelle `GridManager.__sanitize_grid` qui va remettre tout les nombres négatifs à leur valeur.

NOTE2: On effectue `I: cell -> 1000 - cell` comme inversion au lieu de `I: cell -> 0 - cell` car si cell = 0 alors `I(cell) = cell`

Une fois que refresh a finit, on déroule la pile d'appel vers le haut en prenant en compte les codes d'erreur si il y a et on les affiche si jamais.

On envoie également les codes d'erreur dans la pile au cas ou un jour on aie la foi de les afficher sur l'interface

##### Gen\_Trigger Event

Cet event déclenche juste la génération d'une nouvelle grille.


## Conclusion

Voilà qui conclut le fonctionnement de Gandi Rush. Bon jeu ^^
