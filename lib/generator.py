"""
    This module is in charge of generating the grid

    Author: @dchevalier69, @aaryswastaken
    Creation Date:
"""

from random import randint


class Grid():
    """
        This class handles the grid
    """

    def __init__(self):
        self.grid = []
        self.grid_size = (None, None)
        self.candy_nb = None

    def __init_grid(self, size_x, size_y, candy_nb):
        self.grid_size = (size_x, size_y)
        self.grid = [[randint(1, candy_nb) for i in range(size_x)] for j in range(size_y)]
        self.candy_nb = candy_nb

    def check_matches(self):
        """
            check_matches: This function removes any vertical or horizontal alignement
        """

        # Check for horizontal matches
        for y_pos in range(0, self.grid_size[1]):
            for x_pos in range(0, self.grid_size[0]-4):
                if self.grid[y_pos][x_pos] == self.grid[y_pos][x_pos+1] and \
                        self.grid[y_pos][x_pos] == self.grid[y_pos][x_pos+2] and \
                        self.grid[y_pos][x_pos] == self.grid[y_pos][x_pos+3]:

                    self.grid[y_pos][x_pos+2] = None

        # Check for vertical matches
        for y_pos in range(0, self.grid_size[1]-4):
            for x_pos in range(0, self.grid_size[0]):
                if self.grid[y_pos][x_pos] == self.grid[y_pos+1][x_pos] and \
                        self.grid[y_pos][x_pos] == self.grid[y_pos+2][x_pos] and \
                        self.grid[y_pos][x_pos] == self.grid[y_pos+3][x_pos]:

                    self.grid[y_pos+2][x_pos] = None

    def check_gaps(self):
        """
            check_gaps: This function checks for any gaps and drops the cells where there is gaps
        """

        for y_pos in range(self.grid_size[1]-1,-1,-1):
            for x_pos in range(self.grid_size[0]):
                if self.grid[y_pos][x_pos] is None:
                    self.drop_tiles(x_pos, y_pos)

    def drop_tiles(self, x_pos, y_pos):
        """
            drop_tiles: Drops the tiles at the pos
        """

        for colonne in range(y_pos,0,-1):
            self.grid[colonne][x_pos] = self.grid[colonne-1][x_pos]

        self.grid[0][x_pos] = None

    def replace_none_start(self):
        """
            replace_none_start: Replace None values at the start
        """

        for y_pos in range(self.grid_size[1]-2):
            for x_pos in range(self.grid_size[0]-2):
                if self.grid[y_pos+1][x_pos+1] is None:
                    n_generated=0

                    while n_generated not in (self.grid[y_pos+2][x_pos+1],
                                              self.grid[y_pos][x_pos+1],
                                              self.grid[y_pos+1][x_pos],
                                              self.grid[y_pos+1][x_pos+2]):
                        n_generated = randint(1, self.candy_nb)

                    self.grid[y_pos][x_pos] = n_generated

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

        self.__init_grid(size_x, size_y, candy_nb)
        self.check_matches()
        self.check_gaps()
        self.replace_none_start()

        return self.grid

    def populate_grid_manager(self, grid_manager):
        """
            This function helps to fill in the grid_manager's values

            Parameters:
                grid_manager (GridManager)

            Returns:
                None
        """

        grid_manager.grid = self.grid
        grid_manager.grid_size = self.grid_size

    def fill_grid_manager_nones(self, grid_manager):
        """
            After grid_manager's gravity tick we need to regenerate new cells

            Parameters:
                grid_manager (GridManager)

            Returns:
                None
        """

        # Very poor implementation but works because python
        self.grid = grid_manager.grid
        self.replace_none_start()
        grid_manager.grid = self.grid


if __name__ == "__main__":
    def check_any_adjacence(grid):
        """
            Returns true if the grid is invalid
        """

        res = True

        for (offseted_line_id, line_slice) in enumerate(grid[1:-1]):
            line_id = offseted_line_id - 1
            for (offseted_element_position, element) in enumerate(line_slice[1:-1]):
                element_position = offseted_element_position - 1

                res = res and not ((element == grid[line_id-1][element_position] and \
                        element == grid[line_id+1][element_position]) or \
                        (element == grid[line_id][element_position-1] and \
                        element == grid[line_id][element_position+1]))

        return res

    N_TEST = 1000
    print(f"Testing for {N_TEST} random tests")

    i = 0
    ONE_FAILED = False
    while i <= N_TEST and not ONE_FAILED:
        grid_instance = Grid()

        r_grid = grid_instance.init_sequence(randint(10, 30), randint(10, 30), randint(4, 5))

        c_res = check_any_adjacence(r_grid)

        if not c_res:
            print("  Test passed")
            i += 1
        else:
            print("  Test failed")
            ONE_FAILED = True
