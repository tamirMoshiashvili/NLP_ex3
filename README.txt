VectorBuilder.py should be good for all association type in this exercise,
for this  we need that all other association types, will have this API:

    def get_target_count(self, target_id):     e.g - #(u,*)

    def get_pair_count(self, target_id, feature_id):  e.g - #(u,att)

    def get_total_count(self):  e.g - #(*,*)

    def get_word_id(self, word): e.g getter for word_id

    def get_feature_count(self, feature_id):   e.g - #(*,att)

    def get_features_for(self, target):     e.g - list of all the features of u (limited to 30 common ones)

what next?
    cosine method between two vectors from VectorBuilder.get_vector()
    association type for 2 and 3
