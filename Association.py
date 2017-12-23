from time import time

THRESHOLD = 100
NUM_FEATURES_FOR_WORDS = 50


class Association:
    """ holds association-strategy and performs generic functions on it """

    def __init__(self, assoc_strategy, input_filename, arg=None):
        if arg is None:
            self.strategy = assoc_strategy()
        else:
            self.strategy = assoc_strategy(arg)

        # Content words are only verbs, nouns, adjectives, adverbs
        context_type = {  # tag from Penn Treebank II tag set
            'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG', 'WRB',  # verbs
            'MD', 'NN', 'NNS', 'NNP', 'NNPS',  # nouns
            'PRP', 'PRP$',  # pronoun
            'JJ', 'JJR', 'JJS',  # adjectives
            'RB', 'RBR', 'RBS', 'RP'}  # adverbs
        self.strategy.init_count_data_structures(input_filename, context_type)

        self.recovery_filename = 'recovery_file'
        self._filter()

    def _filter(self):
        print ('Start filter uncommon target words.')

        recovery_file = open(self.recovery_filename, 'w')

        strategy = self.strategy
        for word_id in strategy.targets_count.keys():
            recovery_file.write(str(word_id))
            if strategy.targets_count[word_id] < THRESHOLD and word_id in strategy.pair_counts:
                for feature in strategy.pair_counts[word_id]:
                    recovery_file.write(' ' + str(feature))
                del strategy.pair_counts[word_id]

            else:
                # counting: #(*,att) after filtering
                for feature in strategy.pair_counts[word_id]:
                    recovery_file.write(' ' + str(feature))
                    strategy.features_count[feature] += strategy.pair_counts[word_id][feature]
                # counting #(*,*)
                strategy.total_words += strategy.targets_count[word_id]
            recovery_file.write('\n')

        recovery_file.close()
        print ('Filtering is Done.')

    def get_word_id(self, word):
        strategy = self.strategy
        if word in strategy.word_mapper:
            return strategy.word_mapper[word]
        else:
            return False

    def get_all_common_targets_ids(self):
        """ all the words that passed the threshold """
        commons = self.strategy.pair_counts.keys()
        return commons

    def get_word_from_id(self, word_id):
        strategy = self.strategy
        return strategy.word_mapper.keys()[strategy.word_mapper.values().index(word_id)]

    def get_target_count(self, target_id):
        """ #(word, *) """
        strategy = self.strategy
        if target_id in strategy.targets_count:
            return strategy.targets_count[target_id]
        return 0

    def get_pair_count(self, target_id, feature_id):
        """ #(word, feature) """
        strategy = self.strategy
        if target_id in strategy.pair_counts and feature_id in strategy.pair_counts[target_id]:
            return strategy.pair_counts[target_id][feature_id]
        return 0

    def get_total_count(self):
        """ #(*,*) """
        return self.strategy.total_words

    def get_feature_count(self, feature_id):
        """ #(*, feature) """
        strategy = self.strategy
        if feature_id in strategy.features_count:
            return strategy.features_count[feature_id]
        return 0

    def get_features_for(self, target_id):
        strategy = self.strategy
        if target_id in strategy.pair_counts:
            return map(lambda x: x[0], strategy.pair_counts[target_id].most_common(NUM_FEATURES_FOR_WORDS))
        else:
            return {}

    def cleanup(self):
        """ delete all the memory consumed by this object, besides the word-mapper """
        strategy = self.strategy
        del strategy.total_words
        del strategy.targets_count
        del strategy.features_count
        del strategy.pair_counts

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
        strategy = self.strategy
        for word_id in strategy.pair_counts.keys():
            if len(list(strategy.pair_counts[word_id].elements())) != strategy.targets_count[word_id]:
                print ('---')
                print (self.get_word_from_id(word_id))
                print (strategy.pair_counts[word_id])
                print (len(list(strategy.pair_counts[word_id].elements())))
                print (strategy.targets_count[word_id])

    def get_structure_pair_counts(self):
        return self.strategy.pair_counts

    def get_structure_features_count(self):
        return self.strategy.features_count
