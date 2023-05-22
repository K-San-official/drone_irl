import os
import csv
import matplotlib.pyplot as plt

from irl import *
from droneworld import DroneWorld

if __name__ == '__main__':

    # Create environment
    dw = DroneWorld(500, 0, 0, 2)
    n_traj = 100
    n_traj_training = 20
    n_steps = 500
    pol_1 = 'avoid_o'
    pol_2 = 'random'
    directory_1 = f'traj/{pol_1}'
    directory_2 = f'traj/{pol_2}'
    generate_new_traj = False  # Flag that decides whether new trajectories should be recorded

    if generate_new_traj:
        # Clear old files in folder
        if os.path.exists(f'traj/{pol_1}'):
            filelist = [f for f in os.listdir(directory_1) if f.endswith(".csv")]
            for f in filelist:
                os.remove(os.path.join(directory_1, f))

        if os.path.exists(f'traj/{pol_2}'):
            filelist = [f for f in os.listdir(directory_2) if f.endswith(".csv")]
            for f in filelist:
                os.remove(os.path.join(directory_2, f))

        # Record new trajectories from demonstration runs
        for i in range(n_traj):
            print(f'Creating Trajectory {i + 1}')
            dw.execute_policy(pol_1, n_steps)
            dw.execute_policy(pol_2, n_steps)

        for i in range(n_traj_training):
            print(f'Creating Training Trajectory {i + 1}')
            dw.execute_policy(pol_1, n_steps)

    # Import trajectories
    traj_list_1 = []
    traj_list_2 = []
    traj_list_training = []

    print(f'Importing trajectories with {pol_1} policy')
    for filename in os.listdir(directory_1):
        file = os.path.join(directory_1, filename)
        traj = []
        with open(file, 'r') as current_file:
            reader = csv.reader(current_file)
            for i, line in enumerate(reader):
                traj.append(line)
        if len(traj_list_1) < n_traj:
            traj_list_1.append(traj)
        else:
            traj_list_training.append(traj)

    print(f'Importing trajectories with {pol_2} policy')
    for filename in os.listdir(directory_2):
        file = os.path.join(directory_2, filename)
        traj = []
        with open(file, 'r') as current_file:
            reader = csv.reader(current_file)
            for i, line in enumerate(reader):
                traj.append(line)
        traj_list_2.append(traj)

    print('---')
    print(f'Imported {len(traj_list_1)} trajectories using policy 1')
    print(f'Imported {len(traj_list_2)} trajectories using policy 1')
    print(f'Imported {len(traj_list_training)} training trajectories using policy 1')
    print('---')

    # --- IRL Training ---

    w_list, mu_list = execute_irl(20, n_steps, 0.99, dw, traj_list_training)
    w = w_list[-1]

    score_pol_1 = [calculate_score(traj, w) for traj in traj_list_1]
    score_pol_2 = [calculate_score(traj, w) for traj in traj_list_2]

    print(score_pol_1)
    print(score_pol_2)

    # TODO: Save scores to file

    plt.hist(score_pol_1, density=True, bins=30)  # density=False would make counts
    plt.hist(score_pol_2, density=True, bins=30)  # density=False would make counts
    plt.ylabel('Probability')
    plt.xlabel('Data')
    plt.show()


