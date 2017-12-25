from operator import itemgetter

class SentenceNode:
    def __init__(self, token_number, lemma, label):
        self.token_number = token_number
        self.lemma = lemma
        self.label = label
        self.sons = []

    def __del__(self):
        for son in self.sons:
            del son
        del self

    def add_son(self, node):
        self.sons.append(node)

# essume that sentence in a list of lists: [token_number, lemma, label, head_token_number]
def buildSentenceTree(sentence):
    sort_sentence = sorted(sentence, key=lambda tup: (tup[3], tup[0]))
    first = sort_sentence.pop(0)
    root = SentenceNode(first[0] , first[1],first[2])
    sons_of(root, first[0] ,sort_sentence)
    return root

def sons_of(node, level, sentence):
    if sentence: # when not empty
        sentence = filter_level(node, sentence, level)
        for son in node.sons:
            sons_of(son, son.token_number,sentence)

def filter_level (node, sentence, level):
    left = []
    for tp in  sentence:
        if tp[3] == level:
            node.sons.append(SentenceNode(tp[0], tp[1], tp[2]))
        else:
            left.append(tp)
    return left