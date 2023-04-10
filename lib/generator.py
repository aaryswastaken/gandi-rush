"""
    This module is in charge of generating the grid

    Author: @dchevalier69, @aaryswastaken
    Creation Date:
"""

from random import randint


class GridGenerator():
    """
        This class handles the grid
    """

    def __init__(self):
        self.grid = []
        self.grid_size = (None, None)
        self.candy_nb = None

    def __generate_random(self):
        """
            Generates a new random number
        """

        # If we have no informations about what to chose from, raise an error
        if self.candy_nb is None:
            raise ValueError("Grid not initiated")

        return randint(0, self.candy_nb-1)

    def __init_grid(self, size_x, size_y, candy_nb):
        """
            Inits the grid with half cells
        """
        self.grid_size = (size_x, size_y)
        self.candy_nb = candy_nb
        # if i%2 == j%2 allows to fill half of the cells with random values in a diagonal pattern
        self.grid = [[self.__generate_random() if (i%2==j%2) else None for i in range(size_x)]
                     for j in range(size_y)]

    def __safe_access(self, x_pos, y_pos, grid=None, default=-1):
        """
            Access safely the matrix. Returns default if out of bounds
        """

        # default grid is the one that is owned by the class
        if grid is None:
            grid = self.grid

        # If the coordinates are out of bound, return the default
        if x_pos < 0 or x_pos > len(grid[0])-1:
            return default

        if y_pos < 0 or y_pos > len(grid)-1:
            return default

        # If the coordinates are in bound, return the actual value
        return grid[y_pos][x_pos]

    def __populate_grid(self):
        """
            Populates the other half of the grid
        """

        # This solution has been described in issue#39

        # Definition of the adjacence matrix. This matrix defines if its corresponding cell
        # has already a cell with the same number next to it
        adjacence_matrix = [[0 for j in range(self.grid_size[0])]
                             for i in range(self.grid_size[1])]

        # Those arrays defines the directions in which we check
        # Notice that reduced_deltas has only half of them. Because we fill the cell from left to
        # right from top to bottom, we only have to check for adjacence in the already filled cells
        # aka top and left
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        reduced_deltas = [(-1, 0), (0, -1)]

        for (y_pos, mt_sl) in enumerate(self.grid):
            for (x_pos, element) in enumerate(mt_sl):
                # If we need to fill it
                if element is None:
                    # We only have to look at the top and to the left because bottom and right
                    # aren't generated yet

                    # The adjacence array defines the cell type that are already filled in the
                    # neighborhood
                    adjacence_array = [self.__safe_access(x_pos+dx, y_pos+dy)
                                       for (dx, dy) in reduced_deltas]

                    # Reverse adjacence is an array in which we can randomly and freely pick
                    # the number that will be affected to the working cell
                    reverse_adjacence = [i for i in range(self.candy_nb)
                                         if not i in adjacence_array]

                    if len(reverse_adjacence) == 0:
                        # If the reverse_adjacence is empty, there is an issue and so we return
                        # one as an error indicator

                        print("Fatal error. Stacktrace:")
                        print(adjacence_matrix)
                        print(reverse_adjacence)
                        print(self.grid)

                        return 1

                    # We just chose the number
                    chosen_number = reverse_adjacence[randint(0, len(reverse_adjacence)-1)]

                    self.grid[y_pos][x_pos] = chosen_number  # apply it

                    # Now we refresh the adjacence matrix
                    has_any = False

                    # first for the adjacent cell ...
                    for (delta_x, delta_y) in deltas:
                        if self.__safe_access(x_pos+delta_x, y_pos+delta_y) == chosen_number:
                            has_any = True
                            adjacence_matrix[y_pos+delta_y][x_pos+delta_x] = 1

                    # ... and if one of them is a match with the working cell, the working
                    # cell must also be a match
                    if has_any:
                        adjacence_matrix[y_pos][x_pos] = 1

        # If no errors have been encountered, return 0 as the default code
        return 0


    def init_sequence(self, size_x, size_y, candy_nb):
        """
            Main generator entrypoint

            Parameters:
                size_x (int): the width
                size_y (int): the height
                candy_nb (int); the number of candies

            Returns
                grid (int[][])
        """

        # This function is just a wrapper of the 2-phased generator

        self.__init_grid(size_x, size_y, candy_nb) # generate the full random, half empty grid
        return self.__populate_grid() # populate the grid. If any error, return them

    def populate_grid_manager(self, grid_manager):
        """
            This function helps to fill in the grid_manager's values

            Parameters:
                grid_manager (GridManager)

            Returns:
                None
        """

        # This just updates the grid manager with these informations
        grid_manager.grid = self.grid
        grid_manager.grid_size = self.grid_size

#     def fill_grid_manager_nones(self, grid_manager):
#         """
#             After grid_manager's gravity tick we need to regenerate new cells
#
#             Parameters:
#                 grid_manager (GridManager)
#
#             Returns:
#                 None
#         """
#
#         # TODO

    def generate_cell(self):
        """
            Generates a random cell for the grid manager
        """

        try:
            return self.__generate_random()
        except ValueError:
            return -1 # Because it hasn't been initialized yet


if __name__ == "__main__":
    # Just to test

    GRID = GridGenerator()

    RES = GRID.init_sequence(10, 15, 3)

    if RES != 0:
        print("Error :/")
    else:
        print(GRID.grid)
