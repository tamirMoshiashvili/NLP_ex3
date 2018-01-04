import sys
from time import time

from Association import Association
from SentenceAssociationStrategy import SentenceAssociationStrategy
from VectorBuilder import VectorBuilder
from WindowAssociationStrategy import WindowAssociationStrategy
from DependencyEdgeAssocaition import DependencyEdgeAssocaition

TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def make_association_to_part(part_no, filename):
    if part_no == 1:
        association = Association(SentenceAssociationStrategy, filename)
    elif part_no == 2:
        association = Association(WindowAssociationStrategy, filename, arg=2)
    else:
        association = Association(DependencyEdgeAssocaition, filename)
    return association


def write_features_to_file(part, associator):
    f = open('./features/features_part' + str(part) + '.txt', 'w')
    for target_word in TARGET_WORDS:
        f.write(target_word + ':\n')
        for feat in associator.get_features_for(associator.get_word_id(target_word)):
            f.write('\t' + associator.get_word_from_id(feat) + '\n')
        f.write('\n')

    f.close()
    exit(0)

def write_first_order_to_file(part, vector):
    f = open('./features/first_order_for_part' + str(part) + '.txt', 'w')
    for target_word in TARGET_WORDS:
        f.write(target_word + ':\n')
        vec = sorted(vector.vectors[vector.associator.get_word_id(target_word)])
        if len(vec) > 20:
            vec = vec[-20:]
        else:
            print str(len(vec))+" = " +target_word
        for feat in vec:
            f.write('\t' + associator.get_word_from_id(feat) + '\n')
        f.write('\n')

    f.close()
    exit(0)


if __name__ == '__main__':
    print 'start'
    t = time()

    part = 3
    to_test = True

    associator = make_association_to_part(part, sys.argv[1])

    vector_builder = VectorBuilder(associator)
    if to_test:
        associator.test()
        vector_builder.test_pmi()
    vector_builder.build_all_vectors()
    write_first_order_to_file(part, vector_builder)
    vector_builder.find_similarities(TARGET_WORDS, 'result_part' + str(part) + ".txt")

    print 'time: ', time() - t
