import numpy as np
from math import sqrt

class VectorBuilder:
    def __init__(self, associator):
        self.associator = associator
        self.vectors = {}

    def calc_PMI(self, target_id, feature_id):
        numerator = (self.associator.get_pair_count(target_id, feature_id) * 1.0) / self.associator.get_total_count()
        denominator = (self.associator.get_feature_count(feature_id) * 1.0) / self.associator.get_total_count()
        denominator *= (self.associator.get_target_count(target_id) * 1.0) / self.associator.get_total_count()
        if denominator == 0 or numerator == 0:
            return 0
        else:
            return np.log(numerator/denominator)

    def cosine(self, target_id1, target_id2):
        features1 = set(self.vectors[target_id1].keys())
        features2 = set(self.vectors[target_id2].keys())
        union = features1.intersection(features2)
        numerator = 0.0
        right_denominator = 0.0
        left_denominator = 0.0
        for feature in union:
            numerator += (self.vectors[target_id1][feature] * 1.0 * self.vectors[target_id2][feature])
            right_denominator += self.vectors[target_id1][feature]**2
            left_denominator += self.vectors[target_id2][feature]**2

        return numerator / sqrt(right_denominator * left_denominator)

    def make_vector_for(self, target_id):
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


    def test_pmi(self):
        Ptarget = 0.0
        Pfeature = 0.0
        Ppair = 0.0
        for word_id in self.associator.pair_counts.keys():
            Ptarget += (self.associator.get_target_count(word_id) * 1.0) / self.associator.get_total_count()
            for feature_id in self.associator.pair_counts[word_id]:
                Ppair += (self.associator.get_pair_count(word_id, feature_id) * 1.0) / self.associator.get_total_count()
        for feature_id in self.associator.features_count.keys():
            Pfeature += (self.associator.get_feature_count(feature_id) * 1.0) / self.associator.get_total_count()

        if np.isclose([Ptarget], [1.0]) and np.isclose([Pfeature], [1.0]) and np.isclose([Ppair],[1.0]):
            print ('PMI test Succeeded!')
        else:
            print ('PMI test failed!!!')
            print ('Ptarget:' + str(Ptarget))
            print ('Pfeature:' + str(Pfeature))
            print ('Ppair:' + str(Ppair))
