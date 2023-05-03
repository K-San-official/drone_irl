import random


class Policy:

    def __init__(self, type):
        self.type = "random"
        if type == "avoid_people":
            self.type = "avoid_people"
        elif type == "avoid_obstacles":
            self.type = "avoid_obstacles"
        elif type == "avoid_all":
            self.type = "avoid_all"

    def get_action(self, sf):
        if self.type == "random":
            action = self.get_action_random()
        elif self.type == "avoid_people":
            pass
        elif self.type == "avoid_obstacles":
            pass
        elif self.type == "avoid_all":
            pass
        return action

    def get_action_random(self):
        x = random.randint(0, 9)
        if x < 5:
            return "w"
        elif x == 5 or x == 6:
            return "a"
        elif x == 7 or x == 8:
            return "d"
        else:
            return "s"
