"""
This file contains utility functions that are used throughout the whole IRL process
"""


def ccw(a, b, c) -> bool:
    # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def _intersect(a, b, c, d) -> bool:
    # https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def intersect(l1, l2):
    # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
    xdiff = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
    ydiff = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])
    div = det(xdiff, ydiff)
    if div == 0:
        return False
    else:
        return True

def line_intersection_coordinates(l1, l2):
    # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
    xdiff = (l1[0][0] - l1[1][0], l2[0][0] - l2[1][0])
    ydiff = (l1[0][1] - l1[1][1], l2[0][1] - l2[1][1])
    div = det(xdiff, ydiff)
    if div == 0:
       return -1  # Lines do not intersect
    d = (det(*l1), det(*l2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
