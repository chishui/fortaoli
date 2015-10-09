import unittest
from compute import *
from shapely.geometry import LineString
import shapely.geometry
import sympy

class Test(unittest.TestCase) :
#    def test_read_file(self) :
#        data = read_file("Results.csv")
#        self.assertEqual(len(data['X']), 11)
#        self.assertEqual(len(data['Y']), 11)
#        self.assertEqual(data['X'][10], 4.471)

    def test_shapely(self) :
        self.assertEqual(point_line_dist(Point(0,2), Point(0,0), Point(1,1)),
                LineString([(0,0), (1,1)]).project(shapely.geometry.Point(0,2)))
        self.assertEqual(sympy.Line(sympy.Point(10,10), sympy.Point(41,-1)).projection(sympy.Point(0.1,2.3)).distance(sympy.Point(0.1, 2,3)),
                LineString([(0,0), (1,1)]).project(shapely.geometry.Point(0,2)))



    def test_point_to_line_distance(self) :
        q = Point(0, 2)
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        self.assertAlmostEqual(point_line_dist(Point(0,2), Point(0,0), Point(1,1)), 1.414, 3)

    def is_projection_between_two_points(self) :
        # normal true
        self.assertTrue(is_projection_between_two_points(Point(2,2), Point(1, 1), Point(4,4)))
        # normal false
        self.assertFalse(is_projection_between_two_points(Point(0,0), Point(1, 1), Point(4,4)))
        self.assertFalse(is_projection_between_two_points(Point(5,5), Point(1, 1), Point(4,4)))
        # edge cases
        self.assertTrue(is_projection_between_two_points(Point(1,1), Point(1, 1), Point(4,4)))
        self.assertTrue(is_projection_between_two_points(Point(4,4), Point(1, 1), Point(4,4)))

#    def test_point_class_subtraction(self) :
#        self.assertAlmostEqual(Point(0, 0).distance(Point(1, 1)), 1.414, 3)
#        self.assertAlmostEqual(Point(2.5, 1.5).distance(Point(1.5, 0.5)), 1.414, 3)
#        self.assertAlmostEqual(Point(0, 0).distance(Point(0, 0)), 0)
#        self.assertAlmostEqual(Point(-3.2, -1.5).distance(Point(1.5, 0.5)), 5.1078, 4)

    def subtraction(self) :
        points = [Point(-1,-1), Point(0, 0), Point(3, 3), Point(-3, -3)]
        self.assertListEqual(subtraction(points), [1.414, 2.242, 8.485])

if __name__ == '__main__':
    unittest.main()
