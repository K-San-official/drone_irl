import gc

import utils
from irl import *

# Change the following parameters as preferred:
training_policies = [
    'avoid_o',
    'avoid_p',
    'avoid_a',
    'random'
]

n_traj = 20
n_steps = 250
irl_iterations = 40
show_log = True
generate_new_traj = True

if __name__ == '__main__':

    # Iterate over each trajectory and perform an individual IRL routine for each one.
    for pol_type in training_policies:

        # --- Step 1: Create environment ---

        dw = DroneWorld(500, 0, 0, 2)
        traj_dir = f'traj/{pol_type}'

        # --- Step 2: Create expert trajectories ---

        if generate_new_traj:
            # Clear old files in folder
            utils.clear_folder(traj_dir)

            # Record new trajectories from demonstration runs
            for i in range(n_traj):
                print(f'Creating Trajectory {i}')
                dw.execute_policy(pol_type, n_steps)

        # Import trajectories
        traj_list = []
        for filename in os.listdir(traj_dir):
            file = os.path.join(traj_dir, filename)
            traj = []
            with open(file, 'r') as current_file:
                reader = csv.reader(current_file)
                for i, line in enumerate(reader):
                    traj.append(line)
            traj_list.append(traj)

        # --- Step 3: Execute IRL ---

        w_list, mu_list = execute_irl(irl_iterations, n_steps, 0.99, dw, traj_list)

        result_dir = f'results2/ex_1/{pol_type}'
        if os.path.exists(result_dir):
            utils.clear_folder(result_dir)
        else:
            os.makedirs(result_dir)

        # --- Step 4: Plot Results ---
        plot_weights(w_list, result_dir, pol_type)
        plot_fe(mu_list, result_dir, pol_type)

        # --- Step 5: Gather Scores ---
        w = w_list[-1]

        # Saves weights to file
        with open(f'{result_dir}/weights.txt', 'w') as f:
            for line in w:
                f.write(f'{str(line)}\n')

        score_e = calculate_score(traj_list[0], w)  # First expert trajectory

        # Generate random trajectory
        traj_r = dw.execute_policy_get_traj('random', n_steps)
        score_r = calculate_score(traj_r, w)

        with open(f'{result_dir}/score_comparison.txt', 'w') as f:
            f.write(f'{pol_type} Score: {score_e}\n')
            f.write(f'random Score: {score_r}\n')

        print(f'Expert score: {score_e}')
        print(f'Random score: {score_r}')

        # Save weights to file
        reward_weights_file = f'reward_weights/weights_{pol_type}.txt'
        with open(reward_weights_file, 'a') as f:
            for weight in w:
                f.write(f'{weight} ')
            f.write('\n')

        # Clean up to save ram
        del w_list, mu_list, traj_list
        gc.collect()
