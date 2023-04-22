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
    field_size = 10
    new_field = np.zeros((field_size, field_size))
    person_prob = 0.1  # Probability for a person to appear
    return new_field

if __name__ == '__main__':
    field = init_field()
    actions = ['up', 'down', 'left', 'right']
    state_action_list = []
    current_pos = [9, 0]

    window = tk.Tk()
    window.geometry('400x400')
    # Create canvas
    canvas = tk.Canvas(window, bg='green', height=200, width=200)
    canvas.pack()
    for i in range(len(field)):
        for j in range(len(field[0])):
            colour = 'green'
            if field[i][j] == 1:
                colour = 'yellow'
            elif field[i][j] == 2:
                colour = 'blue'
            elif field[i][j] == 3:
                colour = 'purple'
            elif field[i][j] == 4:
                colour = 'orange'
            elif field[i][j] == 5:
                colour = 'gray'

            canvas.create_rectangle(20 * j,
                                    20 * i,
                                    20 * j + 19,
                                    20 * i + 19,
                                    fill=colour)
    drone_cursor = canvas.create_oval(20 * current_pos[1] + 1,
                                      20 * current_pos[0] + 1,
                                      20 * current_pos[1] + 20,
                                      20 * current_pos[0] + 20,
                                      fill='red')

    def print_move(s_row, s_col, a):
        print("S({},{}), A({})".format(s_row, s_col, a))

    def keypress(event):
        """
        Moves the drone (red circle) on the field when a button is pressed.
        :param event:
        :return:
        """
        x = 0
        y = 0
        if event.char == "a" and current_pos[1] >= 1:
            x = -20
            print_move(current_pos[0], current_pos[1], actions[2])
            state_action_list.append("{},{},{}\n".format(current_pos[0], current_pos[1], actions[2]))
            current_pos[1] -= 1
        elif event.char == "d" and current_pos[1] <= 8:
            x = 20
            print_move(current_pos[0], current_pos[1], actions[3])
            state_action_list.append("{},{},{}\n".format(current_pos[0], current_pos[1], actions[3]))
            current_pos[1] += 1
        elif event.char == "w" and current_pos[0] >= 1:
            y = -20
            print_move(current_pos[0], current_pos[1], actions[0])
            state_action_list.append("{},{},{}\n".format(current_pos[0], current_pos[1], actions[0]))
            current_pos[0] -= 1
        elif event.char == "s" and current_pos[0] <= 8:
            y = 20
            print_move(current_pos[0], current_pos[1], actions[1])
            state_action_list.append("{},{},{}\n".format(current_pos[0], current_pos[1], actions[1]))
            current_pos[0] += 1
        canvas.move(drone_cursor, x, y)

    window.bind("<Key>", keypress)

    def save_simulation_run():
        file = open("simulation_runs/log.txt", "w")
        for e in state_action_list:
            file.write(e)
        file.close()
        window.destroy()

    save_button = tk.Button(window, text="Save", command=save_simulation_run)
    save_button.pack()

    window.mainloop()


