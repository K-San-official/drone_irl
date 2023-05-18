import csv
import random
import os
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from sklearn import svm
import matplotlib.pyplot as plt

from droneworld import DroneWorld


def policy_difference(w, mu_e, mu_i):
    v_e = np.inner(np.array(w), np.array(mu_e))
    v_i = np.inner(np.array(w), np.array(mu_i))
    return abs(v_e - v_i)


def feature_expectation(traj_list, discount: float):
    """
    Computes the feature expectation for a set of n trajectories.
    :param discount:
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
                mu[sf] += (pow(discount, s + 1) * float(traj_list[t][s][sf])) / len(traj_list)
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
        #print('Action ', a, ' Position: ', dw.current_pos)
        #print(mu)
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
    gamma = 0.99
    epsilon = 0.3
    alpha = 0.2

    # Create Neural network
    nn = Sequential()
    nn.add(Dense(16, activation='relu'))
    nn.add(Dense(16, activation='relu'))
    nn.add(Dense(4, activation='linear'))
    nn.compile(loss='mse', optimizer='adam', metrics=['mae'])

    # Reset starting position
    dw.current_pos = dw.starting_pos
    dw.current_angle = 90
    dw.update_state()

    # Counts the amount of each action that is taken during each iteration
    action_count = [0] * 4

    # Execute Q-Learning loop for n episodes
    for i in range(episodes):
        q_values_old = nn.predict(np.expand_dims(dw.state_features, axis=0), verbose=None)[0]
        if random.random() < epsilon:
            action = random.randint(0, 3)
        else:
            action = np.argmax(q_values_old)
        a = 'w'
        if action == 0:
            a = 'w'
        elif action == 1:
            a = 'a'
        elif action == 2:
            a = 's'
        elif action == 3:
            a = 'd'
        action_count[action] += 1
        # Keep a copy of the old state features for the backtracking
        sf_old = dw.state_features
        q_old = q_values_old[action]
        # Calculate new reward
        reward = sum(np.multiply(dw.state_features, w))
        # Update environment by one step
        dw.move_drone_by_action(a)
        max_next_state = max(nn.predict(np.expand_dims(dw.state_features, axis=0), verbose=None)[0])
        target = q_old + alpha * (reward + (gamma * max_next_state) - q_old)
        # Update Q(s' ,a') with new target value
        q_values_old[action] = target
        # Backpropagation of weights inside the Neural Network
        nn.fit(np.expand_dims(sf_old, axis=0), np.expand_dims(q_values_old, axis=0), epochs=1, verbose=None)
    print(f'Action Count (w, a, s, d): {action_count}')
    return nn


def svm_tune(w, mu_e, mu_list):
    # x are the training samples where the first sample is the expert feature expectation
    x = [mu_e] + mu_list
    # y are the classification labels so the expert class is 1 and everything else is classified as -1
    y = [1] + ([-1] * len(mu_list))
    # Train SVM
    clf = svm.SVC(kernel='linear')
    clf.fit(x, y)
    return clf.coef_


def execute_irl(iterations: int, n_steps, gamma: float, dw: DroneWorld, traj_list: list):
    """

    :param iterations:
    :param gamma:
    :param dw:
    :param traj_list:
    :return:
    """
    print_results = True

    w = [0] * 16  # Reward weights

    # The following lists keep track of the rewards and feature expectations throughout the process of the IRL.
    w_list = []
    mu_list = []

    # Compute initial feature expectations (expert)
    mu_e = feature_expectation(traj_list, gamma)
    if print_results:
        print(f'Expert feature expectations: {mu_e}')

    # Execute n numbers of IRL-iterations
    for i in range(iterations):
        # --- Step 1: Update reward weights ---
        if i == 0:
            # Initialise random weights for the first iteration
            for j in range(len(w)):
                w[j] = random.random() * 0.2 - 0.1  # Interval [-1, 1]
        else:
            # Tune w using as SVM maximum margin method
            w = svm_tune(w, mu_e, mu_list)[0]
        w_list.append(w)
        if print_results:
            print(f'Iteration {i} reward weights: {w}')

        # --- Step 2: Generate new policy wrt. new reward weights ---
        new_policy_nn = q_learning(n_steps, dw, w)

        # --- Step 3: Compute new feature expectations from policy ---
        mu_new = feature_expectation_nn(new_policy_nn, dw, gamma, n_steps)
        mu_list.append(mu_new)
        if print_results:
            print(f'Iteration {i} feature expectations: {mu_new}')
            print(f'Policy Difference: {policy_difference(w, mu_e, mu_new)}')
            print('---')

    if print_results:
        print(f'Expert feature expectations: {mu_e}')

    return w_list, mu_list


def plot_weights(w_list):
    """
    Plots all reward weights during the IRL process
    :param w_list:
    :return:
    """
    x = np.arange(len(w_list))
    for i in range(16):
        plt.plot(x, np.array(w_list)[:, i], label=f'Weight {i}')
    plt.title("Weights over IRL process")
    plt.legend()
    plt.show()


def plot_fe(mu_list):
    """
    Plots all feature expectations during the IRL process
    :param mu_list:
    :return:
    """
    x = np.arange(len(mu_list))
    for i in range(16):
        plt.plot(x, np.array(mu_list)[:, i], label=f'FE {i}')
    plt.title("FEs over IRL process")
    plt.legend()
    plt.show()


def calculate_score(traj, w):
    """
    Calculates the score that a trajectory achieved given the reward weights w
    :param traj: trajectory with n (rows) steps and m (columns) features
    :param w: reward weight vector of size m
    :return: overall score of the trajectory
    """
    traj_length = len(traj)
    score = 0
    for i in range(len(traj)):
        # Convert trajectory elements from str to float if necessary
        score += np.inner([float(x) for x in traj[i]], w)  # mu_i * w_i
    # Normalise by trajectory length to avoid bias
    score = score / traj_length
    return score


if __name__ == '__main__':
    # --- Step 1: Create environment ---

    dw = DroneWorld(500, 0, 0, 1)
    n_traj = 20  # Number of trajectories that are created by the expert policies
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

    # Import trajectories
    traj_list = []
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        traj = []
        with open(file, 'r') as current_file:
            reader = csv.reader(current_file)
            for i, line in enumerate(reader):
                traj.append(line)
        traj_list.append(traj)

    # --- Step 3: Execute IRL ---
    w_list, mu_list = execute_irl(20, n_steps, 0.99, dw, traj_list)

    # --- Step 4: Plot Results ---
    plot_weights(w_list)
    plot_fe(mu_list)

    # --- Step 5: Gather Scores ---
    w = w_list[-1]

    print('w:')
    print(w)
    print('Traj 0:')
    print(traj_list[0])
    score_e = calculate_score(traj_list[0], w)  # First expert trajectory

    # Generate random trajectory
    traj_r = dw.execute_policy_get_traj('random', n_steps)
    score_r = calculate_score(traj_r, w)

    print(f'Expert score: {score_e}')
    print(f'Random score: {score_r}')


