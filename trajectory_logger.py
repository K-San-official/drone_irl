import os


class TrajectoryLogger:

    # Instance variables
    policy_type = 'not_defined'  # This value should be overridden once policy is set
    directory = ''
    filepath = ''

    def setup(self, pol):
        """
        Sets the file path according to the policy type and determines the filename
        :param pol:
        :return:
        """
        self.policy_type = pol
        self.directory = 'traj/{}'.format(pol)

        # Create directories if they were not created before
        # Check whether the specified path exists or not
        if not os.path.exists(f'traj/{self.policy_type}'):
            # Create a new directory because it does not exist
            os.makedirs(f'traj/{self.policy_type}')
            print("The new directory is created!")

        count = 0
        for element in os.listdir(self.directory):
            element_path = os.path.join(self.directory, element)
            if os.path.isfile(element_path):
                count += 1
        self.filepath = self.directory + '/traj_{}_{}.csv'.format(pol, count + 1)

    def add_line(self, sf, a):
        """
        Adds a new line to the log (state-features and executed action)
        :param sf: state-feature vector
        :param a: action (char)
        :return:
        """
        with open(self.filepath, 'a') as f:
            for i in range(len(sf)):
                if i != 15:
                    f.write(f'{sf[i]},')
                else:
                    f.write(f'{sf[i]}')
            f.write('\n')
