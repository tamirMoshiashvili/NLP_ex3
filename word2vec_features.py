import sys
from time import time

import pandas as pd

TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def load_words_and_vectors(filename):
    # find number of columns
    with open(filename, 'r') as f:
        num_cols = len(f.readline().split())

    # extract from file the words and their representation as vectors
    words_arr = pd.read_csv(filename, header=None, delimiter=' ', dtype=str, usecols=[0]).values
    print 'loaded words'
    vectors_matrix = pd.read_csv(filename, header=None, delimiter=' ', usecols=range(1, num_cols)).values
    print 'loaded matrix'

    return words_arr, vectors_matrix


def calc_sim(u, contexts_arr, vectors_matrix):
    """ u is a vector """
    dt = vectors_matrix.dot(u)  # calc dot-product
    sim_ids = dt.argsort()[-1:10:-1]
    return contexts_arr[sim_ids]  # return list of similar words (each is string)


def get_dict_word_to_vec():
    filename = sys.argv[1] + '.words'
    # load words and vectors and create dictionary for the words
    words, matrix = load_words_and_vectors(filename)
    w2i = {words[i][0]: i for i in range(len(words))}

    return {word: matrix[w2i[word]] for word in TARGET_WORDS}


def main():
    t = time()
    print 'start'

    # load words and vectors and create dictionary for the words
    target_word_to_vec = get_dict_word_to_vec()

    print 'time for loading words-file', time() - t
    t = time()

    # load contexts and vectors and create dictionary for the words
    filename = sys.argv[1] + '.contexts'
    contexts, matrix = load_words_and_vectors(filename)
    print 'time for contexts file:', time() - t
    t = time()

    result_file = open('word2vec2_features_' + sys.argv[1] + '.txt', 'w')
    for word in TARGET_WORDS:  # find similar words for each of target-words
        result_file.write(word + ':\n')
        word_as_vec = target_word_to_vec[word]

        # find similar words to word
        sim_words = [word[0] for word in calc_sim(word_as_vec, contexts, matrix)[:11]]

        for sim_word in sim_words:
            result_file.write('\t' + sim_word + '\n')
        result_file.write('\n')

    result_file.close()
    print 'time for finding similarities', time() - t


if __name__ == '__main__':
    # examples for command-line args:
    # bow5
    # deps
    main()
