from collections import Counter, defaultdict


class WindowAssociationStrategy:
    def __init__(self, window_size):
        # class fields:
        self.total_words = 0  # count of the common words
        self.word_mapper = dict()  # map word to number (to save memory...)
        self.targets_count = Counter()  # count each word repeat
        self.features_count = Counter()  # count each word repeat
        self.pair_counts = defaultdict(Counter)  # count target word and context word pairs
        self.window_size = window_size

    def init_count_data_structures(self, input_file, context_type):
        print ('Initializing count data-structure...')

        window_size = self.window_size
        len_context_of_window = 2 * window_size
        with open(input_file, 'r') as f:
            sentence = []
            for line in f:
                splited = line.split()
                if len(splited) == 0:  # reached end of sentence
                    for i in range(window_size, len(sentence) - window_size):
                        word = sentence[i]
                        self.targets_count[word] += len_context_of_window
                        relevant_indices = range(i - window_size, i + window_size + 1)
                        relevant_indices.remove(i)
                        for context_index in relevant_indices:
                            self.pair_counts[word][sentence[context_index]] += 1

                    del sentence
                    sentence = []
                else:
                    if splited[4] in context_type:
                        lemma = splited[2]
                        if lemma not in self.word_mapper:
                            # map the word to a number that represents its id
                            self.word_mapper[lemma] = len(self.word_mapper)
                        sentence.append(self.word_mapper[lemma])

            # when the file don't end with empty line:
            if len(sentence) > 0:
                for i in range(window_size, len(sentence) - window_size):
                    word = sentence[i]
                    self.targets_count[word] += len_context_of_window
                    relevant_indices = range(i - window_size, i + window_size + 1)
                    relevant_indices.remove(i)
                    for context_index in relevant_indices:
                        self.pair_counts[word][sentence[context_index]] += 1

                del sentence

        print ('Counting is done.')
