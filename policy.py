import random


class Policy:

    def __init__(self, pol_type):
        self.pol_type = pol_type
        self.wind = 0.08

    def get_action(self, sf):
        """
        Calculates an action based on the selected policy time.
        :param sf:
        :return:
        """
        if self.pol_type == "random":
            action = self.get_action_random()
        elif self.pol_type == "avoid_p":
            action = self.get_action_avoid_people(sf)
        elif self.pol_type == "avoid_o":
            action = self.get_action_avoid_obstacles(sf)
        elif self.pol_type == "avoid_a":
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
        x = random.randint(0, 3)
        if x == 0:
            return 'w'
        elif x == 1:
            return 'a'
        elif x == 2:
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
        if total_sum > 2.6:
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

    def get_action_avoid_obstacles_old(self, sf):
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
        if total_sum > 5 or sf[15] > 0.97:
            return 's'
        if total_sum < 2 and sf[15] > 0.95:
            rand_turn = random.random()
            if rand_turn < 0.5:
                return 'd'
            else:
                return 'a'
        if total_sum < 1:
            y = random.random()
            if y < 0.6:
                return 'w'
            elif 0.6 <= y < 0.8:
                return 'a'
            else:
                return 'd'
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
        pass