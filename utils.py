import random

import numpy as np

"""
This file contains utility functions that are used throughout the whole IRL process
"""


def ccw(a, b, c):
    # Source: https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def intersect(a, b, c, d):
    # Source: https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def det(a, b):
    """
    Calculates the determinant of two vectors in two-dimensional space.
    :param a: First vector
    :param b: Second vector
    :return: Determinant
    """
    return a[0] * b[1] - a[1] * b[0]


def line_intersection_coordinates(l1, l2):
    """
    Calculates the coordinates of two lines at their intersection.
    The two points (l1, l2) define a line of infinite length.
    Only suitable for lines in two-dimensional space.
    Raises an exception if lines do not intersect.
    :param l1: First line ((x1, y1), (x2, y1))
    :param l2: Second line ((x1, y1), (x2, y1))
    :return: x and y coordinates of the intersection point
    """
    # Source: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
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
    """
    Calculates the euclidean distance between two points in two-dimensional space.
    :param p1: First point (x, y)
    :param p2: Second point (x, y)
    :return: Distance
    """
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def min_dist_line_seg_point(l, p):
    """
    Calculates the minimum distance between a line segment l and a point in 2D space
    :param l: Line segment (x1, y1, x2, y2) endpoint coordinates
    :param p: (xp, yp) coordinates
    :return (minimum distance from line segment to point, distance from first point in l to the target point)
    """
    dx = p[0] - l[0]
    dy = p[1] - l[1]
    dx_l = l[2] - l[0]
    dy_l = l[3] - l[1]
    dot_product = np.dot([dx, dy], [dx_l, dy_l])
    line_length_sq = dx_l**2 + dy_l**2
    flag = -1
    if line_length_sq != 0:
        flag = dot_product / line_length_sq
    if flag < 0:
        xx = l[0]
        yy = l[1]
    elif flag > 1:
        xx = l[2]
        yy = l[3]
    else:
        xx = l[0] + flag * dx_l
        yy = l[1] + flag * dy_l
    return dist(p, (xx, yy)), dist((l[0], l[1]), (xx, yy))


def get_random_action():
    x = random.randint(0, 3)
    if x == 0:
        return 'w'
    elif x == 1:
        return 'a'
    elif x == 2:
        return 's'
    else:
        return 'd'

