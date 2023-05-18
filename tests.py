import utils as ut
import irl
import unittest

class Testing(unittest.TestCase):
    def testIntersect(self):
        a = (0, 0)
        b = (1, 1)
        c = (0, 1)
        d = (1, 0)
        self.assertEqual(ut.intersect(a, b, c, d), True)

    def testIntersectCoord(self):
        a = (0, 0)
        b = (1, 1)
        c = (0, 1)
        d = (1, 0)
        self.assertEqual(ut.line_intersection_coordinates((a, b), (c, d)), (0.5, 0.5))

    def testCalculateScore(self):
        traj = [[1, 1], [1, 1], [0, 0], [0, 1], [0, 0]]
        w = [1, 1]
        self.assertEqual(irl.calculate_score(traj, w), 1)


if __name__ == '__main__':
    unittest.main()


