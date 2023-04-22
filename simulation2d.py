import tkinter as tk
from droneworld import DroneWorld


if __name__ == '__main__':
    # Edit these variables to change the generation of the world:
    size = 50
    n_people = 5
    n_obstacles = 5
    discount = 0.9

    dw = DroneWorld(size, n_people, n_obstacles, discount)
    root = tk.Tk()
    root.geometry('{}x{}'.format(size * 10 + 100, size * 10 + 100))
    canvas = tk.Canvas(root, bg='green', height=size*10, width=size*10)
    canvas.pack()
    root.mainloop()
