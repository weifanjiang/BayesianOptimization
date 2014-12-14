from __future__ import print_function
from __future__ import division

from sklearn.datasets import make_classification

from sklearn.cross_validation import cross_val_score

from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.svm import SVC

from bayes_opt import BayesianOptimization

# Load data set and target values
data, target = make_classification(n_samples=2500,
                                   n_features=45,
                                   n_informative=12,
                                   n_redundant=7)

def svccv(C, gamma):
    return cross_val_score(SVC(C=C, gamma=gamma, random_state=2),
                           data, target, 'f1', cv=5).mean()

def rfccv(n_estimators, min_samples_split, max_features):
    return cross_val_score(RFC(n_estimators=int(n_estimators),
                               min_samples_split=int(min_samples_split),
                               max_features=min(max_features, 0.999),
                               random_state=2),
                           data, target, 'f1', cv=5).mean()

if __name__ == "__main__":

    svcBO = BayesianOptimization(svccv, {'C': (0.001, 100), 'gamma': (0.0001, 0.1)})
    svcBO.explore({'C': [0.001, 0.01, 0.1], 'gamma': [0.001, 0.01, 0.1]})

    rfcBO = BayesianOptimization(rfccv, {'n_estimators': (10, 250),
                                         'min_samples_split': (2, 25),
                                         'max_features': (0.1, 0.999)})
    print('-'*50)
    svcBO.maximize()

    print('-'*50)
    rfcBO.maximize()

    print('-'*50)
    print('Final Results')
    print('SVC: ' % svcBO.res['max']['max_val'])
    print('RFC: ' % rfcBO.res['max']['max_val'])