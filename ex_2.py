from irl import *
import utils
from droneworld import DroneWorld

pol_comb = [
    ['avoid_o', 'random'],
    ['avoid_p', 'random'],
    ['avoid_a', 'random'],
    ['random', 'avoid_o'],
    ['random', 'avoid_p'],
    ['random', 'avoid_a'],
    ['avoid_o', 'avoid_p'],
    ['avoid_o', 'avoid_a'],
    ['avoid_p', 'avoid_o'],
    ['avoid_p', 'avoid_a'],
    ['avoid_a', 'avoid_p'],
    ['avoid_a', 'avoid_o']
]

generate_new_traj = True  # Flag that decides whether new trajectories should be recorded
irl_iterations = 80
n_traj = 100
n_traj_training = 20
n_steps = 500
gamma = 0.99

if __name__ == '__main__':
    # Iterate over all combinations of policies to generate results
    for comb in pol_comb:
        dw = DroneWorld(500, 0, 0, 2)
        pol_1 = comb[0]
        pol_2 = comb[1]
        traj_dir_1 = f'traj/{pol_1}'
        traj_dir_2 = f'traj/{pol_2}'

        if generate_new_traj:
            # Clear old files in folder
            if os.path.exists(f'traj/{pol_1}'):
                filelist = [f for f in os.listdir(traj_dir_1) if f.endswith(".csv")]
                for f in filelist:
                    os.remove(os.path.join(traj_dir_1, f))

            if os.path.exists(f'traj/{pol_2}'):
                filelist = [f for f in os.listdir(traj_dir_2) if f.endswith(".csv")]
                for f in filelist:
                    os.remove(os.path.join(traj_dir_2, f))

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
        for filename in os.listdir(traj_dir_1):
            file = os.path.join(traj_dir_1, filename)
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
        for filename in os.listdir(traj_dir_2):
            file = os.path.join(traj_dir_2, filename)
            traj = []
            with open(file, 'r') as current_file:
                reader = csv.reader(current_file)
                for i, line in enumerate(reader):
                    traj.append(line)
            traj_list_2.append(traj)

        print('---')
        print(f'Imported {len(traj_list_1)} trajectories using policy 1')
        print(f'Imported {len(traj_list_2)} trajectories using policy 2')
        print(f'Imported {len(traj_list_training)} training trajectories using policy 1')
        print('---')

        # --- IRL Training ---

        w_list, mu_list = execute_irl(irl_iterations, n_steps, gamma, dw, traj_list_training)
        w = w_list[-1]

        score_pol_1 = [calculate_score(traj, w) for traj in traj_list_1]
        score_pol_2 = [calculate_score(traj, w) for traj in traj_list_2]

        result_dir = f'results2/ex_2/{pol_1}_x_{pol_2}'
        if os.path.exists(result_dir):
            utils.clear_folder(result_dir)
        else:
            os.makedirs(result_dir)

        with open(f'{result_dir}/scores_pol_1.txt', 'w') as f:
            for e in score_pol_1:
                f.write(f'{e}\n')

        with open(f'{result_dir}/scores_pol_2.txt', 'w') as f:
            for e in score_pol_2:
                f.write(f'{e}\n')

        label = [f'Policy {pol_1}', f'Policy {pol_2}']
        plt.hist([score_pol_1, score_pol_2], density=False, bins=30, label=label)
        plt.legend()
        plt.ylabel('Count')
        plt.xlabel('Trajectory Score')
        plt.savefig(f'{result_dir}/hist_{pol_1}_x_{pol_2}.png')
        plt.show()
