"""
    This modules focuses on the grid management

    Author: @aaryswastaken
    Created Date: 03/13/2023
"""

# Importing modules for the GridManager Thread
from __future__ import absolute_import
from threading import Thread


class GraphNode():
    """
        This class handles a cell aka a Node in our graph-based approach
    """

    def __init__(self, coordinates, node_value, node_border_type, parent):
        self.coordinates = coordinates
        self.node_value = node_value
        self.node_border_type = node_border_type
        self.parent_graph = parent

    def is_deletable(self, direction):
        """
            is_deletable: Returns if it is deletable on the corresponding direction

            Parameters:
                direction (int): 0 for horizontal and 1 for vertical

            Returns:
                deletable (bool)
        """

        if self.node_border_type == 0:
            return True

        # self.node_border_type == 2 means excluded from vertical
        if direction == 0 and self.node_border_type == 2:
            return True

        # self.node_border_type == 1 means excluded from horizontal
        if direction == 1 and self.node_border_type == 1:
            return True

        return False

    def mutate_coords(self, new_coords):
        """
            mutate_coords: Change the coordinates

            Parameters:
                new_coords (tuple<int>): New coordinates

            Returns:
                None
        """

        if len(new_coords) != 2:
            raise ValueError("Must have two coordinates value")

        self.coordinates = new_coords

    def change_parent(self, new_parent):
        """
            change_parent: Change the graph it belongs to

            Parameters:
                new_parent (CachedGraph): New parent

            Returns:
                None
        """

        self.parent_graph = new_parent


class CachedGraph():
    """
        This class handles a graph, portion of the whole grid, made of connex values.

        When a permutation occurs, only a small portion of the graphs are updated.
        This is where the optimization comes from.
    """

    def __init__(self):
        self.nodes = []

    def permute(self, permutation_coords, node):
        """
            permute: Given a tuple of coordinates, and the other node, do the permutation

            Note: Only one of both graphs is triggered for permutation, handling the permutation
                itself with the other graph

            Parameters:
                permutation_coords (tuple<tuple<int>>): The associated coordinates
                node (GraphNode): The node of the other graph that is permuted

            Returns:
                None
        """

    def fill_reverse_search(self, reverse_grid):
        """
            fill_reverse_search: The reverse_search is a 2d array that do an inverse mapping
                of the coordinates to the corresponding node, a type of cache to make the
                computations less expensive

            Parameters:
                reverse_grid (GraphNode[][]): The reverse mapping grid

            Returns:
                reverse_grid (GraphNode[][]): Shouldn't be used as the reference is directly
                    modified so we don't have to update the value by a return, rather the
                    pointer is directly modified
        """

    def recompute_whole_graph_adjacence(self):
        """
            recompute_whole_graph_adjacence: Recomputes the whole graph node's node_border_type
                corresponding to their position

            Parametrers:
                None

            Returns:
                None
        """


class GridManager(Thread):
    """
        This class manages the grid and its physics
    """

    def __init__(self):
        super().__init__(self)

    def init_grid_random(self, size_x, size_y):
        """
            /!\\ DEPRECATED /!\\

            init_grid_random: Generates a random grid of requested dimentions

            Parameters:
                size_x (int)
                size_y (int)

            Returns:
                None
        """

    def stop(self):
        """
            stop: Stops the thread
        """

    def run(self):
        """
            run: Main loop
        """

    def permute(self, permutation):
        """
            permute: Trigger permutation, assuming it's a legal permutation

            Parametres:
                permutation (tuple<tuple<int>>)

            Renvoie:
                None
        """
