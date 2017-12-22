from collections import defaultdict, Counter


class SentenceAssociationStrategy:
    """ association-strategy that holds data-structures """

    def __init__(self):
        # class fields:
        self.total_words = 0  # count of the common words
        self.word_mapper = dict()  # map word to number (to save memory...)
        self.targets_count = Counter()  # count each word repeat
        self.features_count = Counter()  # count each word repeat
        self.pair_counts = defaultdict(Counter)  # count target word and context word pairs

    def init_count_data_structures(self, input_file, context_type):
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
