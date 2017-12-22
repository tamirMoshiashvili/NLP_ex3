from time import time

import numpy as np
import sys
from VectorBuilder import VectorBuilder
from SentenceAssociation import SentenceAssociation


def cosine(u, v):
    # u and v are np-arrays
    return np.dot(u, v) / (np.sqrt(np.dot(u, u)) * np.sqrt(np.dot(v, v)))


TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']

if __name__ == '__main__':
    print 'start'

    t = time()
    associator = SentenceAssociation(sys.argv[1])
    associator.test()
    vectorBuilder = VectorBuilder(associator)

    # vectorBuilder.test_pmi()
    print "start to build all vectors"
    vectorBuilder.build_all_vectors()
    print ('vectors build done!')
    # print (vectorBuilder.cosine(associator.get_word_id('dog'), associator.get_word_id('cat')))
    vectorBuilder.efficient_algorithm(TARGET_WORDS, 'result_part1.txt')
    print 'time: ', time() - t
