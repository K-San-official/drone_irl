import time
import tkinter as tk
from droneworld import DroneWorld
from policy import Policy
from trajectory_logger import TrajectoryLogger

if __name__ == '__main__':
    """
    This main function needs to be executed to start a new drone world simulation including GUI
    """

    # Edit these variables to change the generation of the world:
    size = 500
    n_people = 25  # Number of people
    n_obstacles = 5  # Number of obstacles

    # Create new instance of the drone world
    dw = DroneWorld(size, n_people, n_obstacles, 1)

    # Trajectory logger instance
    tj = TrajectoryLogger()

    def execute_policy(pol_type):
        """
        Executes a demonstration following the specified policy
        :param pol_type:
        :return:
        """
        pol = Policy(pol_type)
        tj.setup(pol_type)
        for i in range(200):
            a = pol.get_action(dw.state_features)
            tj.add_line(dw.state_features, a)
            time.sleep(0.05)
            perform_action(a)
            canvas.update_idletasks()
            text_area.update_idletasks()

    # Set up GUI
    root = tk.Tk()
    root.geometry('{}x{}'.format(size + 200, size + 200))
    canvas = tk.Canvas(root, bg='green', height=size, width=size)
    canvas.pack(side=tk.LEFT)

    # Policy Execution Buttons
    button_rand_policy = tk.Button(root, text='Random Policy', command=lambda: execute_policy('random'))
    button_rand_policy.pack(side=tk.BOTTOM)

    button_avoid_people_policy = tk.Button(root, text='Avoid People Policy', command=lambda: execute_policy('avoid_p'))
    button_avoid_people_policy.pack(side=tk.BOTTOM)

    button_avoid_obst_policy = tk.Button(root, text='Avoid Obstacle Policy', command=lambda: execute_policy('avoid_o'))
    button_avoid_obst_policy.pack(side=tk.BOTTOM)

    button_avoid_all_policy = tk.Button(root, text='Avoid All Policy',command=lambda: execute_policy('avoid_a'))
    button_avoid_all_policy.pack(side=tk.BOTTOM)

    # --- Set up elements ---
    p = dw.starting_pos

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

    # Sensors
    sensor_lines_people = []
    for i in range(dw.n_sensors):
        new_sensor = canvas.create_line(
            p[0],
            p[1],
            dw.people_sensors[i][0],
            dw.people_sensors[i][1],
            fill='purple',
            width=5
        )
        sensor_lines_people.append(new_sensor)
    sensor_lines_obst = []
    for i in range(dw.n_sensors):
        angle_offset = (i - (dw.n_sensors // 2)) * dw.sensor_spread
        new_sensor = canvas.create_line(
            p[0],
            p[1],
            dw.obst_sensors[i][0],
            dw.obst_sensors[i][1],
            fill='blue')
        sensor_lines_obst.append(new_sensor)

    # Drone
    drone_sphere = canvas.create_oval(
        p[0] - dw.dr_rad,
        p[1] - dw.dr_rad,
        p[0] + dw.dr_rad,
        p[1] + dw.dr_rad,
        fill='red')

    # --- Text Area (for state features) ---
    text_area = tk.Text(root, bg='white', height=20)
    text_area.pack(side=tk.RIGHT, padx=10, pady=10)

    def output_state():
        """
        # Prints the current simulation state onto the right text field as individual features
        """
        feature_count = 1
        for state_feature in dw.state_features:
            text_area.insert(
                tk.INSERT,
                's_{}:\t {}\n'.format(feature_count, round(state_feature, 4))
            )
            feature_count += 1
        text_area.insert("1.0", "Person Sensors\n")
        text_area.insert("9.0", "Obstacle Sensors\n")
        text_area.insert("17.0", "Person Proximity\n")
        text_area.insert("19.0", "Obstacle Proximity\n")

    output_state()

    def perform_action(a):
        """
        Performs an action either by key input or by following a policy input
        """
        dw.update_drone_location(a)
        new_pos = dw.current_pos
        canvas.moveto(
            drone_sphere,
            new_pos[0] - dw.dr_rad,
            new_pos[1] - dw.dr_rad, )
        for i in range(dw.n_sensors):
            canvas.coords(
                sensor_lines_people[i],
                new_pos[0],
                new_pos[1],
                dw.people_sensors[i][0],
                dw.people_sensors[i][1]
            )
            canvas.coords(
                sensor_lines_obst[i],
                new_pos[0],
                new_pos[1],
                dw.obst_sensors[i][0],
                dw.obst_sensors[i][1]
            )
        text_area.delete('1.0', tk.END)
        output_state()

    def keypress(event):
        """
        Moves the drone (red circle) on the field when a button is pressed.
        :param event:
        :return:
        """
        perform_action(event.char)


    root.bind("<Key>", keypress)

    root.mainloop()
