from time import time

import numpy as np
import sys
from VectorBuilder import VectorBuilder
from SentenceAssociation import SentenceAssociation


def cosine(u, v):
    # u and v are np-arrays
    return np.dot(u, v) / (np.sqrt(np.dot(u, u)) * np.sqrt(np.dot(v, v)))


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
