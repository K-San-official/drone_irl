import numpy as np

"""
This file contains utility functions that are used throughout the whole IRL process
"""

def ccw(A,B,C):
    # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def line_intersection_coordinates(l1, l2):
    # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
    xdiff = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
    ydiff = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])
    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')  # Lines do not intersect
    d = (det(*l1), det(*l2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def dist(p1, p2) -> float:
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
