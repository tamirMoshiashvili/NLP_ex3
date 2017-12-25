import sys
from time import time

import numpy as np

TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def load_words_and_vectors():
    filename = sys.argv[1]

    # find number of columns
    with open(filename, 'r') as f:
        cols = len(f.readline().split())

    # extract from file the words and their representation as vectors
    vectors_matrix = np.loadtxt(filename, usecols=range(1, cols))
    print 'loaded words'
    words_arr = np.loadtxt(filename, usecols=0, dtype=str)

    return words_arr, vectors_matrix


def calc_sim(u, words_arr, vectors_matrix):
    """ u is a vector """
    dt = vectors_matrix.dot(u)  # calc dot-product
    sim_ids = dt.argsort()[-1:10:-1]  # find most similar ids of words
    return words_arr[sim_ids]  # return list of similar words (each is string)


if __name__ == '__main__':
    t = time()
    print 'start'

    words, matrix = load_words_and_vectors()
    w2i = {w: i for i, w in enumerate(words)}

    print 'time for loading file', time() - t
    t = time()

    result_file = open('results/word2vec_' + sys.argv[1].split('.')[0] + '.txt', 'w')
    for word in TARGET_WORDS:  # find similar words for each of target-words
        result_file.write(word + ':\n')
        u_vec = matrix[w2i[word]]
        for sim_word in calc_sim(word, words, matrix):
            result_file.write('\t' + sim_word + '\n')
        result_file.write('\n')

    result_file.close()
    print 'time for finding similarities', time() - t
