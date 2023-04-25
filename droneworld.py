import numpy as np

class DroneWorld:
    def __init__(self, size, n_people, n_obst, discount):

        # Simulation onfiguration
        self.forward_step = 5  # Moves 0.2 steps forward
        self.angle_step = 10  # Moves 20 degrees for every turn
        self.n_sensors = 7
        self.sensor_length = 150
        self.sensor_spread = 10  # Angle spread between sensors

        # Define actions (forward, left, right)
        self.actions = ((1, 0), (1, -1), (1, 1))
        self.size = size

        # Place people into the world (randomly)
        self.people = []
        self.p_radius = 10  # Radius of circles representing people
        for i in range(n_people):
            self.people.append(self.get_random_location())

        # Place obstacles into the world (randomly)
        self.obst = []
        for i in range(n_obst):
            (x0, y0) = self.get_random_location()
            x1 = x0 + (np.random.rand() * 90) + 10
            y1 = y0 + (np.random.rand() * 90) + 10
            self.obst.append((x0, y0, x1, y1))

        # Set random starting position
        self.starting_pos = self.get_random_location()
        self.current_pos = self.starting_pos
        self.current_angle = 0

        # Set state (as a list of features)
        self.state = self.get_state()

    def get_random_location(self):
        x_r = np.random.rand() * self.size
        y_r = np.random.rand() * self.size
        return (x_r, y_r)

    def update_drone_location(self, action):  # Updates the drone location for a certain action
        if action == 'w':
            pass
        elif action == 'a':
            self.current_angle -= self.angle_step
            if self.current_angle < 0:
                self.current_angle += 360
        elif action == 'd':
            self.current_angle += self.angle_step
            if self.current_angle > 359:
                self.current_angle -= 360
        (x, y) = self.current_pos
        # Apply rotation matrix
        x += (np.cos(self.current_angle * np.pi / 180) * self.forward_step)
        y += (np.sin(self.current_angle * np.pi / 180) * self.forward_step)
        self.current_pos = (x, y)
        self.get_state()
        print("Drone Postion: {}, \t Angle: {}".format(self.current_pos, self.current_angle))

    def get_min_person_dist(self):
        min_dist = -1
        for p in self.people:
            dist = np.linalg.norm(np.array(p) - np.array(self.current_pos))
            if dist < min_dist or min_dist == -1:
                min_dist = dist
        return min_dist

    def get_state(self):  # Gets the features out of the simulation
        features = [0] * 7
        features[6] = self.get_min_person_dist()
        return features


    def __str__(self):
        pass


class FeatureState:

    def __init__(self, sensor_readings, min_dist_person, min_dist_obst):
        self.sensor_readings = sensor_readings
        self.min_dist_person = min_dist_person
        self.min_dist_obst = min_dist_obst