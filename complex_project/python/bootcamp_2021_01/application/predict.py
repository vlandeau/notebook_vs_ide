import argparse
import pickle
import numpy as np

from bootcamp_2021_01.application.train import read, merge_transaction_identity, PROJECT_DIR, MODEL_FOLDER, \
    MODEL_NAME, TRANSACTION_ID, extract_features

PREDICTION_PROBA_COL = "prediction_proba"
PREDICTION_CLASS_COL = "prediction_class"
PREDICTION_FOLDER = "/output/prediction/"
PREDICTION_FILENAME = "prediction_v0.csv"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", help="set threshold")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    trans, identity = read("test_transaction.csv", "test_identity.csv")
    all_features = merge_transaction_identity(trans, identity)
    features = extract_features(all_features)
    model = pickle.load(open(PROJECT_DIR + MODEL_FOLDER + MODEL_NAME, 'rb'))
    pred_proba = [p[1] for p in model.predict_proba(features)]
    all_features[PREDICTION_PROBA_COL] = pred_proba
    all_features[PREDICTION_CLASS_COL] = np.array(pred_proba) > float(args.threshold)
    all_features[[TRANSACTION_ID, PREDICTION_PROBA_COL, PREDICTION_CLASS_COL]].to_csv(
        PROJECT_DIR + PREDICTION_FOLDER + PREDICTION_FILENAME, index=False)
