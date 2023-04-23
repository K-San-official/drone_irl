import numpy as np

class DroneWorld:
    def __init__(self, size, n_people, n_obst, discount):

        # World configuration
        self.forward_step = 0.2

        # Define actions (forward, left, right)
        self.actions = ((1, 0), (1, -1), (1, 1))
        self.size = size

        # Place people into the world (randomly)
        self.people = []
        for i in range(n_people):
            self.people.append(self.get_random_location())

        # Place obstacles into the world (randomly)

        # Set random starting position
        self.starting_pos = self.get_random_location()
        self.current_pos = self.starting_pos

        # Set state (as a list of features)

    def get_random_location(self):
        x_r = np.random.rand() * self.size
        y_r = np.random.rand() * self.size
        return (x_r, y_r)

    def update_drone_location(self, action): # Updates the drone location for a certain action
        if action == 'w':
            self.current_pos = (self.current_pos[0] + self.forward_step, self.current_pos[1])
        elif action == 'a':
            pass
        elif action == 'd':
            pass

    def get_state(self):  # Gets the features out of the simulation
        pass

    def __str__(self):
        pass


class FeatureState:

    def __init__(self, sensor_readings, min_dist_person, min_dist_obst):
        self.sensor_readings = sensor_readings
        self.min_dist_person = min_dist_person
        self.min_dist_obst = min_dist_obst