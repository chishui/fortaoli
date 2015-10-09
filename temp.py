import numpy
import re
import os
import pandas
from scipy.spatial import distance
from numpy import sqrt
import matplotlib.pyplot as plt

class Point(object) :
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, p):
        #return math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)
        return distance.euclidean((self.x, self.y), (p.x, p.y))

    def __repr__(self) :
        return ('x=%f, y=%f') % (self.x, self.y)


# read from csv file and get x,y values of points
def read_file(filename) :
    df = pandas.read_csv(filename, skiprows = 0, sep=',', usecols=['X', 'Y'])
    df.dropna(how="all", inplace=True)
    return df

# group x,y into a point object
def group_to_points(data) :
    return [Point(v, data['Y'][i]) for i,v in enumerate(data['X'])]

# compute distance between two distance:
def subtraction(points) :
    return [points[i] - points[i-1] for i in range(1, len(points))]

def get_projection_point(p, p1, p2) :
    y3,x3 = p.y, p.x
    (y1,x1),(y2,x2) = (p1.y, p1.x), (p2.y, p2.x)

    dx21 = (x2-x1)
    dy21 = (y2-y1)

    lensq21 = dx21*dx21 + dy21*dy21
    if lensq21 == 0:
        #20080821 raise ValueError, "zero length line segment"
        dy = y3-y1
        dx = x3-x1
        return sqrt( dx*dx + dy*dy )  # return point to point distance

    u = (x3-x1)*dx21 + (y3-y1)*dy21
    u = u / float(lensq21)

    x = x1+ u * dx21
    y = y1+ u * dy21
    return Point(x, y)

# compute point to line distance
def point_line_dist(p, p1, p2, testSegmentEnds=False):
    projection = get_projection_point(p, p1, p2)
    return p - projection

# check if projection of a point to line is between two points
def is_projection_between_two_points(p, p1, p2) :
    return (p1.x - p.x)*(p2.x - p.x) <= 0 and (p1.y - p.y) * (p2.y - p.y) <= 0

# compute distances between point and line in two points set
def compute_distances_between_two_points_set(points1, points2) :
    index = 0
    distances = []
    i = 0
    li = []
    while i < len(points1):
        p1 = points1[i]
        if index >= len(points2) - 1: break
        pro = get_projection_point(p1, points2[index], points2[index + 1])
        if is_projection_between_two_points(pro, points2[index], points2[index + 1]):
            distances.append(p1 - pro)
            li.append([p1, pro])
            index += 1
       else:
            if pro - points2[index + 1] < pro - points2[index]:
                i -= 1
                index += 1
        i += 1
    return distances, li

def find_all_files(ext):
    files = [f for f in os.listdir(os.path.abspath(os.getcwd())) if os.path.splitext(f)[-1] == ext]
    return files

def make_file_pairs(files) :
    pairs = []
    pattern = re.compile(r'\w+-\d+-\d+.csv')
    for f in files :
        if pattern.match(f):
            another = f[:f.index('.csv')] + 's.csv'
            pairs.append((f, another))
    return pairs

def do():
    files = find_all_files('.csv')
    pairs = make_file_pairs(files)
    li = []
    for pair in pairs:
        f1, f2 = pair[0], pair[1]
        d1 = read_file(f1)
        d2 = read_file(f2)
        p1 = group_to_points(d1)
        p2 = group_to_points(d2)
        li.append(p1)
        li.append(p2)
        s1 = subtraction(p1)
        s2 = subtraction(p2)
        dist, ver = compute_distances_between_two_points_set(p1, p2)
        li = li + ver
    show_image(li)

def show_image(points_list) :
    plt.figure()
    for li in points_list:
        x = [p.x for p in li]
        y = [p.y for p in li]
        plt.plot(x, y, c='r', marker='*')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('$X*Y$')
    plt.show()


def show(p1, p2):
    x1 = [p.x for p in p1]
    y1 = [p.y for p in p1]
    x2 = [p.x for p in p2]
    y2 = [p.y for p in p2]
    plt.figure()
    plt.plot(x1,y1,c='r',marker='*')
    plt.plot(x2,y2,c='r',marker='*')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('$X*Y$')
    plt.show()


if __name__ == '__main__':
    do()
