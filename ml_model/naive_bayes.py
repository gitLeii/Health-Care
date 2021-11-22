import numpy as np 
import pandas as pd 

class  NaiveBayes:
    def __init__(self): 
        self.features = list
        self.likelihoods = {}
        self.class_priors = {}
        self.pred_priors = {}

        self.X_train = np.array
        self.y_train = np.array
        self.train_size = int
        self.num_feats = int

    def fit(self, X, y):

        self.features = list(X.columns)
        self.X_train = X
        self.y_train = y
        self.train_size = X.shape[0]
        self.num_feats = X.shape[1]

        for feature in self.features:
            self.likelihoods[feature] = {}
            self.pred_priors[feature] = {}

            for feat_val in np.unique(self.X_train[feature]):
                self.pred_priors[feature].update({feat_val: 0})

                for outcome in np.unique(self.y_train):
                    outcome_count = sum(self.y_train == outcome) 
                    self.likelihoods[feature].update({str(feat_val)+'_'+str(outcome):1/(outcome_count + len(self.features))})
                    self.class_priors.update({outcome: 0})

        self._calc_class_prior()
        self._calc_likelihoods()
        self._calc_predictor_prior()


    def _calc_class_prior(self): 
        """ P(c) - Prior Class Probability """ 
        for outcome in np.unique(self.y_train):
            outcome_count = sum(self.y_train == outcome)
            self.class_priors[outcome] = outcome_count / self.train_size


    def _calc_likelihoods(self): 
        """ P(x|c) - Likelihood """ 
        for feature in self.features:

            for outcome in np.unique(self.y_train):
                outcome_count = sum(self.y_train == outcome)
                feat_likelihood = self.X_train[feature][self.y_train[self.y_train == outcome].index.values.tolist()].value_counts().to_dict()

                for feat_val, count in feat_likelihood.items():
                    self.likelihoods[feature][str(feat_val) + '_' + str(outcome)] = (count + 1)/(outcome_count + len(self.features) * 1)


    def _calc_predictor_prior(self): 
        """ P(x) - Evidence """ 
        for feature in self.features:
            feat_vals = self.X_train[feature].value_counts().to_dict()

            for feat_val, count in feat_vals.items():
                self.pred_priors[feature][feat_val] = count/self.train_size


    def predict(self, X): 
        """ Calculates Posterior probability P(c|x) """
        results = []
        X = np.array(X)

        for query in X:
            probs_outcome = {}
            for outcome in np.unique(self.y_train):
                prior = self.class_priors[outcome]
                likelihood = 1
                evidence = 1

                for feat, feat_val in zip(self.features, query):
                    if feat_val != 0:
                        likelihood *= self.likelihoods[feat][str(feat_val) + '_' + str(outcome)]
                    evidence *= self.pred_priors[feat][feat_val]

                posterior = (likelihood * prior) / (evidence) 
                probs_outcome[outcome] = posterior

            result = max(probs_outcome, key = lambda x: probs_outcome[x])
            results.append(result)
        total_sum = 0
        for i,j in probs_outcome.items():
            total_sum += j 
        percentage_outcome = {}
        for i,j in probs_outcome.items():
            percentage_outcome[i] = round((j/total_sum)*100, 2)
        sorted_percentage_outcome = sorted(percentage_outcome.items(), key=lambda x:x[1], reverse=True)
#         print(sorted_percentage_outcome[:10]) 
        return sorted_percentage_outcome[:6]
 