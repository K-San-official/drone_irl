import tkinter as tk
from droneworld import DroneWorld


def get_circle_coordinates(x, y, r):
    p1 = [x-r, y-r]
    p2 = [x+r, y+r]
    return [p1, p2]

if __name__ == '__main__':
    # Edit these variables to change the generation of the world:
    size = 50
    n_people = 5
    n_obstacles = 5
    discount = 0.9
    drone_angle = 0  # Rotation in the world

    dw = DroneWorld(size, n_people, n_obstacles, discount)

    # Set up GUI
    root = tk.Tk()
    root.geometry('{}x{}'.format(size * 10 + 100, size * 10 + 100))
    canvas = tk.Canvas(root, bg='green', height=size*10, width=size*10)
    canvas.pack()

    p = dw.starting_pos
    dr = 10  # Drone radius
    drone_sphere = canvas.create_oval(
        (p[0] * 10) - dr,
        (p[1] * 10) - dr,
        (p[0] * 10) + dr,
        (p[1] * 10) + dr,
        fill='red')

    def keypress(event):
        """
        Moves the drone (red circle) on the field when a button is pressed.
        :param event:
        :return:
        """
        x = 0
        y = 0
        dw.update_drone_location(event.char)
        new_pos = dw.current_pos
        canvas.moveto(
            drone_sphere,
            (new_pos[0] * 10) - dr,
            (new_pos[1] * 10) - dr,)


    root.bind("<Key>", keypress)

    root.mainloop()
