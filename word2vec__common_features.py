from collections import defaultdict
from operator import itemgetter
from time import time
import numpy as np


WORD2VEC_METHOD = "deps"
CONTEXT_FILE = WORD2VEC_METHOD + '.contexts'
WORD_FILE = WORD2VEC_METHOD +'.words'
TARGETS_WORDS = {'car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar', 'piano'}

def get_targets_words_vector():
    r_file = open(WORD_FILE, "r")
    print ("start get target vectors")
    targets = dict()
    for line in r_file:
        s_line = line.split()
        word = s_line[0]
        # print "check word " + word
        if word in TARGETS_WORDS:
            targets[word] = np.array([float(val) for val in s_line[1:]])
    print "finish get target vectors"
    r_file.close()
    del r_file
    return targets

def peek_skip_gram(targets):
    r_file = open(CONTEXT_FILE,'r')
    commons = defaultdict(list)
    print "start to go over context file"
    for context_line in r_file:
        s_context_line = context_line.split()
        context = s_context_line[0]
        # print "check context: " + context
        vector = np.array([float(val) for val in s_context_line[1:]])
        for word in targets.keys():
            if word == context:
                continue
            mult = np.dot(vector, targets[word])
            if len(commons[word]) < 10:
                commons[word].append((context, mult))
                commons[word].sort(key=itemgetter(1))
            elif mult > commons[word][0][1]:
                commons[word].append((context, mult))
                commons[word].sort(key=itemgetter(1))
                commons[word] = commons[word][1:] # drop the smaller
    r_file.close()
    del r_file
    print "finish to go over the context file"
    return commons


if __name__ == '__main__':
    start = time()
    targets = get_targets_words_vector()

    commons = peek_skip_gram(targets)
    w_file = open("./features/features_word2vec_" + WORD2VEC_METHOD + ".txt", "w")
    for word in targets.keys():
        w_file.write(word + '=\n')
        for feature in commons[word]:
            w_file.write("\t" + feature[0] + "\n")
        w_file.write("\n")
    w_file.close()
    print "done "+ str(time() - start)




