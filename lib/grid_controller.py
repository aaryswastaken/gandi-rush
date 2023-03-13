class Grid():
    def __init__(self):
        self.grid = []

    def init_grid(self, size_x, size_y):
        self.grid = [[0 for i in range(size_y)] for j in range(size_x)]
