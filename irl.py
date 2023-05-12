import csv
import random
import os
import numpy as np

from droneworld import DroneWorld

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
    # For each trajectory
    for t in range(len(traj_list)):
        # For each step
        for s in range(len(traj_list[0])):
            # For each state feature
            for sf in range(16):
                mu[sf] += pow(discount, t + 1) * float(traj_list[t][s][sf]) / len(traj_list)
    return mu


def execute_irl(epochs: int, gamma: float, dw: DroneWorld, traj_path: str):
    """

    :param epochs:
    :param gamma:
    :param dw:
    :param traj_path:
    :return:
    """
    w = [0] * 16  # Reward weights
    traj_list = []  # axis 0 = trajectory | axis 1 = step | axis 2 = [state feature, action]

    # Import trajectories from csv files
    for filename in os.listdir(traj_path):
        file = os.path.join(traj_path, filename)
        traj = []
        with open(file, 'r') as current_file:
            reader = csv.reader(current_file)
            for i, line in enumerate(reader):
                traj.append(line)
        traj_list.append(traj)

    # Compute initial feature expectations (expert)
    mu_e = feature_expectation(traj_list, gamma)
    print(mu_e)

    for i in range(epochs):
        # --- Step 1: Update reward weights ---
        if i == 0:
            # Initialise random weights for the first iteration
            for j in range(len(w)):
                w[j] = random.random() * 2 - 1  # Interval [-1, 1]

        # --- Step 2: Generate new policy wrt. new reward weights ---

        # --- Step 3: Compute new feature expectations from policy ---

        pass


if __name__ == '__main__':
    # --- Step 1: Create environment ---

    dw = DroneWorld(500, 0, 0, 1)
    n_traj = 10  # Number of trajectories that are created by the expert policies
    n_steps = 500  # Number of steps performed for each trajectory
    pol_type = 'avoid_o'
    directory = f'traj/{pol_type}'
    generate_new_traj = False

    # --- Step 2: Create expert trajectories ---

    if generate_new_traj:
        # Clear old files in folder
        if os.path.exists(f'traj/{pol_type}'):
            directory = f'traj/{pol_type}'
            filelist = [f for f in os.listdir(directory) if f.endswith(".csv")]
            for f in filelist:
                os.remove(os.path.join(directory, f))

        # Record new trajectories from demonstration runs
        for i in range(n_traj):
            print(f'Creating Trajectory {i}')
            dw.execute_policy(pol_type, n_steps)


    # --- Step 3: Execute IRL ---
    execute_irl(1, 0.9, dw, directory)
