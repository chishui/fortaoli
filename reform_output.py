import pandas
import os
from compute import *
import scipy
import numpy

def generate_50_min_variance(data) :
    ndata = numpy.array(data)
    mean = ndata.mean()
    top = [(i, abs(i-mean)) for i in data]
    top = sorted(top, key=lambda i:i[1])
    return [i[0] for i in top[:50]]


def generate_50_random(data) :
    return numpy.random.choice(data, 50)


def reform_output(sub, generate_function) :
    folder = os.path.join(os.getcwd(),sub)
    files = find_all_files(folder, '.csv')
    for f in files:
        keyword = os.path.splitext(f)[0].split('_')[-1]
        data = read_file(os.path.join(folder,f), usecols=['file', keyword])
        names = data['file']
        values = data.get(keyword)
        buffer = {}
        for i, name in enumerate(names) :
            tag = '-'.join(name.split('-')[:2])
            buffer.setdefault(tag, []).append(values[i])

        output_data = {}
        for k,v in buffer.items():
            if len(v) <= 50:
                output_data[k] = v
                print len(v), "<= 50", f, k
                continue
            output_data[k] = generate_function(v)

        postfix = '_selection.csv' if sys.argv[2] == 'closest' else '_random_selection.csv'
        with open(os.path.join(folder, os.path.splitext(f)[0] + postfix), 'w') as fout:
            fout.write('tag,value\n')
            for k,v in output_data.items():
                for i in v:
                    fout.write(k)
                    fout.write(',')
                    fout.write(str(i))
                    fout.write('\n')


if __name__ == '__main__':
    if sys.argv[2] == 'random':
        reform_output(sys.argv[1], generate_50_random)
    elif sys.argv[2] == 'closest':
        reform_output(sys.argv[1], generate_50_min_variance)
