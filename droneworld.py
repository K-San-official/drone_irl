import numpy as np
import utils as ut

from policy import Policy
from trajectory_logger import TrajectoryLogger


class DroneWorld:
    """
    This class stores all the information of the drone world.
    A state consists of the features that the drone perceives.
    """

    def __init__(self, size, n_people, n_obst, env=0):
        """
        Initialises a new drone world.
        :param size: square field of size*size
        :param n_people: number of people
        :param n_obst: number of obstacles
        """
        # Simulation configuration
        self.dr_rad = 10  # Drone radius
        self.forward_step = 5  # Moves 0.2 steps forward
        self.angle_step = 10  # Moves 20 degrees for every turn
        self.n_people = n_people
        self.n_obst = n_obst

        self.people = []  # List with positions of all people
        self.obst = []  # List with coordinate bounds of all obstacles
        self.p_radius = 10  # Radius of circles representing people

        self.n_sensors = 7
        self.sensor_length = 200
        self.sensor_spread = 15  # Angle spread between sensors
        self.people_sensors = [(0, 0)] * self.n_sensors  # Tuple of (x1, y1) as an endpoint of each sensor
        self.obst_sensors = [(0, 0)] * self.n_sensors

        self.current_pos = (0, 0)
        self.starting_pos = (0, 0)
        self.current_angle = 0

        # Define actions (forward, left, right)
        self.actions = ((1, 0), (1, -1), (1, 1))
        self.size = size

        # Create environment
        if env == 0:
            self.create_rand_env()
        elif env == 1:
            self.create_env_1()
        elif env == 2:
            self.create_env_2()

        # IRL state description
        self.state_features = [0] * ((self.n_sensors * 2) + 2)

        self.update_state()

    def create_env_1(self):
        """
        Creates a pre-designed environment.
        """
        # Set borders at the edges
        self.place_borders()

        # Set drone start
        self.starting_pos = (250, 250)
        self.current_pos = self.starting_pos
        self.current_angle = 90

        # Place obstacles in the world
        self.obst.append((100, 0, 150, 200))
        self.obst.append((0, 350, 100, 400))
        self.obst.append((320, 300, 380, 350))
        self.obst.append((290, 150, 390, 230))
        self.obst.append((400, 0, 500, 50))

        # Place people in the world
        self.people.append((22, 50))
        self.people.append((180, 30))
        self.people.append((400, 126))
        self.people.append((284, 332))
        self.people.append((130, 350))
        self.people.append((430, 460))

        self.people.append((325, 265))
        self.people.append((220, 59))
        self.people.append((410, 452))
        self.people.append((440, 174))
        self.people.append((465, 210))
        self.people.append((261, 158))
        self.people.append((380, 130))
        self.people.append((120, 280))
        self.people.append((180, 170))
        self.people.append((214, 101))
        self.people.append((240, 89))
        self.people.append((52, 420))

    def create_env_2(self):
        """
        Creates a pre-designed environment.
        """
        # Set borders at the edges
        self.place_borders()

        # Set drone start
        self.starting_pos = (250, 250)
        self.current_pos = self.starting_pos
        self.current_angle = 90

        # Place obstacles in the world
        self.obst.append((65, 86, 89, 120))
        self.obst.append((226, 77, 250, 133))
        self.obst.append((200, 382, 381, 416))
        self.obst.append((380, 170, 430, 260))
        self.obst.append((0, 250, 150, 300))

        # Place people in the world
        self.people.append((200, 250))
        self.people.append((134, 55))
        self.people.append((426, 39))
        self.people.append((80, 323))
        self.people.append((400, 460))
        self.people.append((360, 200))
        self.people.append((355, 261))
        self.people.append((20, 159))
        self.people.append((450, 450))
        self.people.append((360, 294))
        self.people.append((365, 240))
        self.people.append((265, 120))
        self.people.append((180, 430))
        self.people.append((320, 80))
        self.people.append((50, 200))
        self.people.append((213, 201))
        self.people.append((140, 189))
        self.people.append((50, 450))

    def create_rand_env(self):
        """
        Creates a random environment with a certain number of obstacles and people.
        The size of the obstacles varies.
        """
        # Place people into the world (randomly)
        for i in range(self.n_people):
            self.people.append(self.get_random_location())

        # Place obstacles into the world (randomly)
        for i in range(self.n_obst):
            (x0, y0) = self.get_random_location()
            x1 = x0 + (np.random.rand() * 90) + 10
            y1 = y0 + (np.random.rand() * 90) + 10
            self.obst.append((x0, y0, x1, y1))

        self.place_borders()

        # Set random starting position
        self.starting_pos = self.get_random_location()

        # Repeat if starting location is inside an obstacle
        while self.is_in_obstacle(self.starting_pos):
            self.starting_pos = self.get_random_location()
        self.current_pos = self.starting_pos

    def place_borders(self):
        """
        Places borders at the edges of the environment so that the drone cannot leave the field.
        """
        bt = 5  # Border thickness
        self.obst.append((0, 0, self.size, bt))  # Top wall
        self.obst.append((0, self.size - bt, self.size, self.size))  # Bottom wall
        self.obst.append((0, bt, bt, self.size - bt))  # Left wall
        self.obst.append((self.size - bt, bt, self.size, self.size - bt))

    def get_random_location(self) -> (float, float):
        """
        Generates a new random location in the field (x, y)
        :return: location as a tuple (x, y)
        """
        x_r = np.random.rand() * (self.size - (self.dr_rad * 2)) + self.dr_rad
        y_r = np.random.rand() * (self.size - (self.dr_rad * 2)) + self.dr_rad
        return x_r, y_r

    def move_drone_by_action(self, action: str):
        """
        Performs one action in the drone world and moves the drone according to the action
        :param action: character in the set {'w', 'a', 's', 'd'}
        """
        if action == 'w':
            step = self.forward_step
        elif action == 's':
            step = -self.forward_step
        elif action == 'a':
            self.current_angle -= self.angle_step
            if self.current_angle < 0:
                self.current_angle += 360
            step = self.forward_step
        elif action == 'd':
            self.current_angle += self.angle_step
            if self.current_angle > 359:
                self.current_angle -= 360
            step = self.forward_step
        else:
            return
        (x, y) = self.current_pos

        # Apply rotation matrix
        x += (np.cos(self.current_angle * np.pi / 180) * step)
        y += (np.sin(self.current_angle * np.pi / 180) * step)

        # Check if drone is still in the bounds of the field
        if self.dr_rad <= x <= self.size - self.dr_rad and self.dr_rad <= y <= self.size - self.dr_rad:
            # Check if new position is not inside obstacles
            if not self.is_in_obstacle((x, y)):
                self.current_pos = (x, y)
        self.update_state()

    def get_min_person_dist(self) -> float:
        """
        :return: euclidean distance between the drone and the center of the closest person
        """
        min_dist = -1
        for p in self.people:
            dist = np.linalg.norm(np.array(p) - np.array(self.current_pos))
            if dist < min_dist or min_dist == -1:
                min_dist = dist
        return min_dist

    def get_min_obst_dist(self) -> float:
        """
        :return: euclidean distance between the drone and the closest obstacle
        """
        min_dist = -1
        for o in self.obst:
            dx = max(o[0] - self.current_pos[0], self.current_pos[0] - o[2], 0)
            dy = max(o[1] - self.current_pos[1], self.current_pos[1] - o[3], 0)
            dist = np.sqrt(dx ** 2 + dy ** 2)
            if dist < min_dist or min_dist == -1:
                min_dist = dist
        return min_dist

    def update_people_sensors(self):
        """
        Updates the sensor readings for sensors that detect people.
        """
        for i in range(len(self.people_sensors)):
            angle_offset = (i - (self.n_sensors // 2)) * self.sensor_spread
            x1 = self.current_pos[0] + (np.cos((self.current_angle + angle_offset) * np.pi / 180) * self.sensor_length)
            y1 = self.current_pos[1] + (np.sin((self.current_angle + angle_offset) * np.pi / 180) * self.sensor_length)
            min_dist = self.sensor_length
            p0 = self.current_pos
            person_detected = False
            # Check if there is already an obstacle detected by this sensor (and update min_dist accordingly)
            obst_dist = ut.dist(p0, self.obst_sensors[i])
            if obst_dist < min_dist:
                min_dist = obst_dist
            for p in self.people:
                (hit_dist, sensor_dist) = ut.min_dist_line_seg_point((p0[0], p0[1], x1, y1), p)
                # Check if sensor detects a person
                if hit_dist < 10 and sensor_dist < min_dist:
                    min_dist = sensor_dist
                    person_detected = True
            if person_detected:
                x1 = self.current_pos[0] + (np.cos((self.current_angle + angle_offset) * np.pi / 180) * min_dist)
                y1 = self.current_pos[1] + (np.sin((self.current_angle + angle_offset) * np.pi / 180) * min_dist)
                # Map sensor distance to the feature (normalised)
                self.state_features[i] = 1 - (min_dist / self.sensor_length)
            else:
                # Set sensors to drone location for further display
                x1, y1 = p0
                self.state_features[i] = 0.0
            self.people_sensors[i] = (x1, y1)

    def update_obst_sensors(self):
        """
        Updates the sensor readings for sensors that detect obstacles.
        """
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
            # Map sensor distance to the feature (normalised)
            self.state_features[self.n_sensors + i] = 1 - (min_dist / self.sensor_length)
            self.obst_sensors[i] = (x1, y1)

    def update_state(self):  # Gets the features out of the simulation
        """
        Updates the current state (all state features) of the simulation.
        """
        # Update obstacle sensors
        self.update_obst_sensors()
        # Update people sensors
        self.update_people_sensors()
        # Update min person proximity (normalised)
        self.state_features[-2] = 1 - (self.get_min_person_dist() / self.size)
        # Update min obstacle (normalised)
        self.state_features[-1] = 1 - (self.get_min_obst_dist() / self.size)

    def is_in_obstacle(self, pos):
        """
        Checks if a position is inside an obstacle.
        The drone radius is added as a margin.
        :return: True, if the drone is inside an obstacle.
        """
        in_obst = False
        for o in self.obst:
            if o[0] - self.dr_rad < pos[0] < o[2] + self.dr_rad and o[1] - self.dr_rad < pos[1] < o[3] + self.dr_rad:
                in_obst = True
                break
        return in_obst

    def execute_policy(self, pol_type, steps):
        """
        Executes a policy in the drone world for a number of steps without a GUI
        :param pol_type: type of expert policy
        :param steps: number of steps to execute
        """
        tj = TrajectoryLogger()
        pol = Policy(pol_type)
        tj.setup(pol_type)
        # Reset drone position and orientation
        self.current_pos = self.starting_pos
        self.current_angle = 90
        self.update_state()
        # Run n steps in the simulation and log data
        for i in range(steps):
            a = pol.get_action(self.state_features)
            tj.add_line(self.state_features, a)
            self.move_drone_by_action(a)

    def execute_policy_get_traj(self, pol_type, steps):
        """
        Executes a policy in the drone world for a number of steps without a GUI.
        A trajectory is not saved to a file but directly returned as a list.
        :param pol_type: type of expert policy
        :param steps: number of steps to execute
        :return: trajectory
        """
        pol = Policy(pol_type)
        self.current_pos = self.starting_pos
        self.current_angle = 90
        self.update_state()
        traj = []
        # Run n steps in the simulation and log data
        for i in range(steps):
            a = pol.get_action(self.state_features)
            traj.append(self.state_features)
            self.move_drone_by_action(a)
        return traj
