from collections import Counter
from time import time

import numpy as np

TOP_N_SIMILAR = 20


class VectorBuilder:
    def __init__(self, associator):
        self.associator = associator
        self.vectors = {}

    def calc_PMI(self, target_id, feature_id):
        # p(a, b) where a is a word and b is a feature
        numerator = float(self.associator.get_pair_count(target_id, feature_id)) / self.associator.get_total_count()

        # p(a) * p(b)
        denominator = float(self.associator.get_feature_count(feature_id)) / self.associator.get_total_count()
        denominator *= float(self.associator.get_target_count(target_id)) / self.associator.get_total_count()

        if denominator == 0 or numerator == 0:
            return 0
        else:
            return np.log(numerator / denominator)

    def make_vector_for(self, target_id , recovery_file):
        """ :return vector, which is a dictionary mapping feature to pmi-value(target, feature) """
        vector = dict()
        features = self.associator.get_features_for(target_id)
        for feature_id in features:
            recovery_file.write(str(feature_id)+" "+ str(target_id) +"\n")
            pmi_result = self.calc_PMI(target_id, feature_id)
            if pmi_result > 0:
                vector[feature_id] = pmi_result
        return vector

    def build_all_vectors(self):
        print "start to build all vectors"
        recovery_file = open(self.associator.recovery_filename, 'w')
        for target_id in self.associator.get_all_common_targets_ids():
            self.vectors[target_id] = self.make_vector_for(target_id, recovery_file)
        recovery_file.close()
        self.associator.cleanup()
        print ('vectors build done!')

    def cosine(self, target_id1, target_id2):
        features1 = set(self.vectors[target_id1].keys())
        features2 = set(self.vectors[target_id2].keys())
        intersection = features1.intersection(features2)
        numerator = 0.0
        right_denominator, left_denominator = 0.0, 0.0
        for feature in intersection:
            numerator += float(self.vectors[target_id1][feature]) * self.vectors[target_id2][feature]
            right_denominator += self.vectors[target_id1][feature] ** 2
            left_denominator += self.vectors[target_id2][feature] ** 2

        return numerator / np.sqrt(right_denominator * left_denominator)

    def test_pmi(self):
        p_target = 0.0
        p_feature = 0.0
        p_pair = 0.0
        for word_id in self.associator.get_structure_pair_counts().keys():
            p_target += float(self.associator.get_target_count(word_id)) / self.associator.get_total_count()
            for feature_id in self.associator.get_structure_pair_counts()[word_id]:
                p_pair += float(self.associator.get_pair_count(word_id, feature_id)) / self.associator.get_total_count()
        for feature_id in self.associator.get_structure_features_count().keys():
            p_feature += float(self.associator.get_feature_count(feature_id)) / self.associator.get_total_count()

        if np.isclose([p_target], [1.0]) and np.isclose([p_feature], [1.0]) and np.isclose([p_pair], [1.0]):
            print ('PMI test Succeeded!')
        else:
            print ('PMI test failed!!!')
            print ('Ptarget:' + str(p_target))
            print ('Pfeature:' + str(p_feature))
            print ('Ppair:' + str(p_pair))

    def calc_sim(self, word):
        word_id = self.associator.get_word_id(word)
        sim_vec = Counter()
        for v_id in self.vectors:
            sim_vec[v_id] = self.cosine(word_id, v_id)
        sim_vec = sim_vec.most_common(20)
        as_words = [(self.associator.get_word_from_id(vec_id[0]), vec_id[1]) for vec_id in sim_vec]
        for item in as_words:
            print item

    def find_similarities(self, words, result_filename):
        """ find top-n similar-words to the given words, writes the results in the file specified """

        print 'applying efficient algorithm'
        t = time()

        f = open(result_filename, 'w')
        att_to_words = self.associator.recover_file()

        for u in words:
            f.write(u + ':\n')
            u = self.associator.get_word_id(u)
            dt = Counter()  # word-v to score, actually similarity-of-u-and-v

            u_vec = self.vectors[u]
            for att in u_vec:
                one = u_vec[att]
                for v in att_to_words[att]:
                    if v not in self.vectors or u == v:
                        continue
                    two = 0
                    if att in self.vectors[v]:
                        two = self.vectors[v][att]
                    dt[v] += one * two

            top_n = [(self.associator.get_word_from_id(word[0]), word[1]) for word in dt.most_common(TOP_N_SIMILAR)]
            for item in top_n:
                f.write('\t' + item[0] + '\n')
            f.write('\n')

        f.close()
        print 'time to find words:', time() - t  # should take about 60-sec
