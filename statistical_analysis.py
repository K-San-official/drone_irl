import scipy.stats as stats
import numpy as np

if __name__ == '__main__':
    sample_1_path = 'results/experiment_2/scores_pol_1.txt'
    sample_2_path = 'results/experiment_2/scores_pol_2.txt'
    sample_size = 100

    sample_1 = []
    sample_2 = []

    # Read data from files
    with open(sample_1_path, 'r') as current_file:
        for line in current_file:
            sample_1.append(float(line.rstrip()))

    with open(sample_2_path, 'r') as current_file:
        for line in current_file:
            sample_2.append(float(line.rstrip()))

    arr_1 = np.array(sample_1[:sample_size])
    arr_2 = np.array(sample_2[:sample_size])
    print(arr_1)
    print(arr_2)

    print(stats.ttest_ind(a=arr_1, b=arr_2, equal_var=False))

