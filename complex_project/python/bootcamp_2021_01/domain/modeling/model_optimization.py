from typing import List, Dict

from catboost import CatBoostClassifier
from pandas import DataFrame, Series
from sklearn.model_selection import RandomizedSearchCV


def tune_model(cat_features_indexes: List[int], x_train: DataFrame, y_train: Series) -> Dict:
    params_grid = {'depth': [4, 6, 8, 10],
                   'one_hot_max_size': [20, 100, 400, None],
                   'l2_leaf_reg': [2, 10, 30, 50],
                   'border_count': [16, 32, 64, 128]}
    tuning_classifier = CatBoostClassifier(cat_features=cat_features_indexes)
    search = RandomizedSearchCV(tuning_classifier, params_grid, cv=2, n_jobs=8, n_iter=2)
    search.fit(x_train, y_train)
    best_params = search.best_params_
    print(best_params)
    print(search.best_score_)
    return best_params
