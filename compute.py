import numpy
import sys
import re
import os
import pandas
import matplotlib.pyplot as plt
import math
from sympy import Point, Line, Segment
from numpy import sqrt
from scipy import stats
from help import *
import logging

logging.basicConfig(filename='running.log',format='%(asctime)s %(message)s',level=logging.DEBUG)

# read from csv file and get x,y values of points
def read_file(filename, usecols = ['X', 'Y']) :
    logging.info(filename)
    df = pandas.read_csv(filename, skiprows = 0, sep=',', usecols=usecols)
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
def compute_distances_between_two_points_set(points1, points2, check = None) :
    index = 0
    distances = []
    i = 0
    li = []
    while i < len(points1):
        p1 = points1[i]
        if index >= len(points2) - 1: break

        if check:
            if i < len(points1) - 1:
                if check(points2[index], points2[index+1], points1[i], points1[i+1]):
                    logging.warn("crossing~")

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

def check_segment_crossing(p1,p2,q1,q2) :
    p = Segment(p1, p2)
    q = Segment(q1, q2)
    return len(p.intersection(q)) > 0

def find_all_files(folder, ext, func = str.endswith):
    files = [f for f in os.listdir(folder) if func(f, ext)]
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

def compute(p1, p2) :
    s1 = subtraction(p1)
    s2 = subtraction(p2)
    d1, li = compute_distances_between_two_points_set(p1, p2, check_segment_crossing)
    d2, li = compute_distances_between_two_points_set(p2, p1, check_segment_crossing)
    return s1 + s2, d1 + d2

def output_csv(data, filename) :
    pdata = pandas.DataFrame(data)
    pdata.to_csv(filename)

def points_from_pairs(sub = ""):
    folder = os.getcwd()
    if sub != "":
        folder = os.path.join(folder, sub)
    files = find_all_files(folder, '.csv')
    pairs = make_file_pairs(files)
    for pair in pairs:
        f1, f2 = pair[0], pair[1]
        d1 = read_file(os.path.join(folder, f1))
        d2 = read_file(os.path.join(folder, f2))
        p1 = group_to_points(d1)
        p2 = group_to_points(d2)
        yield (f1,) + compute(p1, p2)

def points_from_single_file(sub = "") :
    folder = os.getcwd()
    if sub != "":
        folder = os.path.join(folder, sub)
    files = find_all_files(folder, '.csv')
    for f in files:
        d = read_file(os.path.join(folder, f))
        p = group_to_points(d)
        p1 = [v for i,v in enumerate(p) if not (i % 2)]
        p2 = [v for i,v in enumerate(p) if i % 2]
        yield (f,) +  compute(p1, p2)

def run(sub, output, pair = True):
    out_l = {'file':[], 'length':[]}
    out_d = {'file':[], 'dist':[]}
    if pair:
        results = points_from_pairs(sub)
    else:
        results = points_from_single_file(sub)
    for f, l, d in results:
        out_l['file'] += [f for i in l]
        out_l['length'] += l
        out_d['file'] += [f for i in d]
        out_d['dist'] += d

    output_csv(out_l, os.path.join(output, os.path.basename(sub) + '_output_length.csv'))
    output_csv(out_d, os.path.join(output, os.path.basename(sub) + '_output_dist.csv'))


def show_histogram(csv) :
    data = pandas.read_csv(csv)
    plt.figure()
    plt.hist(data['value'], bins=50)
    plt.title(os.path.basename(csv))
    ndata = numpy.array(data['value'])
    print ndata.mean()
    print ndata.var()
    plt.savefig(csv +'.png')
    plt.close()

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

def test_image(filename, sub, pair = True):
    folder = os.getcwd()
    folder = os.path.join(folder, sub)
    if pair:
        f1, f2 = os.path.join(folder, filename + '.csv'), os.path.join(folder, filename+'s.csv')
        d1 = read_file(os.path.join(folder, f1))
        d2 = read_file(os.path.join(folder, f2))
        p1 = group_to_points(d1)
        p2 = group_to_points(d2)
    else:
        d = read_file(os.path.join(folder, filename + '.csv'))
        p = group_to_points(d)
        p1 = [v for i,v in enumerate(p) if i % 2 == 0]
        p2 = [v for i,v in enumerate(p) if i % 2 != 0]
    plt.figure()
    x = [p.x for p in p1]
    y = [p.y for p in p1]
    plt.plot(x, y, c='r', marker='*')
    x = [p.x for p in p2]
    y = [p.y for p in p2]
    plt.plot(x, y, c='r', marker='.')
    d1,li = compute_distances_between_two_points_set(p1, p2)
    for i,l in enumerate(li):
        x = [p.x for p in l]
        y = [p.y for p in l]
        plt.plot(x, y, c='g', label=str(d1[i]))

    d2, li = compute_distances_between_two_points_set(p2, p1)
    for i,l in enumerate(li):
        x = [p.x for p in l]
        y = [p.y for p in l]
        plt.plot(x, y, c='b', label=str(d2[i]))

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(filename)
    plt.gca().set_aspect('equal', adjustable='box')
    #plt.show()

    ax=plt.gca()                                # get the axis
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.savefig(os.path.join(folder, filename+'.png'))
    plt.close()

def output_all_image(sub, pair = True):
    folder = os.getcwd()
    folder = os.path.join(folder, sub)
    files = find_all_files(folder, '.csv')
    if pair:
        pairs = make_file_pairs(files)
        for pair in pairs:
            test_image(os.path.splitext(pair[0])[0], sub, pair)
    else:
        for f in files:
            test_image(os.path.splitext(f)[0], sub, pair)

def plot_image(sub):
    folder = os.getcwd()
    folder = os.path.join(folder, sub)
    files = find_all_files(folder, '_selection.csv', str.endswith)
    for f in files:
        show_histogram(os.path.join(folder, f))

if __name__ == '__main__':
    logging.info('*******    run    *******')
    logging.info(' '.join(sys.argv[1:]))
    if sys.argv[1] == 'run':
        run(sys.argv[2], sys.argv[4], eval(sys.argv[3]))
    elif sys.argv[1] == 'image':
        output_all_image(sys.argv[2], eval(sys.argv[3]))
    elif sys.argv[1] == 'plot':
        plot_image(sys.argv[2])
