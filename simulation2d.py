import tkinter as tk
from droneworld import DroneWorld


if __name__ == '__main__':
    # Edit these variables to change the generation of the world:
    size = 50
    n_people = 5
    n_obstacles = 5
    discount = 0.9

    dw = DroneWorld(size, n_people, n_obstacles, discount)
    gui = tk.Tk()
    gui.geometry
