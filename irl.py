from droneworld import DroneWorld
import os

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


def execute_irl(epochs: int, gamma: float, dw: DroneWorld, traj_path: str):
    # Step 1:
    pass


if __name__ == '__main__':
    # --- Step 1: Create environment ---

    dw = DroneWorld(500, 0, 0, 1)
    n_traj = 10  # Number of trajectories that are created by the expert policies
    n_steps = 500  # Number of steps performed for each trajectory
    pol_type = 'avoid_o'

    # --- Step 2: Create expert trajectories ---

    # Clear old files in folder
    directory = f'traj/{pol_type}'
    filelist = [f for f in os.listdir(directory) if f.endswith(".csv")]
    for f in filelist:
        os.remove(os.path.join(directory, f))

    # Record new trajectories from demonstration runs
    for i in range(n_traj):
        print(f'Creating Trajectory {i}')
        dw.execute_policy(pol_type, n_steps)

    # --- Step 3: Execute IRL ---
