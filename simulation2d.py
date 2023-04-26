import tkinter as tk
import numpy as np
from droneworld import DroneWorld


def get_circle_coordinates(x, y, r):
    p1 = [x-r, y-r]
    p2 = [x+r, y+r]
    return [p1, p2]

if __name__ == '__main__':
    # Edit these variables to change the generation of the world:
    size = 500
    n_people = 5
    n_obstacles = 5
    discount = 0.9
    drone_angle = 0  # Rotation in the world

    dw = DroneWorld(size, n_people, n_obstacles, discount)

    # Set up GUI
    root = tk.Tk()
    root.geometry('{}x{}'.format(size + 200, size + 200))
    canvas = tk.Canvas(root, bg='green', height=size, width=size)
    canvas.pack(side=tk.LEFT)

    # --- Set up elements ---

    # People
    for person in dw.people:
        canvas.create_oval(
            person[0] - dw.p_radius,
            person[1] - dw.p_radius,
            person[0] + dw.p_radius,
            person[1] + dw.p_radius,
            fill='purple'
        )
    # Obstacles
    for obst in dw.obst:
        canvas.create_rectangle(
            obst[0],
            obst[1],
            obst[2],
            obst[3],
            fill='grey'
        )

    # Drone
    p = dw.starting_pos
    dr = 10  # Drone radius
    drone_sphere = canvas.create_oval(
        p[0] - dr,
        p[1] - dr,
        p[0] + dr,
        p[1] + dr,
        fill='red')

    # Sensors
    sensor_lines = []
    for i in range(dw.n_sensors):
        angle_offset = (i - (dw.n_sensors // 2)) * dw.sensor_spread
        new_sensor = canvas.create_line(
            p[0],
            p[1],
            p[0] + (np.cos(angle_offset * np.pi / 180) * dw.sensor_length),
            p[1] + (np.sin(angle_offset * np.pi / 180) * dw.sensor_length),
            fill='blue')
        sensor_lines.append(new_sensor)

    # --- Text Area (for state features) ---
    text_area = tk.Text(root, bg='white', height=20)
    text_area.pack(side=tk.RIGHT, padx=10, pady=10)

    def output_state():
        # Prints the current simulation state onto the right text field as individual features
        count = 1
        for state_feature in dw.state:
            text_area.insert(tk.INSERT, 's_{}: {}\n'.format(count, round(state_feature, 4)))
            count += 1

    output_state()

    def keypress(event):
        """
        Moves the drone (red circle) on the field when a button is pressed.
        :param event:
        :return:
        """
        dw.update_drone_location(event.char)
        new_pos = dw.current_pos
        canvas.moveto(
            drone_sphere,
            new_pos[0] - dr,
            new_pos[1] - dr,)
        for i in range(dw.n_sensors):
            canvas.coords(
                sensor_lines[i],
                new_pos[0],
                new_pos[1],
                dw.obst_sensors[i][0],
                dw.obst_sensors[i][1]
            )
        text_area.delete('1.0', tk.END)
        output_state()

    root.bind("<Key>", keypress)

    root.mainloop()
