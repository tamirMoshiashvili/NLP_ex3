from collections import defaultdict, Counter
class SentenceAssociation:
    def __init__(self, input_file):
        # Content words are only verbs, nouns, adjectives, adverbs
        context_type = { # tag from Penn Treebank II tag set
                        'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG', 'WRB', # verbs
                        'MD', 'NN', 'NNS', 'NNP', 'NNPS',                # nouns
                        'PRP', 'PRP$',                                  # pronoun
                        'JJ', 'JJR', 'JJS',                             # adjectives
                        'RB', 'RBR', 'RBS', 'RP'}                       # adverbs
        print ('Initializing count data-structure...')

        # class fields:
        self.total_words = 0  # count of the common words
        self.word_mapper = dict() # map word to number (to save memory...)
        self.targets_count = Counter() # count each word repeat
        self.features_count = Counter() # count each word repeat
        self.pair_counts = defaultdict(Counter) # count target word and context word pairs
        ###

        with open(input_file, 'r') as f:
            sentence = set()
            for line in f:
                splitted = line.split()
                if len(splitted) == 0:
                    for word in sentence:
                        for context in sentence.difference({word}):
                            self.pair_counts[word][context] += 1
                            self.targets_count[word] += 1
                    sentence.clear()
                else:
                    if splitted[4] in context_type:
                        lemma = splitted[2]
                        if lemma not in self.word_mapper:
                            self.word_mapper[lemma] = len(self.word_mapper)
                        sentence.add(self.word_mapper[lemma])

            # when the file don't end with empty line:
            if len(sentence) > 0:
                for word in sentence:
                    for context in sentence.difference({word}):
                        self.pair_counts[word][context] += 1
                        self.targets_count[word] += 1
                sentence.clear()

        print ('Counting is done.')
        print ('Start filter uncommon target words.')

        for word_id in self.targets_count.keys():
            if self.targets_count[word_id] < 100 and word_id in self.pair_counts:
                del self.pair_counts[word_id]

            else:
                # counting: #(*,att) after filtering
                for feature in self.pair_counts[word_id]:
                    self.features_count[feature] += self.pair_counts[word_id][feature]
                # counting #(*,*)
                self.total_words += self.targets_count[word_id]

        print ('Filtering is Done.')

        # TODO - delete this:
        common = self.targets_count.most_common(1)
        common = common[0][0]
        common_word = self.word_mapper.keys()[self.word_mapper.values().index(common)]
        print ('common word is ' + str(common_word))

    def get_word_id(self, word):
        if word in self.word_mapper:
            return self.word_mapper[word]
        else:
            return False

    def get_all_common_targets_ids(self):
        commons = self.pair_counts.keys()
        return commons

    def get_word_from_id(self, id):
        return self.word_mapper.keys()[self.word_mapper.values().index(id)]

    def get_target_count(self, target_id):
        if target_id in self.targets_count:
            return self.targets_count[target_id]
        return 0

    def get_pair_count(self, target_id, feature_id):
        if target_id in self.pair_counts and feature_id in self.pair_counts[target_id]:
            return self.pair_counts[target_id][feature_id]
        return 0

    def get_total_count(self):
        return self.total_words

    def get_feature_count(self, feature_id):
        if feature_id in self.features_count:
            return self.features_count[feature_id]
        return 0

    def get_features_for(self, target_id):
        if target_id in self.pair_counts:
            return map(lambda x: x[0], self.pair_counts[target_id].most_common(30))
        else:
            return {}

    def test(self):
        for word_id in self.pair_counts.keys():
            if len(list (self.pair_counts[word_id].elements())) != self.targets_count[word_id]:
                print ('---')
                print (self.get_word_from_id(word_id))
                print (self.pair_counts[word_id])
                print (len(list (self.pair_counts[word_id].elements())))
                print (self.targets_count[word_id])




