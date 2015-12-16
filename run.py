import sys
import os
import datetime

def output_folder_name():
	now = datetime.datetime.now()
	return 'output_' + now.strftime("%Y%m%d%H%m")

def enumerate_folder(parent):
    folders = []
    for f in os.listdir(parent):
	f = os.path.join(parent, f)
        if os.path.isdir(f):
            folders.append(f)
    return folders

def run(folder, output = None, include = [1, 2, 3, 4, 5]):
    folder = os.path.abspath(folder)
    subfolders = enumerate_folder(folder)

    if not output:
        output = os.path.join(folder, output_folder_name())
    output = os.path.abspath(output)
    if not os.path.exists(output) :
        os.mkdir(output)

    print "reform file names"
    if 1 in include:
        for sub in subfolders:
            os.system("python help.py \"" + sub + "\"")

    print "run compute distances"
    if 2 in include:
        for sub in subfolders:
            os.system("python compute.py run \"" + sub + "\" False \"" + output + "\"")

    print "output images"
    if 3 in include:
        for sub in subfolders:
            os.system("python compute.py image \"" + sub + "\" False \"")

    print "selection and output distributed images"
    if 4 in include:
        os.system("python reform_output.py \"" + output + "\" random")

    print "output distributive images"
    if 5 in include:
        print "python compute.py plot \"" + output + '\"'
        os.system("python compute.py plot \"" + output + '\"')


if __name__ == '__main__':
    output = None
    include = [1,2,3,4,5]
    if len(sys.argv) > 2:
        output = sys.argv[2]
    if len(sys.argv) > 3:
        include = map(int, list(sys.argv[3]))
    run(sys.argv[1], output = output, include = include)
