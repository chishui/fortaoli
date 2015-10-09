import numpy
import re
import os
import pandas
import matplotlib.pyplot as plt
import math
from sympy import Point, Line, Segment
from numpy import sqrt
from scipy import stats

# read from csv file and get x,y values of points
def read_file(filename) :
    print filename
    df = pandas.read_csv(filename, skiprows = 0, sep=',', usecols=['X', 'Y'])
    df.dropna(how="all", inplace=True)
    return df

# group x,y into a point object
def group_to_points(data) :
    return [Point(v, data['Y'][i], evaluate=False) for i,v in enumerate(data['X'])]

# compute distance between two distance:
def subtraction(points) :
    return [points[i].distance(points[i-1]) for i in range(1, len(points))]

# check if projection of a point to line is between two points
def is_projection_between_two_points(p, p1, p2) :
    #return (p1.x - p.x)*(p2.x - p.x) <= 0 and (p1.y - p.y) * (p2.y - p.y) <= 0
    seg = Segment(p1, p2)
    return seg.contains(p)

# compute distances between point and line in two points set
def compute_distances_between_two_points_set(points1, points2) :
    index = 0
    distances = []
    i = 0
    li = []
    while i < len(points1):
        p1 = points1[i]
        if index >= len(points2) - 1: break
        line = Line(points2[index], points2[index + 1])
        pro = line.projection(p1)
        if is_projection_between_two_points(pro, points2[index], points2[index + 1]):
            distances.append(p1.distance(pro))
            li.append([p1, pro])
            index += 1
        else:
            if pro.distance(points2[index + 1]) < pro.distance(points2[index]):
                i -= 1
                index += 1
        i += 1
    return distances, li

def find_all_files(folder, ext):
    files = [f for f in os.listdir(folder) if os.path.splitext(f)[-1] == ext]
    return files

def make_file_pairs(files) :
    pairs = []
    pattern = re.compile(r'\w+(-\d+){3,4}.csv')
    #pattern = re.compile(r'\w+.csv')
    for f in files :
        if pattern.match(f):
            another = f[:f.index('.csv')] + 's.csv'
            pairs.append((f, another))
    return pairs

def do():
    folder = os.path.join(os.getcwd(), 'data')
    files = find_all_files(folder, '.csv')
    pairs = make_file_pairs(files)
    li = []
    for pair in pairs:
        f1, f2 = pair[0], pair[1]
        d1 = read_file(os.path.join(folder, f1))
        d2 = read_file(os.path.join(folder, f2))
        p1 = group_to_points(d1)
        p2 = group_to_points(d2)
        li.append(p1)
        li.append(p2)
        s1 = subtraction(p1)
        s2 = subtraction(p2)
        dist, ver = compute_distances_between_two_points_set(p2, p1)
        print dist
        li = li + ver
    show_image(li)

def compute():
    out_l = {'file':[], 'length':[]}
    out_d = {'file':[], 'dist':[]}

    folder = os.path.join(os.getcwd(), 'data')
    files = find_all_files(folder, '.csv')
    pairs = make_file_pairs(files)
    for pair in pairs:
        f1, f2 = pair[0], pair[1]
        d1 = read_file(os.path.join(folder, f1))
        d2 = read_file(os.path.join(folder, f2))
        p1 = group_to_points(d1)
        p2 = group_to_points(d2)
        s1 = subtraction(p1)
        for s in s1:
            out_l['file'].append(f1)
            out_l['length'].append(s)
        s2 = subtraction(p2)
        for s in s2:
            out_l['file'].append(f2)
            out_l['length'].append(s)

        dist, ver = compute_distances_between_two_points_set(p1, p2)
        for d in dist:
            out_d['file'].append(f1)
            out_d['dist'].append(d)
        dist, ver = compute_distances_between_two_points_set(p2, p1)
        for d in dist:
            out_d['file'].append(f2)
            out_d['dist'].append(d)

    data = pandas.DataFrame(out_l)
    data.to_csv('output_length.csv', sep=",")
    data = pandas.DataFrame(out_d)
    data.to_csv('output_dist.csv', sep=",")

    #out_length = open('output_length.csv', 'w')
    #out_dist = open('output_dist.csv', 'w')
    #out_length.close()
    #out_dist.close()

def show_histogram() :
    data = pandas.read_csv("output_length.csv")
    length = [data['length'][i] for i,v in enumerate(data['file']) if v.startswith("592")]
    plt.hist(length, bins=150)
    plt.show()
    ndata = numpy.array(length)
    print ndata.mean()
    print ndata.var()

def show_image(points_list) :
    plt.figure()
    for i, li in enumerate(points_list):
        x = [p.x for p in li]
        y = [p.y for p in li]
        plt.plot(x, y, c='r', marker='*' if i < 2 else '.')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('$X*Y$')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


if __name__ == '__main__':
    compute()
    #show_histogram()
