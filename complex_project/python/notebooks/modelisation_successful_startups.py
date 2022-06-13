# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import random
import warnings

import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
# %%
from pilotis_io.directory_structure import dataset_raw_dir_path
from pilotis_io.local import LocalPandasApi
from pilotis_io.local.local_io_api import LocalIoApi

from bootcamp_2021_01.domain.feature_engineering import feature_engineering
from bootcamp_2021_01.domain.modeling.model_optimization import tune_model
from bootcamp_2021_01.domain.persistence.use_cases.models_persistence import UseCasesModelPersistence
from bootcamp_2021_01.domain.use_cases import USE_CASE_NAME

pd.set_option("display.max_columns", 100)
warnings.simplefilter(action='ignore', category=FutureWarning)
# %%
WORK_DIR = '../../workdir'

MODEL_NAME = 'cat_boost'

# %% [markdown]
# # Load raw data for schema discovery

# %% [markdown]
# ## Load data

# %%
io_api = LocalIoApi(WORK_DIR)
pandas_api = LocalPandasApi(io_api)

# %%
dataset_version = '2015-12'

invest_name = 'notpeter_investments'
invest_path = dataset_raw_dir_path(invest_name, dataset_version)

acq_name = 'notpeter_acquisitions'
acq_path = dataset_raw_dir_path(acq_name, dataset_version)

comp_name = 'notpeter_companies'
comp_path = dataset_raw_dir_path(comp_name, dataset_version)

# %%
dataset_version_bachelorarbeit_clean = '2013-12-cleaned'
orga_name = 'bachelorarbeit_organizations'
orga_path = dataset_raw_dir_path(orga_name, dataset_version_bachelorarbeit_clean)

orga_files = io_api.list_files_in_dir(orga_path)
organizations = pandas_api.load_pandas_dataset(orga_files)

# %%
vc_holy_grail_people_dataset_version = 'vc_holy_grail_cleaned'

vc_holy_grail_people_name = 'vc_holy_grail_people'
vc_holy_grail_people_path = dataset_raw_dir_path(vc_holy_grail_people_name, vc_holy_grail_people_dataset_version)

# %%
invest_files = io_api.list_files_in_dir(invest_path)
acq_files = io_api.list_files_in_dir(acq_path)
comp_files = io_api.list_files_in_dir(comp_path)
vc_holy_grail_people_files = io_api.list_files_in_dir(vc_holy_grail_people_path)


# %%
invest = pandas_api.load_pandas_dataset(invest_files, encoding='unicode_escape')
acq = pandas_api.load_pandas_dataset(acq_files, encoding='unicode_escape')
companies = pandas_api.load_pandas_dataset(comp_files, encoding='unicode_escape')
vc_holy_grail_people = pandas_api.load_pandas_dataset(vc_holy_grail_people_files)


# %%
recent_invest = invest[invest.funded_at >= "2007-01-01"]

# %%
from datetime import date
from bootcamp_2021_01.domain.feature_engineering.target_definition import add_series_a_success_status

series_a_success_or_not_df = add_series_a_success_status(recent_invest, acq, companies, date(2015, 12, 3))

# %%
series_a_success_or_not_df.shape

# %%
series_a_success_or_not_df.head()

# %%
series_a_train = series_a_success_or_not_df[series_a_success_or_not_df.funded_at < "2013-01"]
series_a_test = series_a_success_or_not_df[series_a_success_or_not_df.funded_at >= "2013-01"]
series_a_train.shape, series_a_test.shape

# %%
x_train, y_train, _ = feature_engineering.prepare_inputs_for_machine_learning(series_a_train,
                                                                              organizations,
                                                                              vc_holy_grail_people)
x_test, y_test, _ = feature_engineering.prepare_inputs_for_machine_learning(series_a_test,
                                                                            organizations,
                                                                            vc_holy_grail_people)
len(y_train), len(y_test)


# %%
cat_features_indexes = list(np.where(x_train.dtypes == object)[0])
cat_features_indexes

# %%
#best_params = tune_model(cat_features_indexes, x_train, y_train)
best_params = {}

# %%
classifier = CatBoostClassifier(cat_features=cat_features_indexes, **best_params)
classifier.fit(x_train, y_train)

# %%
x_test

# %%
classifier.predict_proba(x_test)

# %% [markdown]
# ## Model export

# %%
models_persistence = UseCasesModelPersistence(io_api, USE_CASE_NAME, MODEL_NAME)

# %%
models_persistence.save_sklearn_model(classifier, run_id='run_notebook')

# %% [markdown]
# ## Model analysis

# %%
classifier.score(x_train, y_train), \
classifier.score(x_test, y_test)

# %%
test_predictions = classifier.predict_proba(x_test)[:, 1].reshape(-1, 1)
test_predictions.shape

# %%
from sklearn.metrics import auc, roc_curve

x_coord_roc, y_coord_roc, thresholds = roc_curve(y_test, test_predictions)
auc(x_coord_roc, y_coord_roc)

# %%
predictions_vs_reality = x_test.assign(predictions=test_predictions,
                                       reality=y_test)

# %%
predictions_vs_reality.head(30)

# %%
predictions_vs_reality.groupby("predictions")["reality"].value_counts()

# %%
import shap

explainer = shap.TreeExplainer(classifier)
shap_values = explainer.shap_values(x_test)

shap.summary_plot(shap_values, x_test)

# %%
shap.summary_plot(shap_values, x_test, plot_type="bar")

# %%
shap.dependence_plot("max_founded_organizations", shap_values, x_test,
                     interaction_index=None)


# %%
shap.dependence_plot("nb_days_since_first_funding", shap_values, x_test,
                     interaction_index=None)


# %%
shap.dependence_plot("number_of_days_since_first_january_70", shap_values, x_test,
                     interaction_index=None)


# %%
shap.dependence_plot("mean_news_articles", shap_values, x_test,
                     interaction_index=None)


# %%
shap.initjs()
sample_index = random.randint(0, len(x_test))

shap.force_plot(explainer.expected_value,
                shap_values[sample_index, :],
                x_test.iloc[sample_index, :])

# %%
shap.__version__

# %%
x_test.iloc[sample_index, :].values

# %%
