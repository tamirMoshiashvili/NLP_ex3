import numpy as np


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

    def make_vector_for(self, target_id):
        """ :return vector, which is a dictionary mapping feature to pmi-value(target, feature) """
        vector = dict()
        features = self.associator.get_features_for(target_id)
        for feature_id in features:
            pmi_result = self.calc_PMI(target_id, feature_id)
            if pmi_result > 0:
                vector[feature_id] = pmi_result
        return vector

    def build_all_vectors(self):
        for target_id in self.associator.get_all_common_targets_ids():
            self.vectors[target_id] = self.make_vector_for(target_id)

    def cosine(self, target_id1, target_id2):
        features1 = set(self.vectors[target_id1].keys())
        features2 = set(self.vectors[target_id2].keys())
        intersection = features1.intersection(features2)
        numerator = 0.0
        right_denominator = 0.0
        left_denominator = 0.0
        for feature in intersection:
            numerator += float(self.vectors[target_id1][feature]) * self.vectors[target_id2][feature]
            right_denominator += self.vectors[target_id1][feature] ** 2
            left_denominator += self.vectors[target_id2][feature] ** 2

        return numerator / np.sqrt(right_denominator * left_denominator)

    def test_pmi(self):
        p_target = 0.0
        p_feature = 0.0
        p_pair = 0.0
        for word_id in self.associator.pair_counts.keys():
            p_target += (self.associator.get_target_count(word_id) * 1.0) / self.associator.get_total_count()
            for feature_id in self.associator.pair_counts[word_id]:
                p_pair += (
                          self.associator.get_pair_count(word_id, feature_id) * 1.0) / self.associator.get_total_count()
        for feature_id in self.associator.features_count.keys():
            p_feature += (self.associator.get_feature_count(feature_id) * 1.0) / self.associator.get_total_count()

        if np.isclose([p_target], [1.0]) and np.isclose([p_feature], [1.0]) and np.isclose([p_pair], [1.0]):
            print ('PMI test Succeeded!')
        else:
            print ('PMI test failed!!!')
            print ('Ptarget:' + str(p_target))
            print ('Pfeature:' + str(p_feature))
            print ('Ppair:' + str(p_pair))
