import pickle

import pandas as pd
import os

from bootcamp_2021_01.domain.evaluation import plot_roc, plot_confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier

PROJECT_DIR_ENV_VAR_NAME = "PROJECT_DIR"

DEFAULT_THRESHOLD = 0.5

DATA_FOLDER_PATH = "/data_sample/"
EVAL_METRIC_PATH = "/output/eval_metric/"
MODEL_FOLDER = "/output/model/"
PROJECT_DIR = os.environ.get(PROJECT_DIR_ENV_VAR_NAME, "/Users/robinlespes/Desktop/ekinox/code/ieee-fraud-detection")

MODEL_NAME = "gb_v0.pickle"

TRANSACTION_DT = "TransactionDT"
TRANSACTION_ID = "TransactionID"
IS_FRAUD = "isFraud"

TRAIN_TEST_THRESHOLD = 15000


def read(transaction_filename, id_filename):
    trans = pd.read_csv(PROJECT_DIR + DATA_FOLDER_PATH + transaction_filename, nrows=20000)
    identity = pd.read_csv(PROJECT_DIR + DATA_FOLDER_PATH + id_filename)
    return trans, identity


def merge_transaction_identity(trans, id):
    all_features = trans.merge(id, on=TRANSACTION_ID, how="left")
    all_features.sort_values(TRANSACTION_DT, inplace=True)
    return all_features


def extract_target(df):
    X = df.drop(IS_FRAUD, axis=1).sort_index(axis=1)
    y = df[IS_FRAUD]
    return X, y


def extract_features(X):
    return X[[col for col in X.columns if col.startswith("C")]]


def train_classifier(X_train_v0, y_train, output_path):
    gb = GradientBoostingClassifier()
    gb.fit(X_train_v0, y_train)
    pickle.dump(gb, open(output_path, 'wb'))
    return gb


def eval_classifier(label, proba):
    plot_roc(label, proba, PROJECT_DIR + EVAL_METRIC_PATH + "roc.png")
    plot_confusion_matrix(label, proba, DEFAULT_THRESHOLD, PROJECT_DIR + EVAL_METRIC_PATH + "confusion_matrix.png")


if __name__ == '__main__':
    trans_train, id_train = read("train_transaction.csv", "train_identity.csv")
    df = merge_transaction_identity(trans_train, id_train)
    X_train, y_train = extract_target(df[:TRAIN_TEST_THRESHOLD])
    X_test, y_test = extract_target(df[TRAIN_TEST_THRESHOLD:])
    X_train_feature_selected = extract_features(X_train)
    X_test_feature_selected = extract_features(X_test)
    model = train_classifier(X_train_feature_selected, y_train, PROJECT_DIR + MODEL_FOLDER + MODEL_NAME)
    pred_proba_test = [p[1] for p in model.predict_proba(X_test_feature_selected)]
    pd.Series(pred_proba_test).to_csv(PROJECT_DIR + EVAL_METRIC_PATH + "proba_pred.csv", index=False)
    y_test.to_csv(PROJECT_DIR + EVAL_METRIC_PATH + "label.csv", index=False)
    eval_classifier(y_test, pred_proba_test)
