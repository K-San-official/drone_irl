# Drone Inverse Reinforcement Learning #

---

Author: Konstantin Sandfort

Version: 1.0

Since: 01.04.2023

---

## Dependencies ##

The following packages need to be installed for this application:

- Numpy
- TensorFlow
- Matplotlib
- Sklearn
- Tkinter
- Scipy

---

## Getting Started ##

Navigate to the file 'simulation2d.py' and execute the main function to execute a GUI that allows
a user to navigate the drone with the keys [W, A, S, D].

---

## Experiments ##

There are 4 experiments in total that are stated as follows:

1) How does the generated reward function change
throughout the IRL iterations? It is hypothesised that
reward weights are stabilising over a large number of
iterations during the IRL process.
2) Is it possible to identify whether a trajectory follows
a certain policy by creating a score with a trained
reward function? It is hypothesised that the score
of trajectories following the expert policy that is used
for learning is significantly higher than the score of
trajectories following other policies.
3) How well-suited are the reward functions for un-
known environments? The hypothesis is similar to the
one from research question 2 with the only difference
that trajectories used to calculate scores originate from
a different environment than the ones used for learning.
4) What information can be extracted from the weights
of a reward function? It is hypothesised that the reward
weights corresponding to sensing people will be close
to zero for an expert policy that only avoids obstacles
but disregards people.

In order to obtain results, the files ex_1.py, ex_2.py and ex_3.py can be executed.
The fourth experiment relies on the prior execution of ex_1. By executing barplot_generater.py,
results for the fourth experiment will be created.

The file statistical_analysis.py provides a tool to calculate the statistical significance
for both experiment 2 and 3.

---

## Simulation ##

A drone is wandering around in a two-dimensional field. There are people and obstacles placed at random
positions. Neither of them moves during the runtime of the simulation. With every new start of the application,
a new random environment is created.

---

## Inverse Reinforcement Learning ##

### Preliminaries ###

Reinforcement Learning is based on a 5-Tuple `(S, A, P_a{s, s'}, γ, R)` for a Markov Decision Process.

- `S` = State Space
- `A` = Action Set
- `P_a{s, s'}` = Transition Probabilities from the current state to the next one
- `γ` = Discount Factor
- `R` = Reward Function

In normal (forward) RL, the goal is to find an optimal policy with a given reward function.
An optimal policy will maximise the reward and choose the optimal action `a` for a given state `s`.

With Inverse Reinforcement Learning (IRL), the reward function is not given but the agent acts
accordingly to its own policy. We assume that expert behaviour leads to a good policy.
The goal is to find a reward function based on a fixed set of expert demonstrations (trajectories).

For this simulation, the environment is not stochastic. If a certain action `a` is performed in state `s`,
we can certainly compute the next state `s'`, so the transition probabilities `P_a` are either 0 or 1.

### State Space ###

The drone is moving in a continuous two-dimensional field. The position can be described unambiguously
by the x and y coordinates and the current rotation of the drone. This description however is meaningless
in terms of what the drone perceives in the current environment. 
The state `s` of the drone is denoted as a vector of exactly 16 elements with normalised floating point
values from 0 to 1.

- Entries 1 - 7: Directional sensors for people from left to right
- Entries 8 - 14: Directional sensors for obstacles from left to right
- Entry 15: Distance to the closest person
- Entry 16: Distance to the closest obstacle

The normalised values are high for close distances and low for distances far away.
It is important to mention that people in this simulation are "see-through", so the drone is able to detect
obstacles behind people in a straight line of sight, but it is not able to detect people behind obstacles.
The last two entries disregard anything in-between and just indicate proximity. 

### Actions ###

There are 4 possible actions denoted by the characters `w`, `a`, `s`, `d`, corresponding to normal
keyboard controls (up, left, down, right)

For forward and backward movement, the drone moves by a fixed step.
Turning left and right happens on the spot without any change of coordinates.