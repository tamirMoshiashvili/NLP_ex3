from time import time

import numpy as np
import sys


def cosine(u, v):
    # u and v are np-arrays
    return np.dot(u, v) / (np.sqrt(np.dot(u, u)) * np.sqrt(np.dot(v, v)))


def read_dataset_file(filename):
    f = open(filename, 'r')
    file_lines = f.readlines()
    f.close()
    print 'read the file successfully'
    return file_lines


# get a list where each item is a dictionary
def parse_dataset(filename):
    print 'start parsing the file'
    ls = []
    i = 1

    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            if len(line) != 0:  # skip empty lines
                # create dictionary out of the given line,
                # according to the format in https://depparse.uvt.nl/DataFormat.html
                ls.append({'id': int(line[0]), 'form': line[1], 'lemma': line[2],
                        'cpostag': line[3], 'head': line[6]})
                if i % 600000 == 0:
                    print i
                i += 1
    return ls


if __name__ == '__main__':
    print 'start'

    t = time()
    for i, item in enumerate(parse_dataset(sys.argv[1])):
        if i % 8000 == 0:
            print item

    print 'time: ', time() - t
