from collections import defaultdict, Counter
from time import time

THRESHOLD = 100
NUM_FEATURES_FOR_WORDS = 50


class SentenceAssociation:
    def __init__(self, input_file):
        # class fields:
        self.total_words = 0  # count of the common words
        self.word_mapper = dict()  # map word to number (to save memory...)
        self.targets_count = Counter()  # count each word repeat
        self.features_count = Counter()  # count each word repeat
        self.pair_counts = defaultdict(Counter)  # count target word and context word pairs
        self.recovery_filename = 'recovery_file'

        self._init_count_data_structures(input_file)
        self._filter()

    def _init_count_data_structures(self, input_file):
        # Content words are only verbs, nouns, adjectives, adverbs
        context_type = {  # tag from Penn Treebank II tag set
            'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG', 'WRB',  # verbs
            'MD', 'NN', 'NNS', 'NNP', 'NNPS',  # nouns
            'PRP', 'PRP$',  # pronoun
            'JJ', 'JJR', 'JJS',  # adjectives
            'RB', 'RBR', 'RBS', 'RP'}  # adverbs

        print ('Initializing count data-structure...')
        with open(input_file, 'r') as f:
            sentence = set()
            for line in f:
                splitted = line.split()
                if len(splitted) == 0:  # reached end of sentence
                    for word in sentence:
                        relevant_sentence = sentence.difference({word})
                        self.targets_count[word] += len(relevant_sentence)
                        for context in relevant_sentence:
                            self.pair_counts[word][context] += 1
                    sentence.clear()
                else:
                    if splitted[4] in context_type:  # check for valid context word (that has tag from the valid above)
                        lemma = splitted[2]
                        if lemma not in self.word_mapper:
                            # map the word to a number that represents its id
                            self.word_mapper[lemma] = len(self.word_mapper)
                        sentence.add(self.word_mapper[lemma])

            # when the file don't end with empty line:
            if len(sentence) > 0:
                for word in sentence:
                    relevant_sentence = sentence.difference({word})
                    self.targets_count[word] += len(relevant_sentence)
                    for context in relevant_sentence:
                        self.pair_counts[word][context] += 1
                sentence.clear()

        print ('Counting is done.')

    def _filter(self):
        print ('Start filter uncommon target words.')

        recovery_file = open(self.recovery_filename, 'w')

        for word_id in self.targets_count.keys():
            recovery_file.write(str(word_id))
            if self.targets_count[word_id] < THRESHOLD and word_id in self.pair_counts:
                for feature in self.pair_counts[word_id]:
                    recovery_file.write(' ' + str(feature))
                del self.pair_counts[word_id]

            else:
                # counting: #(*,att) after filtering
                for feature in self.pair_counts[word_id]:
                    recovery_file.write(' ' + str(feature))
                    self.features_count[feature] += self.pair_counts[word_id][feature]
                # counting #(*,*)
                self.total_words += self.targets_count[word_id]
            recovery_file.write('\n')

        recovery_file.close()
        print ('Filtering is Done.')

    def get_word_id(self, word):
        if word in self.word_mapper:
            return self.word_mapper[word]
        else:
            return False

    def get_all_common_targets_ids(self):
        """ all the words that passed the threshold """
        commons = self.pair_counts.keys()
        return commons

    def get_word_from_id(self, word_id):
        return self.word_mapper.keys()[self.word_mapper.values().index(word_id)]

    def get_target_count(self, target_id):
        """ #(word, *) """
        if target_id in self.targets_count:
            return self.targets_count[target_id]
        return 0

    def get_pair_count(self, target_id, feature_id):
        """ #(word, feature) """
        if target_id in self.pair_counts and feature_id in self.pair_counts[target_id]:
            return self.pair_counts[target_id][feature_id]
        return 0

    def get_total_count(self):
        """ #(*,*) """
        return self.total_words

    def get_feature_count(self, feature_id):
        """ #(*, feature) """
        if feature_id in self.features_count:
            return self.features_count[feature_id]
        return 0

    def get_features_for(self, target_id):
        if target_id in self.pair_counts:
            return map(lambda x: x[0], self.pair_counts[target_id].most_common(NUM_FEATURES_FOR_WORDS))
        else:
            return {}

    def cleanup(self):
        """ delete all the memory consumed by this object, besides the word-mapper """
        del self.total_words
        del self.targets_count
        del self.features_count
        del self.pair_counts

    def recover_file(self):
        t = time()
        att_to_word = dict()
        with open(self.recovery_filename, 'r') as f:
            for line in f:
                splitted = line.split()
                att_to_word[int(splitted[0])] = [int(item) for item in splitted[1:]]
            f.close()

        import os
        os.remove(self.recovery_filename)
        print 'time for recover-file:', time() - t
        return att_to_word

    def test(self):
        for word_id in self.pair_counts.keys():
            if len(list(self.pair_counts[word_id].elements())) != self.targets_count[word_id]:
                print ('---')
                print (self.get_word_from_id(word_id))
                print (self.pair_counts[word_id])
                print (len(list(self.pair_counts[word_id].elements())))
                print (self.targets_count[word_id])
