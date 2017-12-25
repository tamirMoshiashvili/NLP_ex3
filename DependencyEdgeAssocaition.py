from collections import Counter, defaultdict
import SentenceNode as Node


class DependencyEdgeAssocaition:
    def __init__(self):
        # class fields:
        self.total_words = 0  # count of the common words
        self.word_mapper = dict()  # map word to number (to save memory...)
        self.targets_count = Counter()  # count each word repeat
        self.features_count = Counter()  # count each word repeat
        self.pair_counts = defaultdict(Counter)  # count target word and context word pairs

    def init_count_data_structures(self, input_file, context_type):
        preposition = {'IN'}
        all_context_type = preposition.union(context_type)
        print ('Initializing count data-structure...')
        with open(input_file, 'r') as f:
            sentence = set()
            for line in f:
                splitted = line.split()
                if len(splitted) == 0:  # reached end of sentence
                    tree = Node.buildSentenceTree(sentence)
                    sentence.clear()
                    # TODO - make the tree to features



                else:
                    if splitted[4] in all_context_type:  # TODO - check if it ok to cut here.
                        sentence.add((int(splitted[0]), splitted[2], splitted[4], int(splitted[6])))

            # when the file don't end with empty line:
            if len(sentence) > 0:
                for word in sentence:
                    relevant_sentence = sentence.difference({word})
                    self.targets_count[word] += len(relevant_sentence)
                    for context in relevant_sentence:
                        self.pair_counts[word][context] += 1
                sentence.clear()

        print ('Counting is done.')