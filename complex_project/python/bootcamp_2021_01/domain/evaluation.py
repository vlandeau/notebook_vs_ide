import matplotlib.pyplot as plt
from sklearn import metrics
import seaborn as sns
import numpy as np
import pandas as pd


def plot_confusion_matrix(label, proba, threshold, output_path):
    pred = (np.array(proba) > threshold) * 1
    cm = metrics.confusion_matrix(label, pred)
    # Transform to df for easier plotting
    cm_df = pd.DataFrame(cm,
                         index=[0, 1],
                         columns=[0, 1])

    plt.figure(figsize=(5.5, 4))
    sns.heatmap(cm_df, annot=True)
    plt.title('Classifier threshold:{0:.2f} \nAccuracy:{1:.3f}, \nPrecision:{2:.3f}, \nRecall:{3:.3f}, \nF1:{4:.3f}'
              .format(threshold,
                      metrics.accuracy_score(label, pred),
                      metrics.precision_score(label, pred),
                      metrics.recall_score(label, pred),
                      metrics.f1_score(label, pred)))
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(output_path)


def plot_roc(label, proba, output_path):
    fpr, tpr, _ = metrics.roc_curve(label, proba)
    auc = metrics.roc_auc_score(label, proba)
    plt.plot(fpr, tpr, color='darkorange',
             lw=2, label='ROC curve (area = %0.2f)' % auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve')
    plt.legend(loc="lower right")
    plt.savefig(output_path)
