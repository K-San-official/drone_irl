import random


class Policy:

    def __init__(self, type):
        self.type = "random"
        self.wind = 0.2
        if type == "avoid_people":
            self.type = "avoid_people"
        elif type == "avoid_obstacles":
            self.type = "avoid_obstacles"
        elif type == "avoid_all":
            self.type = "avoid_all"

    def get_action(self, sf):
        """
        Calculates an action based on the selected policy time.
        :param sf:
        :return:
        """
        if self.type == "random":
            action = self.get_action_random()
        elif self.type == "avoid_people":
            action = self.get_action_avoid_people(sf)
        elif self.type == "avoid_obstacles":
            action = self.get_action_avoid_obstacles(sf)
        elif self.type == "avoid_all":
            action = self.get_action_avoid_all(sf)
        return action

    def get_action_random(self):
        """
        Returns a random action with the following probabilities:
        Forward:    50%
        Left:       20%
        Right:      20%
        Back:       10%
        :return:
        """
        x = random.randint(0, 9)
        if x < 5:
            return 'w'
        elif x == 5 or x == 6:
            return 'a'
        elif x == 7 or x == 8:
            return 'd'
        else:
            return 's'

    def get_action_avoid_people(self, sf):
        """
        Returns an action that actively avoids people in the field.
        :param sf:
        :return:
        """
        # With a certain percentage, execute random action
        x = random.random()
        if x <= self.wind:
            return self.get_action_random()
        left_sum = 0
        right_sum = 0
        # Technically this is not part of the policy to take obstacles into consideration.
        # If the drone is facing a wall and would get stuck, the next part is to unstuck it.
        obst_sum = sum(sf[int(len(sf) / 2) - 2:-2])
        if obst_sum > 2 and sf[-1] > 0.95:
            return 'd'
        total_sum = sum(sf[:int(len(sf) / 2) - 2])
        if total_sum < 0.3:
            return 'w'
        if total_sum > 3:
            return 's'
        # Iterate over all people detecting sensors
        for i in range(int(len(sf) / 2) - 2):
            if i <= 2:
                left_sum += sf[i]
            if i >= 4:
                right_sum += sf[i]
        # If the left sensors detect more, then turn right and vice-versa
        if left_sum > right_sum:
            return 'd'
        else:
            return 'a'

    def get_action_avoid_obstacles(self, sf):
        """
        Returns an action that actively avoids obstacles in the field.
        People are ignored.
        :param sf:
        :return:
        """
        # With a certain percentage, execute random action
        x = random.random()
        if x <= self.wind:
            return self.get_action_random()
        left_sum = 0
        right_sum = 0
        total_sum = sum(sf[int(len(sf) / 2) - 2:-2])
        if total_sum < 1:
            return 'w'
        if total_sum > 3.5:
            return 's'
        # Iterate over all obstacles detecting sensors
        for i in range(int(len(sf) / 2) - 2):
            if i <= 2:
                left_sum += sf[i + 7]
            if i >= 4:
                right_sum += sf[i + 7]
        # If the left sensors detect more, then turn right and vice-versa
        if left_sum > right_sum:
            return 'd'
        else:
            return 'a'

    def get_action_avoid_all(self, sf):
        """
        Returns an action that avoids both obstacles and people in the field.
        The rules that handle the trade-off between obstacle and people avoidance can be described as follows:
        TODO: Describe policy in pseudo-rules
        :param sf:
        :return:
        """