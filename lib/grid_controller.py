"""
    This modules focuses on the grid management

    NOTE: The exchange between the generator and the grid manager
        is a bit trash, we should create a grid class that is shared
        between both classes.

    Author: @aaryswastaken, @Byllie
    Created Date: 03/13/2023
"""

# Importing modules for the GridManager Thread
from __future__ import absolute_import
from time import sleep

from threading import Thread
from lib.event_pool_controller import Event


def default_val(val, default=0):
    """
        Returns val if not None, else returns default

        Parameters:
            val (any): The value
            default (any, optional): The replacement [default=int<0>]

        Returns:
            res (any)
    """

    # This wrapper is pretty useful as it is used sevral times and increase code
    # lisibility greatly
    return val if val is not None else default

def explore_adj(_grille, pos_x, pos_y, scanned_value):
    """
        explore_adj: Returns the val if coordinates are in bound and the value is the same as the
            value we want to compate it to, else False

        Parameters:
            _grille (t[][]): Search array
            pos_x (int): x coordinates
            pos_y (int): y coordinate
            scanned_value (t): The value we compare it to

        Returns:
            out (bool): If condition is met
    """

    # If negative, we prevent array looping
    if pos_x < 0 or pos_y < 0:
        return False

    # This imprementation is trash but it works: if out of bound, return False else return the val
    try:
        return _grille[pos_y][pos_x] == scanned_value
    except IndexError:
        return False


