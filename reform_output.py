import pandas
import os
from compute import *
import scipy
import numpy

def reform_output_min_variance(sub) :
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
            ndata = numpy.array(v)
            mean = ndata.mean()
            top = [(i, abs(i-mean)) for i in v]
            top = sorted(top, key=lambda i:i[1])
            output_data[k] = [i[0] for i in top[:50]]

        with open(os.path.splitext(f)[0] + '_selection.csv', 'w') as fout:
            for k,v in output_data.items():
                for i in v:
                    fout.write(k)
                    print k
                    fout.write(',')
                    fout.write(str(i))
                    print str(i)
                    fout.write('\n')

def reform_output_random(sub) :
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
            output_data[k] = numpy.random.choise(v, 50)

        with open(os.path.splitext(f)[0] + '_selection.csv', 'w') as fout:
            for k,v in output_data.items():
                for i in v:
                    fout.write(k)
                    fout.write(',')
                    fout.write(str(i))
                    fout.write('\n')




if __name__ == '__main__':
    reform_output_min_variance(sys.argv[1])
