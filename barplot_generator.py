import numpy as np
import matplotlib.pyplot as plt

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

    x_values = np.arange(len(values[0]))

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
