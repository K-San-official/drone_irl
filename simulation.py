import numpy as np
import tkinter as tk

def init_field():
    """
    Field Indices:
    0 = empty
    1 = target
    2 = water
    3 = house
    4 = people
    5 = road
    :return:
    """
    field = [[0, 0, 0, 0, 0, 0, 4, 0, 0, 1],
             [0, 0, 0, 0, 0, 0, 4, 0, 0, 5],
             [2, 2, 2, 2, 0, 0, 4, 4, 4, 5],
             [0, 0, 0, 2, 2, 2, 4, 4, 0, 5],
             [0, 0, 0, 0, 0, 2, 2, 2, 0, 5],
             [0, 5, 5, 5, 5, 5, 3, 2, 0, 5],
             [0, 5, 3, 3, 0, 5, 3, 2, 0, 5],
             [0, 5, 3, 3, 0, 5, 5, 2, 2, 5],
             [0, 5, 3, 3, 0, 0, 5, 3, 2, 5],
             [0, 5, 3, 3, 0, 0, 5, 5, 2, 5]]
    return field

if __name__ == '__main__':
    field = init_field()
    current_pos = [9, 0]

    window = tk.Tk()
    window.geometry('400x400')
    # Create canvas
    canvas = tk.Canvas(window, bg='green', height=200, width=200)
    canvas.pack()
    for i in range(len(field[0])):
        for j in range(len(field)):
            canvas.create_rectangle(20 * i, 20 * j, 20 * i + 19, 20 * j + 19, fill="green")
    drone_cursor = canvas.create_oval(20 * current_pos[1],
                                      20 * current_pos[0],
                                      20 * current_pos[1] + 19,
                                      20 * current_pos[0] + 19,
                                      fill='red')
    def keypress(event):
        """
        Moves the drone (red circle) on the field when a button is pressed.
        :param event:
        :return:
        """
        x = 0
        y = 0
        if event.char == "a":
            x = -20
            current_pos[1] += 1
        elif event.char == "d":
            x = 20
            current_pos[1] -= 1
        elif event.char == "w":
            y = -20
            current_pos[0] -= 1
        elif event.char == "s":
            y = 20
            current_pos[0] += 1
        canvas.move(drone_cursor, x, y)
        print_move()

    window.bind("<Key>", keypress)



    window.mainloop()

