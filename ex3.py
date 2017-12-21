from time import time

import numpy as np
import sys
from VectorBuilder import VectorBuilder
from SentenceAssociation import SentenceAssociation


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
    associator = SentenceAssociation(sys.argv[1])
    associator.test()
    vectorBuilder = VectorBuilder(associator)

    vectorBuilder.test_pmi()
    print "start to build all vectors"
    vectorBuilder.build_all_vectors()
    print ('vectors build done!')
    print (vectorBuilder.cosine(associator.get_word_id('dog'), associator.get_word_id('cat')))
    print (vectorBuilder.make_vector_for(associator.get_word_id('be')))
    print 'time: ', time() - t
