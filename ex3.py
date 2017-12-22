import sys
from time import time

from Association import Association
from SentenceAssociationStrategy import SentenceAssociationStrategy
from VectorBuilder import VectorBuilder

TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def main_part1(filename):
    associator = Association(SentenceAssociationStrategy, filename)
    associator.test()
    vector_builder = VectorBuilder(associator)

    vector_builder.build_all_vectors()
    vector_builder.find_similarities(TARGET_WORDS, 'result_part1.txt')


if __name__ == '__main__':
    print 'start'

    t = time()

    mode = 1
    mains = {1: main_part1}
    mains[mode](sys.argv[1])

    print 'time: ', time() - t
