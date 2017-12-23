import sys
from time import time

from Association import Association
from SentenceAssociationStrategy import SentenceAssociationStrategy
from VectorBuilder import VectorBuilder
from WindowAssociationStrategy import WindowAssociationStrategy

TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def main_part1(filename):
    associator = Association(SentenceAssociationStrategy, filename)
    associator.test()
    vector_builder = VectorBuilder(associator)

    vector_builder.build_all_vectors()
    vector_builder.find_similarities(TARGET_WORDS, 'result_part1.txt')


def main_part2(filename):
    associator = Association(WindowAssociationStrategy, filename, arg=2)
    associator.test()
    vector_builder = VectorBuilder(associator)

    vector_builder.build_all_vectors()
    vector_builder.find_similarities(TARGET_WORDS, 'result_part2.txt')


if __name__ == '__main__':
    print 'start'

    t = time()

    mode = 2
    mains = {1: main_part1, 2: main_part2}
    mains[mode](sys.argv[1])

    print 'time: ', time() - t
