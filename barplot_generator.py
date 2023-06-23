import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

"""
This file generates barplots for recorded reward weights of multiple IRL processes.
Part of experiment 4.
"""

if __name__ == '__main__':

    # Import values from file
    filepath = 'reward_weights/weights_avoid_o.txt'
    file = open(filepath, 'r')
    lines = file.readlines()
    values = []

    for line in lines:
        weights_str = line.split()
        # Convert to float
        weights = [float(x) for x in weights_str]
        values.append(weights)

    arr = np.array(values)
    means = arr.mean(axis=0)  # Column means
    stds = arr.std(axis=0)  # Standard Deviations

    x_values = np.arange(1, len(values[0]) + 1)

    # Build plot
    fig, ax = plt.subplots()
    ax.bar(x_values, means, yerr=stds, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_xlabel('Reward Weight Index')
    ax.set_ylabel('Reward Weight Value')
    ax.set_xticks(x_values)
    ax.yaxis.grid(True)

    # Save the figure and show
    plt.tight_layout()
    plt.savefig('results2/ex_4/bar_plot_with_error_bars.png')
    plt.show()

    # T-Test for absolute values
    arr_abs = np.abs(arr)
    abs_sum = np.sum(arr_abs, axis=0)  # Sum of absolute values for each reward weight

    group_people = np.append(abs_sum[0:7], abs_sum[14])
    group_obst = np.append(abs_sum[7:14], abs_sum[15])

    print('-----')
    print(f'Mean Group People: {np.mean(group_people)}')
    print(f'Mean Group Obstacles: {np.mean(group_obst)}')

    print(stats.ttest_ind(group_people, group_obst, equal_var=False))
