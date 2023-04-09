"""
    This test is about the grid generator
"""

from random import randint
import pytest

from lib.generator import GridGenerator

@pytest.mark.timeout(15)
def test_generator_1000():
    """
        Test the generator on 1000 occurences
    """

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

    n_test = 1000
    print(f"Testing for {n_test} random tests")

    i = 0
    one_failed = False
    while i <= n_test and not one_failed:
        grid_instance = GridGenerator()

        r_grid = grid_instance.init_sequence(randint(10, 30), randint(10, 30), randint(4, 5))

        c_res = check_any_adjacence(r_grid)

        if not c_res:
            print(f"  {i+1} Test passed")
            i += 1
        else:
            print(f"  {i+1} Test failed")
            one_failed = True

    assert not one_failed
