import os
import re
import sys
from compute import *

def convert_xls_to_csv():
    import xlrd
    import csv
    import subprocess

    cur = os.getcwd()
    files = [f for f in os.listdir(os.path.abspath(cur)) if os.path.splitext(f)[-1] == '.xls']
    for f in files:
        csv_file = os.path.splitext(f)[0] + '.csv'
        command = 'in2csv %s > %s' % (os.path.join(cur,f) ,os.path.join(cur,csv_file))
        print command
        proc = subprocess.Popen(command)
        proc.wait()

def convert_delimiter(filename, fm, to) :
    with open(filename, 'r') as f:
        lines = f.readlines()
        nl = [to.join(line.split(fm)) for line in lines]

    with open(filename, 'w') as f:
        f.writelines(nl)

def reform_file_name(filename, fm, to) :
    return filename.replace(fm, to)

def change_file_name(folder) :
#    files = os.listdir(folder)
    files = find_all_files(folder, '.csv')
    for f in files:
        nf = reform_file_name(f, '_', '-')
        print f, nf
        os.rename(os.path.join(folder, f),  os.path.join(folder, nf))

def convert_file_delimiter(folder) :
    #files = os.listdir(folder)
    files = find_all_files(folder, '.csv')
    for f in files:
        convert_delimiter(os.path.join(folder, f), '\t', ',')



if __name__ == '__main__' :
    if len(sys.argv) > 1:
        data = sys.argv[1]
        folder = os.getcwd()
        folder = os.path.join(folder, data)
        change_file_name(folder)
        convert_file_delimiter(folder)
