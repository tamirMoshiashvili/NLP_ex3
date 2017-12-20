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
        self.word_counter = Counter() # count each word repeat
        self.counts = defaultdict(Counter) # count target word and context word pairs
        ###

        with open(input_file, 'r') as f:
            sentence = set()
            for line in f:
                splitted = line.split()
                if len(splitted) == 0:
                    for word in sentence:
                        for context in sentence.difference({word}):
                            self.counts[word][context] += 1
                    sentence.clear()
                else:
                    if splitted[4] in context_type:
                        lemma = splitted[2]
                        if lemma not in self.word_mapper:
                            self.word_mapper[lemma] = len(self.word_mapper)
                        self.word_counter[self.word_mapper[lemma]] += 1
                        sentence.add(self.word_mapper[lemma])
            # when the file don't end with empty line:
            if len(sentence) > 0:
                for word in sentence:
                    for context in sentence.difference({word}):
                        self.counts[word][context] += 1
                sentence.clear()

        print ('Counting is done.')
        print ('Start filter uncommon target words.')


        for word_id in self.word_counter.keys():
            if self.word_counter[word_id] < 100 and word_id in self.counts:
                del self.counts[word_id]
            else:
                self.total_words += self.word_counter[word_id]
        print ('Filtering is Done.')

    def get_target_count(self, target):
        if target in self.word_mapper:
            target = self.word_mapper[target]
            if target in self.word_counter[target]:
                return self.word_counter[target]
        return 0

    def get_pair_count(self, target, feature):
        if target in self.word_mapper and feature in self.word_mapper:
            target = self.word_mapper[target]
            feature = self.word_mapper[feature]
            if target in self.counts and feature in self.counts[target]:
                return self.counts[target][feature]
        return 0

    def get_total_count(self):
        return self.total_words

    def get_feature_count(self, feature):
        return self.get_target_count(feature)

    def get_features_for(self, target):
        if target in self.counts:
            return self.counts[target].most_common(30)
        else:
            return []
