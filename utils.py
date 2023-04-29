import numpy as np

"""
This file contains utility functions that are used throughout the whole IRL process
"""


def ccw(a, b, c):
    # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def intersect(a, b, c, d):
    # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    return ccw(a, c, c) != ccw(b, c, c) and ccw(a, b, c) != ccw(a, b, d)


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


def min_dist_line_seg_point(l, p):
    """
    Calculates the minimum distance between a line segment l and a point in 2D space
    :param l: (x1, y1, x2, y2) endpoint coordinates
    :param p: (xp, yp) coordinates
    """
    dx = p[0] - l[0]
    dy = p[1] - l[1]
    dx_l = l[2] - l[0]
    dy_l = l[3] - l[1]
    dot_product = np.dot([dx, dx_l], [dy, dy_l])
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
    return dist((p[0] - xx), p[1] - yy)