class GridManager(Thread):
    """
        This class manages the grid and its physics
    """

    def __init__(self, event_pool, generator, candy_count=5, animation_wait_time=0):
        # Initialise stuff, we don't care
        super().__init__()
        self.grid = []
        self.grid_size = ()

        self.event_pool = event_pool
        self.generator = generator
        self.candy_count = candy_count
        self.animation_wait_time = animation_wait_time

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

        # Generate the grid and refresh its cache
        self.generator.init_sequence(size_x, size_y, self.candy_count)
        self.generator.populate_grid_manager(self)

    def stop(self):
        """
            Stops the thread
        """

        # Set the stop flag to True
        self.thread_stop_flag = True

    def __event_tick(self, payload):
        """
            __event_tick: Function called every tick to call for an update

            Parameters:
                payload (object):
                    "coordinates" (tuple<int>): coordinates
                    "animation_id" (int): animation_id
        """

        # This build an event towards the UI calling an update with the provided payload
        print(f"New update: {payload}")
        event = Event(1, Event.TYPE_UI_UPDATE,
                      {"update_type": 1, "coordinates": payload["coordinates"],
                       "new_gem": payload["animation_id"]})
        self.event_pool.push(event)

    def run(self):
        """
            Main loop
        """

        while not self.thread_stop_flag:
            # Fetch the next event towards the manager
            event = self.event_pool.next_and_delete(0)

            # Because pylint asks it
            if event is not None:
                # If is a permutation
                if event.msg_type == Event.TYPE_GRID_PERMUTATION:
                    permutation = event.payload["permutation"]

                    print(f"Permutation: {permutation}")

                    # If the payload is not well built, send an Error event
                    if len(permutation) != 2 or (not isinstance(permutation, tuple)):
                        error_event = Event(1, Event.TYPE_GRID_PERMUTATION_ERROR,
                                            {"permutation": permutation})
                        self.event_pool.push(error_event)

                    else:
                        # Do the actual permutation
                        res = self.tick(permutation, animation_tick=self.__event_tick,
                                        animation_wait_time=self.animation_wait_time)

                        # If an error has been encountered, send an Error event
                        if res != 0:
                            error_event = Event(1, Event.TYPE_GRID_TICK_ERROR,
                                                {"permutation": permutation, "res": res})
                            print(f"Error when ticking: {res}")
                            self.event_pool.push(error_event)
                elif event.msg_type == Event.TYPE_GEN_TRIGGER:
                    dimensions = event.payload["grid_size"]

                    self.init_grid(dimensions[0], dimensions[1])

                    self.inject_grid()
                elif event.msg_type == Event.TYPE_EXIT_ALL:
                    # Using stop instead of self.stop_flag = True in case we do some
                    # garbage collection in the method
                    self.stop()

    def permute(self, permutation):
        """
            permute: Do the permutation, assuming it is legal

            Parameters:
                permutation (tuple<tuple<int>>)

            Returns:
                None
        """

        # g[y1][x1], g[y2][x2] = g[y2][x2], g[y1][x1]

        self.grid[permutation[0][1]][permutation[0][0]], \
            self.grid[permutation[1][1]][permutation[1][0]] = \
            self.grid[permutation[1][1]][permutation[1][0]], \
            self.grid[permutation[0][1]][permutation[0][0]]

    def transpose(self):
        """
            transpose: Transpose the grid

            Parameters:
                None

            Returns:
                transposed (int[][]): Transposed grid
        """

        # Transposes the matrix (rotation along the diagonal)

        # This operation is used to speed things up because the column will now be
        # represented as a line, thus the gravity ticking will be easier for the cpu
        # in term of reference accessing
        transposed = [[] for _i in range(len(self.grid[0]))]

        for ligne in self.grid:
            for (col_id, element) in enumerate(ligne):
                transposed[col_id].append(element)

        return transposed

    def from_transposed(self, transposed):
        """
            from_transposed: Opposite of transpose: takes a traposed matrix and turns it back
                into a normal matrix

            Parameterts:
                transposed (int[][]): A transposed matrix

            Returns:
                None
        """

        # Same rotation technically, just not the same assignements
        self.grid = [[] for _i in range(len(transposed[0]))]

        for ligne in transposed:
            for (col_id, element) in enumerate(ligne):
                self.grid[col_id].append(element)

    def clone(self):
        """
            clone: Clones the grid for comparison

            Parameters:
                None

            Returns:
                cloned_grid (int[][]): Grid's clone
        """

        # Returns a clone of the grid, used to see if there is a modification
        return [list(sl) for sl in self.grid]

    def do_compare(self, grille):
        """
            do_compare: Compare parameter's grid with self's

            Parameters:
                grid (int[][]): The grid we compare against

            Returns§:
                res (bool): True if different
        """

        return any(any(e[0] != e[1] for e in zip(*grilles_slice))
                   for grilles_slice in zip(self.grid, grille))

    def detecte_coordonnees_combinaison(self, i, j):
        """
            detecte_coordonnees_combinaison: Renvoie une liste des item adjacent de meme nature

            Parameters:
                grille (Grille): the grid
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
            detecte_combinaison: Returns True if there is a vertical or horizontal match

            Parameters:
                i (int): x coordinates
                j (int): y coordinates

            Renvoie:
                res (bool): Result
        """

        # Value of the interest cell
        actual_type = self.grid[j][i]


        # To avoid None detection
        if actual_type is None:
            return False

        # To avoid negative detection:
        if actual_type < 0:
            return False

        # Testing for horizontal matches
        if explore_adj(self.grid, i-1, j, actual_type) and \
                explore_adj(self.grid, i+1, j, actual_type):
            return True

        # Testing for vertical matches
        if explore_adj(self.grid, i, j-1, actual_type) and \
                explore_adj(self.grid, i, j+1, actual_type):
            return True

        # If no matches, return False
        return False

    def gravity_tick(self, animation_tick=lambda payload: None, animation_wait_time=0):
        """
            gravity_tick: Gravityyyy

            Parametres:
                None

            Renvoie:
                None
        """

        # We take the grid's transposition
        transposed = self.transpose()
        print(f"Gravity's transposed: {transposed}")

        # We initialise new grid in the transposed form
        mutated_transposed = []

        # Create a new array that will store what line in the transposed has been updated
        updated_line = []
        updated_from = []


        # For every line of the transposed aka every column
        for (col_id, line) in enumerate(transposed):
            if None in line: # If the line doesn't have to be updated we skip it, otherwise:
                i = len(line) - 1 # We start the cursor at the end
                stop = False

                # Migrates values but only the first:
                # [2, -1, 4, 5, -1, 6] -> [-1, 2, -1, 4, 5, 6]

                # We start to fetch where the first None is
                while i >= 0 and not stop:
                    i -= 1
                    if line[i] is None:
                        stop = True

                # We get a new gem
                new_gem = self.generator.generate_cell()

                j = i-1

                # For when i == j, animate that i-1 is replacing None
                an_id = 0x200
                an_id += 0xa
                an_id += default_val(line[i-1], default=0xa) * 16
                animation_tick({"coordinates": (col_id, i),
                                "animation_id": an_id})

                # For all 0 < j < i -> Animate that it's going down
                while j >= 1:
                    an_id = 0x200
                    an_id += default_val(line[j-1], default=0xa) * 16
                    an_id += default_val(line[j], default=0xa)

                    animation_tick({"coordinates": (col_id, j),
                                    "animation_id": an_id})

                    j -= 1

                # For when j == 0, animate last going down and new cell coming
                an_id = 0x200
                an_id += new_gem * 16
                an_id += default_val(line[j], default=0xa) # Should never default
                animation_tick({"coordinates": (col_id, 0),
                                "animation_id": an_id})


                # Fill the actual line with every cell above the updated with inverted values
                # so that they arent taken into account when testing if the bottom cell can react
                new_line = [-1000+new_gem,
                            *[-1000+e_ if e_ is not None else None for e_ in line[0:i-1]],
                            line[i-1],
                            *line[(i+1):]]

                mutated_transposed.append(new_line)

                updated_line.append(col_id)
                updated_from.append(i)
            else:
                mutated_transposed.append(line)

        if len(updated_line) > 0:
            print("Waiting...")
            sleep(animation_wait_time / 1000) # TODO : /2 ??
            print("waited :)")

            for (col_id, i) in zip(updated_line, updated_from):
                # We update the screen so that it's visible

                j = i-1

                animation_tick({"coordinates": (col_id, i),
                                "animation_id": 0x300 + default_val(mutated_transposed[col_id][i],
                                                                    default=0xa)
                                })

                while j >= 0:
                    temp = mutated_transposed[col_id][j]
                    animation_tick({"coordinates": (col_id, j),
                                    "animation_id": 0x300 +
                                        (1000 + temp if temp is not None else 0xa)
                                    })

                    j -= 1

        print(f"After gravity transposed: {mutated_transposed}")

        # De-transpose
        self.from_transposed(mutated_transposed)

        return (updated_line, updated_from)

    def __routine(self, permutation, animation_tick=lambda payload: None, solo=False):
        """
            __routine (private): Wrapper for the deletion
        """

        to_delete_array = []

        if not solo:
            # Permutations
            self.permute(permutation)

            to_delete0 = self.detecte_coordonnees_combinaison(permutation[0][0],
                                                              permutation[0][1])
            to_delete1 = self.detecte_coordonnees_combinaison(permutation[1][0],
                                                              permutation[1][1])

            # If in the whole group, there is something that has a 3 alignement
            is_detected0 = any(self.detecte_combinaison(coords[0], coords[1])
                               for coords in to_delete0)
            is_detected1 = any(self.detecte_combinaison(coords[0], coords[1])
                               for coords in to_delete1)

            if not (is_detected0 or is_detected1):  # If there is no alignement on both permuted
                self.permute(permutation)  # Reset move
                print("Is useless move")
                print(f"Grid: {self.grid}")
                return 2  # Useless move

            if is_detected0: # If there is an alignement on group zero, delete everything
                to_delete_array.append(to_delete0)
            if is_detected1: # Same with one
                to_delete_array.append(to_delete1)
        else:
            # If is solo aka we only check for this cell
            to_delete_array = [
                self.detecte_coordonnees_combinaison(permutation[0][0], permutation[0][1])
            ]

        # Trigger the print of the permutation
        if not solo:
            animation_tick({"coordinates": (permutation[0][0], permutation[0][1]),
                            "animation_id": 0x100 +
                                self.grid[permutation[0][1]][permutation[0][0]]})

            animation_tick({"coordinates": (permutation[1][0], permutation[1][1]),
                            "animation_id": 0x100 +
                                self.grid[permutation[1][1]][permutation[1][0]]})


        # For every cell group we have to delete
        for to_delete in to_delete_array:
            if len(to_delete) >= 3: # Little sanity check
                for coords in to_delete: # For every deletion we have to operate
                    # Trigger an animation
                    animation_tick({"coordinates": (coords[0], coords[1]),
                                    "animation_id": 0x100+self.grid[coords[1]][coords[0]]})

                    # Do the actual deletion
                    self.grid[coords[1]][coords[0]] = None

        return 0 # If everything went fine, return 0

    def __refresh(self, update_payload, animation_tick=lambda payload: None, animation_wait_time=0):
        """
            __refresh (private): Wrapper for deletion (routine ) + gravity
        """

        old_grid = self.clone()
        first = True

        (last_updated_cols, last_updated_from) = update_payload

        while self.do_compare(old_grid) or first:
            first = False

            old_grid = self.clone()


            if len(last_updated_cols) == 0:
                # HEAVILY UNOPTIMIZED

                # For every cell ...
                for (pos_y, grille_sl) in enumerate(self.grid):
                    for (pos_x, _e) in enumerate(grille_sl):
                        # If there is a horizontal or vertical alignement
                        if self.detecte_combinaison(pos_x, pos_y):
                            # If so, trigger a deletion of the group
                            self.__routine([(pos_x, pos_y)], animation_tick, solo=True)
            else:
                for (col, i) in zip(last_updated_cols, last_updated_from):
                    if self.detecte_combinaison(i, col):
                        self._routine([(i, col)], animation_tick, solo=True)

            # Do the animation stuff
            sleep(animation_wait_time / 1000) # TODO: maybe /2 when updated b4
            (last_updated_cols, last_updated_from) = self.gravity_tick(animation_tick,
                                                                       animation_wait_time)
            sleep(animation_wait_time / 1000)

        return 0 # If everything is fine, return 0


