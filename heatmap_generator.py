import sys
import numpy as np
import matplotlib.pyplot as plt

class Heatmap:

    def __init__(self, field_size, scale):
        self.scale = scale
        self.grid = np.zeros(shape=(int(field_size[0] * scale), int(field_size[1] * scale)))

    def track_position(self, pos):
        x = int(pos[0] * self.scale)
        y = int(pos[1] * self.scale)
        try:
            self.grid[x, y] += 1
        except IndexError:
            print(f"Position index out of bound for x = {x} and y = {y}")

    def print_grid(self):
        np.set_printoptions(threshold=sys.maxsize)
        print(np.sum(self.grid))

    def create_heatmap(self):
        plt.imshow(self.grid.clip(0, 20), cmap='hot', interpolation='nearest')
        plt.xlabel('x-coordinate')
        plt.ylabel('y-coordinate')
        plt.show()
