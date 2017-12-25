from collections import Counter, defaultdict
import SentenceNode as Node

HEAD = 0
WORD = 1
TAG = 2


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
            sentence = []
            for line in f:
                splitted = line.split()
                if len(splitted) == 0:  # reached end of sentence
                    self._feature_sentence(sentence, context_type, preposition)
                    sentence = []
                else:
                    if splitted[4] in all_context_type:  # TODO - check if it ok to cut here.
                        lemma = splitted[2]
                        sentence.append((int(splitted[6]), lemma, splitted[4]))
                    else:
                        sentence.append((-1,))  # to keep the token number

            # when the file don't end with empty line:
            if len(sentence) > 0:
                self._feature_sentence(sentence, context_type, preposition)
        print ('Counting is done.')

    def _get_lemma_id(self, lemma):
        if lemma not in self.word_mapper:
            # map the word to a number that represents its id
            self.word_mapper[lemma] = len(self.word_mapper)
        return self.word_mapper[lemma]

    def _feature_sentence(self, sentence, context_type, preposition):
        # tree = Node.buildSentenceTree(sentence)
        for tup in sentence:  # tup == (word, tag, head_id)
            if tup[HEAD] > 0 and tup[TAG] not in preposition:  # skip on root and for words that not context_type (==-1)
                word_id = self._get_lemma_id(WORD)

                father = sentence[tup[HEAD] - 1]

                prepositions = []
                try:
                    father[TAG]
                except:
                    print str(tup[WORD]) + "=>" + str(tup[HEAD])
                while father[TAG] in preposition:
                    prepositions.append(father[WORD])
                    father = sentence[father[HEAD] - 1]

                feature = ">" + father[WORD]

                for pre in preposition:
                    feature = feature + ">" + pre
                feature_id = self._get_lemma_id(feature)
                self.pair_counts[word_id][feature_id] += 1
                self.targets_count[word_id] += 1

                feature = "<" + tup[WORD]
                for pre in preposition:
                    feature = feature + "<" + pre
                word_id = self._get_lemma_id(father[WORD])
                self.targets_count[word_id] += 1
                feature_id = self._get_lemma_id(feature)
                self.pair_counts[word_id][feature_id] += 1