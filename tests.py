import utils as ut

if __name__ == '__main__':
    a = (134.30229109146936, 434.916540491883)
    b = (284.3022910914693, 434.916540491883)
    c = (14.113893599659095, 422.32066425227714)
    d = (4.0599547393179165, 501.3347123594574)
    print(ut.intersect(a, b, c, d))
    print(ut.line_intersection_coordinates((a, b), (c, d)))


