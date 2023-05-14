import csv
import random
import os
import numpy as np

from keras.models import Sequential
from keras.layers import InputLayer
from keras.layers import Dense

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


def feature_expectation(traj_list, discount: float):
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


def feature_expectation_nn(nn, dw: DroneWorld, discount: float, steps: int):
    """
    Computes the feature expectation vector for one demonstration of n steps with the state-action mapping
    from a neural network. Decisions are deterministic, so there is no point in averaging multiple runs.
    :param nn: Neural Network for state-action mapping
    :param dw: Drone World
    :param discount: Discount Factor
    :param steps: Number of steps in the simulation
    :return:
    """
    # Reset to starting position
    dw.current_pos = dw.starting_pos
    dw.update_state()

    # Init feature expectation vector
    mu = [0] * 16

    # Update feature expectation for each step
    for i in range(steps):
        for j in range(16):
            mu[j] += pow(discount, i + 1) * dw.state_features[j]
        # Predict new action
        action = np.argmax(nn.predict(np.expand_dims(dw.state_features, axis=0), verbose=None))
        a = 'w'
        if action == 0:
            a = 'w'
        elif action == 1:
            a = 'a'
        elif action == 2:
            a = 's'
        elif action == 3:
            a = 'd'
        dw.move_drone_by_action(a)
    return mu



def q_learning(episodes: int, dw: DroneWorld, w):
    """
    Reference: https://www.baeldung.com/cs/reinforcement-learning-neural-network
    Executes the famous Q-Learning algorithm to find a policy that matches the reward-function best
    :param episodes:
    :param env:
    :param w:
    :return: The generated neural network itself so that it can be used for state-action mapping S -> A
    """

    # Define variables
    gamma = 0.9
    eps = 0.5
    eps_decay_factor = 0.99

    # Create Neural network
    nn = Sequential()
    nn.add(Dense(16, activation='relu'))
    nn.add(Dense(16, activation='relu'))
    nn.add(Dense(4, activation='linear'))
    nn.compile(loss='mse', optimizer='adam', metrics=['mae'])

    # Reset starting position
    dw.current_pos = dw.starting_pos

    # Execute Q-Learning loop for n episodes
    for i in range(episodes):
        if random.random() < eps:
            action = random.randint(0, 3)
        else:
            action = np.argmax(nn.predict(np.expand_dims(dw.state_features, axis=0), verbose=None))
        a = 'w'
        if action == 0:
            a = 'w'
        elif action == 1:
            a = 'a'
        elif action == 2:
            a = 's'
        elif action == 3:
            a = 'd'
        # Keep a copy of the old state features for the backtracking
        sf_old = dw.state_features
        # Update environment by one step
        dw.move_drone_by_action(a)
        # Calculate new reward
        reward = sum(np.multiply(dw.state_features, w))
        target_vector = nn.predict(np.expand_dims(dw.state_features, axis=0), verbose=None)[0]
        print('Target vector', target_vector)
        target = reward + gamma + np.max(target_vector)
        # Update Q(s' ,a') with new target value
        target_vector[action] = target
        # Backpropagation of weights inside the Neural Network
        nn.fit(np.expand_dims(sf_old, axis=0), np.expand_dims(target_vector, axis=0), epochs=1)
    return nn



def execute_irl(iterations: int, gamma: float, dw: DroneWorld, traj_path: str):
    """

    :param iterations:
    :param gamma:
    :param dw:
    :param traj_path:
    :return:
    """
    print_results = True

    w = [0] * 16  # Reward weights
    traj_list = []  # axis 0 = trajectory | axis 1 = step | axis 2 = state feature (0-15), action (16)

    # The following lists keep track of the rewards and feature expectations throughout the process of the IRL.
    w_list = []
    mu_list = []

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
    mu_new = [0] * 16
    print(mu_e)

    # Execute n numbers of IRL-iterations
    for i in range(iterations):
        # --- Step 1: Update reward weights ---
        if i == 0:
            # Initialise random weights for the first iteration
            for j in range(len(w)):
                w[j] = random.random() * 2 - 1  # Interval [-1, 1]
        else:
            pass
        w_list.append(w)
        if print_results:
            print(f'Iteration {i} reward weights: {w}')

        # --- Step 2: Generate new policy wrt. new reward weights ---
        new_policy_nn = q_learning(20, dw, w)

        # --- Step 3: Compute new feature expectations from policy ---
        mu_new = feature_expectation_nn(new_policy_nn, dw, gamma, 500)
        mu_list.append(mu_new)
        if print_results:
            print(f'Iteration {i} feature expectations: {mu_new}')
            print('---')

    if print_results:
        print(f'Expert feature expectations: {mu_e}')

    return w_list, mu_list


if __name__ == '__main__':
    # --- Step 1: Create environment ---

    dw = DroneWorld(500, 0, 0, 1)
    n_traj = 10  # Number of trajectories that are created by the expert policies
    n_steps = 10  # Number of steps performed for each trajectory
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
