from sympy import Point, Line, Segment
p1, p2, p3 = Point(0, 0), Point(1, 1), Point(1, 2)
l1 = Line(p1, p2)

print l1.contains(Point(-1,-1))
print l1.contains(Point(1,1))

print l1.contains(Point(0.1,0.1))