#     def __push_final_gems(self, animation_tick):
#         """
#             __push_final_gems: Push when finished
#         """
#
#         for (y_pos, g_slice) in enumerate(self.grid):
#             for (x_pos, element) in enumerate(g_slice):
#                 animation_tick({"coordinates": (x_pos, y_pos),
#                                 "animation_id": 0x300 + element})


    def __tick(self, permutation, animation_tick=lambda payload: None, animation_wait_time=0):
        """
            __tick (private): Wrapper for first tick + gravity then the refresh
        """

        # Do the actual move
        res = self.__routine(permutation, animation_tick=animation_tick)
        if res != 0:
            print("Routine had an error")
            return res # If there is any error, returns it

        # Do a lil animation shit
        sleep(animation_wait_time / 1000)
        print("Gravity tick")
        update_payload = self.gravity_tick(animation_tick, animation_wait_time)
        print("Gravity ticked")
        sleep(animation_wait_time / 1000)

        # Call for the refresh
        print("Going for the refresh")
        res = self.__refresh(update_payload, animation_tick, animation_wait_time)

        if res != 0:
            print("Error when refreshed")
            return res # If there is any error, returns it

        # Now done in gravity_tick
        # --------
        # Else, push new gems to grid then reurn 0
        # sleep(animation_wait_time / 1000)
        # print("Going for the final gem update")
        # self.__push_final_gems(animation_tick)
        # --------

        print("FINISHED :))))")

        return 0


    def is_legal_permutation(self, permutation):
        """
            is_legal_permutation: Compute if it is a legal permutation in term of coordinates

            Parametres:
                permutation (tuple<tuple<int>>): Cell to test

            Renvoie:
                possible (bool): Result
        """

        # If the coordinates are out of bound, return False
        for permut in permutation:
            if permut[0] < 0 or permut[1] < 0 or \
                permut[0] >= self.grid_size[0] or permut[1] >= self.grid_size[1]:
                return False

        # The squared distance
        distance_manhattan = abs(permutation[0][0] - permutation[1][0]) + \
            abs(permutation[0][1] - permutation[1][1])

        # If they are not vertically or horizontally aligned, return False else True
        return distance_manhattan == 1

    def tick(self, permutation, animation_tick=lambda payload: None,
             animation_wait_time=0):
        """
            tick: Do the wrapper: If it is a legal move, do the move

            Parametres:
                permutation (tuple<tuple<int>>): Permutation to trigger
                animation_tick (function(payload: object)): Animation tick
                animation_wait_time (int): The period of the animation (ms)

            Renvoie:
                state (int): Return code

            Note:
                state:
                    - 0 = ok
                    - 1 = illegal
                    - 2 = legal but useless
        """

        # If is illegalm return 1
        if not self.is_legal_permutation(permutation):
            return 1

        # Else, proceed with the move
        return self.__tick(permutation, animation_tick, animation_wait_time)

    def inject_grid(self):
        """
            Takes the newly generated grid and sends its content to the
                pool manager for the ui to print it
        """

        event = Event(1, Event.TYPE_UI_REFRESH, {"grid": self.clone()})
        self.event_pool.push(event)
