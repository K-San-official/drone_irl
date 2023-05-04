# Drone Inverse Reinforcement Learning #

---

Author: Konstantin Sandfort

Version: 1.0

Since: 01.04.2023

---

## Disclaimer: This project is work in progress. ##

With Inverse Reinforcement Learning (IRL), expert behaviour forms
policies that can be translated into reward functions that are
initially unknown. The goal is to evaluate drone piloting based on
expert data and to be able to understand the underlying decision-making.

---

## Getting Started: ##

Navigate to the file 'simulation2d.py' and execute the main function

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