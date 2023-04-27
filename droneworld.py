import numpy as np
import utils as ut

class DroneWorld:
    """
    This class stores all the information of the drone world.
    A state consists of the features that the drone perceives.
    """

    def __init__(self, size, n_people, n_obst):
        """
        Initialises a new drone world.
        :param size: square field of size*size
        :param n_people: number of people
        :param n_obst: number of obstacles
        """
        # Simulation configuration
        self.forward_step = 5  # Moves 0.2 steps forward
        self.angle_step = 10  # Moves 20 degrees for every turn

        self.n_sensors = 7
        self.sensor_length = 150
        self.sensor_spread = 10  # Angle spread between sensors
        self.person_sensors = [(0, 0)] * self.n_sensors  # Tuple of (x1, y1) as an endpoint of each sensor
        self.person_sensors_readings = [0] * self.n_sensors
        self.obst_sensors = [(0, 0)] * self.n_sensors
        self.obst_sensors_readings = [0.0] * self.n_sensors

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
        self.current_angle = 0  # 0 = right, 90 = down, 180 = left, 270 = up (no negative angle)

        # IRL state description
        self.state_features = [0] * ((self.n_sensors * 2) + 2)

        self.update_state()

    def get_random_location(self) -> (float, float):
        """
        Generates a new random location in the field (x, y)
        :return: tuple (x, y)
        """
        x_r = np.random.rand() * self.size
        y_r = np.random.rand() * self.size
        return x_r, y_r

    def update_drone_location(self, action: str):  # Updates the drone location for a certain action
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
        else:
            return
        (x, y) = self.current_pos
        # Apply rotation matrix
        x += (np.cos(self.current_angle * np.pi / 180) * self.forward_step)
        y += (np.sin(self.current_angle * np.pi / 180) * self.forward_step)
        self.current_pos = (x, y)
        self.update_state()
        #print("Drone Postion: {}, \t Angle: {}".format(self.current_pos, self.current_angle))

    def get_min_person_dist(self) -> float:
        min_dist = -1
        for p in self.people:
            dist = np.linalg.norm(np.array(p) - np.array(self.current_pos))
            if dist < min_dist or min_dist == -1:
                min_dist = dist
        return min_dist

    def get_min_obst_dist(self) -> float:
        min_dist = -1
        for o in self.obst:
            dx = max(o[0] - self.current_pos[0], self.current_pos[0] - o[2], 0)
            dy = max(o[1] - self.current_pos[1], self.current_pos[1] - o[3], 0)
            dist = np.sqrt(dx**2 + dy**2)
            if dist < min_dist or min_dist == -1:
                min_dist = dist
        return min_dist


    def update_people_sensors(self):
        pass


    def update_obst_sensors(self):
        for i in range(len(self.obst_sensors)):
            angle_offset = (i - (self.n_sensors // 2)) * self.sensor_spread
            x1 = self.current_pos[0] + (np.cos((self.current_angle + angle_offset) * np.pi / 180) * self.sensor_length)
            y1 = self.current_pos[1] + (np.sin((self.current_angle + angle_offset) * np.pi / 180) * self.sensor_length)
            min_dist = self.sensor_length
            p0 = self.current_pos
            # Calculate collision with walls using a line segment intersection algorithm
            for o in self.obst:
                # extract all 4 corner points
                cp = [(o[0], o[1]), (o[2], o[1]), (o[2], o[3]), (o[0], o[3])]
                for j in range(len(cp)):  # For all 4 line segments of a rectangle
                    # Check if line segments intersect
                    if ut.intersect(p0, (x1, y1), cp[j], cp[(j + 1) % 4]):
                        x1_t, y1_t = ut.line_intersection_coordinates((p0, (x1, y1)), (cp[j], cp[(j + 1) % 4]))
                        current_dist = ut.dist(p0, (x1_t, y1_t))
                        # Check if the distance to the intersection is the closest one
                        if current_dist < self.sensor_length:
                            if current_dist < min_dist or min_dist == -1:
                                min_dist = current_dist
                                x1 = x1_t
                                y1 = y1_t
            print(min_dist)
            # Map sensor distance to the feature (normalised)
            self.state_features[self.n_sensors + i] = 1 - (min_dist / self.sensor_length)
            self.obst_sensors[i] = (x1, y1)

    def update_state(self):  # Gets the features out of the simulation
        # Update people sensors

        # Update obstacle sensors
        self.update_obst_sensors()
        # Update min person proximity
        self.state_features[-2] = self.get_min_person_dist()
        # Update min obstacle proximity
        self.state_features[-1] = self.get_min_obst_dist()

