import numpy as np

class VectorBuilder:
    def __init__(self, associator):
        self.associator = associator

    def calc_PMI(self, target, feature):
        numerator = (self.associator.get_pair_count(target, feature) * 1.0) / self.associator.get_total_count
        denominator = (self.associator.get_feature_count * 1.0) / self.associator.get_total_count
        denominator *= (self.associator.get_target_count * 1.0) / self.associator.get_total_count
        if denominator == 0:
            return 0
        else:
            return np.log(numerator/denominator)

    def get_vector_for(self, target):
        vector = dict()
        features = self.associator.get_features_for(target)
        for feature in features:
            pmi_result = self.calc_PMI(target, feature)
            if pmi_result > 0:
                vector[feature] = pmi_result
        return vector
