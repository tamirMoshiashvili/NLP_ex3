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


if __name__ == '__main__':
    print 'start'
    t = time()

    part = 3
    to_test = False

    associator = make_association_to_part(part, sys.argv[1])
    f = open('./features/features_part' + str(part) + '.txt', 'w')
    for target_word in TARGET_WORDS:
        f.write(target_word + ':\n')
        for feat in associator.get_features_for(associator.get_word_id(target_word)):
            f.write('\t' + associator.get_word_from_id(feat) + '\n')
        f.write('\n')

    f.close()

    vector_builder = VectorBuilder(associator)
    if to_test:
        associator.test()
        vector_builder.test_pmi()
    vector_builder.build_all_vectors()
    vector_builder.find_similarities(TARGET_WORDS, 'result_part' + str(part) + ".txt")

    print 'time: ', time() - t
