

class DroneWorld:
    def __init__(self, size, n_people, n_obst, discount):

        # Define actions (forward, left, right)
        self.actions = ((1, 0), (1, -1), (1, 1))

        # Place people into the world (randomly)

        # Place obstacles into the world (randomly)

        # Set random starting position
        self.starting_pos = (0, 0)  #TODO: Implement

        # Set state (as a list of features)

    def update_drone_location(self, action): # Updates the drone location for a certain action
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