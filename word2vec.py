import sys
from time import time
import pandas as pd
import numpy as np

TARGET_WORDS = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano']


def load_words_and_vectors():
    filename = sys.argv[1]

    # find number of columns
    with open(filename, 'r') as f:
        num_cols = len(f.readline().split())

    # extract from file the words and their representation as vectors
    words_arr = pd.read_csv(filename, header=None, delimiter=' ', dtype=str, usecols=[0]).values
    print 'loaded words'
    vectors_matrix = pd.read_csv(filename, header=None, delimiter=' ', usecols=range(1, num_cols)).values
    print 'loaded matrix'

    return words_arr, vectors_matrix


def calc_sim(u, words_arr, vectors_matrix):
    """ u is a vector """
    dt = vectors_matrix.dot(u)  # calc dot-product
    sim_ids = dt.argsort()[-1:10:-1]  # find most similar ids of words
    return words_arr[sim_ids]  # return list of similar words (each is string)


def main():
    t = time()
    print 'start'

    # load words and vectors and create dictionary for the words
    words, matrix = load_words_and_vectors()
    w2i = {words[i][0]: i for i in range(len(words))}

    print 'time for loading file', time() - t
    t = time()

    result_file = open('features/word2vec_features_' + sys.argv[1].split('.')[0] + '.txt', 'w')
    for word in TARGET_WORDS:  # find similar words for each of target-words
        result_file.write(word + ':\n')
        word_as_vec = matrix[w2i[word]]

        # find similar words to word, taking [:21] items include the word and [1:] skips it
        sim_words = [word[0] for word in calc_sim(word_as_vec, words, matrix)[1:11]]

        for sim_word in sim_words:
            result_file.write('\t' + sim_word + '\n')
        result_file.write('\n')

    result_file.close()
    print 'time for finding similarities', time() - t


def calc_sim2(word_vec):
    d = dict()

    with open(sys.argv[1], 'r') as f:
        for line in f:
            context_vec = np.ndarray(line[1:])
            d[line[0]] = context_vec.dot(word_vec)

    return d


def main2():
    filename = sys.argv[1]
    features_file = open('features/word2vec_features_' + filename.split('.')[0] + '.txt', 'w')
    context_words = pd.read_csv(filename, header=None, delimiter=' ', dtype=str, usecols=[0]).values
    print 'loaded words'

    for target_word in TARGET_WORDS:
        features_file.write(target_word + ':\n')
        for feat in calc_sim2(target_word):  # todo change to word-vector
            features_file.write('\t' + feat + '\n')

    features_file.close()


if __name__ == '__main__':
    main()
