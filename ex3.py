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
    return file_lines


# get a list where each item is a dictionary
def parse_dataset(filename):
    file_lines = read_dataset_file(filename)
    ls = []

    for line in file_lines:
        toks = line.split()
        if len(toks) != 0:  # skip empty lines
            # create dictionary out of the given line according to the format in https://depparse.uvt.nl/DataFormat.html
            format_dict = {'id': int(toks[0]), 'form': toks[1], 'lemma': toks[2],
                           'cpostag': toks[3], 'postag': toks[4], 'feats': toks[5],
                           'head': toks[6], 'deprel': toks[7], 'phead': toks[8], 'pdeprel': toks[9]}
            ls.append(format_dict)
    return ls


if __name__ == '__main__':
    print 'start'

    t = time()

    for i, item in enumerate(parse_dataset(sys.argv[1])):
        if i % 8000 == 0:
            print item

    print 'time: ', time() - t
