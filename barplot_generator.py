import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    values = [
        -0.0781,
        0.0057,
        -0.0468,
        -0.4989,
        0.2056,
        0.1712,
        -0.2304,
        0.0263,
        -0.2969,
        0.4720,
        -0.4899,
        0.1205,
        -0.1842,
        0.1771,
        -0.5213,
        0.3382,
    ]

    x = np.arange(1, 17)

    plt.bar(x, values)
    plt.xlabel('Reward Weight Index')
    plt.ylabel('Weight Value')
    plt.xticks(x)
    plt.show()

