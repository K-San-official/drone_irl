def margin_opt(traj_list):
    """
    Computes a reward function using margin optimisation.
    The input needs to be a list of trajectories where each trajectory is a 2d list
    where the first index denotes the time step and the second index denotes the
    state features and the actions in the end.
    :param traj_list:
    :return:
    """
    pass


def feature_expectation(traj_list, discount):
    """
    Computes the feature expectation for a set of n trajectories.
    :param traj_list:
    :return:
    """
    mu = [0] * 16
    for n in range(len(traj_list)):
        for t in range(len(traj_list[0])):
            for k in range(16):
                mu[k] += discount**t * traj_list[n][t][k]
    mu = mu / len(traj_list)  # TODO: check if that works for a whole vector
