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
# This will import code from the refactored project
import os.path
import sys
import pandas as pd
import numpy as np
from pilotis_io.pandas import PandasApi
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
pd.set_option("display.max_columns", 100)
python_dir = os.path.abspath('..')
sys.path.append(python_dir)

# %%
import bootcamp_2021_01
from bootcamp_2021_01.domain.feature_engineering import target_definition
from datetime import date
from bootcamp_2021_01.domain.feature_engineering.target_definition import FAILURE_FLAG, SUCCESS_FLAG, STATUS_CLOSED_VALUE, HOMEPAGE_URL_COLUMN, FIRST_FUNDING_AT_COLUMN, CITY_COLUMN, REGION_COLUMN, COUNTRY_CODE_COLUMN, TWO_YEARS_IN_DAYS, FUNDED_AT_COLUMN, STATUS_ACQUIRED_VALUE, LEFT_JOIN_TYPE, SUCCESSFUL_SERIES_A_COLUMN, COMPANY_NAME_COLUMN, FUNDING_ROUND_CODE_COLUMN, ROUND_CODE_SERIE_A_VALUE, ROUND_CODE_SERIE_SEED_VALUE, ROUND_CODE_SERIE_B_VALUE, STATUS_IPO_VALUE, STATUS_COLUMN, NAME_COLUMN, FUNDED_AT_AS_DATE_COLUMN, _IS_ACQUIRED_COL, _HAS_NEW_FUNDING_ROUND_COL, INVESTOR_CITY_COLUMN, INVESTOR_REGION_COLUMN, INVESTOR_NAME_COLUMN, INVESTOR_COUNTRY_CODE_COLUMN

# %%
WORK_DIR = '../../workdir'

MODEL_NAME = 'cat_boost'

# %% [markdown]
# # Load raw data for schema discovery

# %% [markdown]
# ## Load data

# %%
from pilotis_io.local.local_io_api import LocalIoApi
from pilotis_io.directory_structure import dataset_raw_dir_path

# %%
io_api = LocalIoApi(WORK_DIR)
pandas_api = PandasApi(io_api)

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
invest_files = io_api.list_files_in_dir(invest_path)
acq_files = io_api.list_files_in_dir(acq_path)
comp_files = io_api.list_files_in_dir(comp_path)

# %%
invest = pandas_api.load_pandas_dataset(invest_files, encoding='unicode_escape')
acq = pandas_api.load_pandas_dataset(acq_files, encoding='unicode_escape')
companies = pandas_api.load_pandas_dataset(comp_files, encoding='unicode_escape')


# %%
input_dataset_with_success_status = target_definition.add_series_a_success_status(
    invest, acq, companies, date(2015, 12, 1))

# %% [markdown]
# ## Model export

# %%
from bootcamp_2021_01.domain.persistence.use_cases.models_persistence import UseCasesModelPersistence
from bootcamp_2021_01.domain.use_cases import USE_CASE_NAME

models_persistence = UseCasesModelPersistence(io_api, USE_CASE_NAME, MODEL_NAME)

# %%
classifier = models_persistence.load_sklearn_model(run_id='run_notebook')

# %% [markdown]
# ## Model Dataviz

# %%
# shap_values = io_api.load_numpy_array("use_cases/bootcamp-2021-01/exports/shapley_values.npz")



# %%
import dash_table

from bootcamp_2021_01.domain.dash_components.banner import banner
from bootcamp_2021_01.domain.feature_engineering.feature_engineering import DAYS_SINCE_FIRST_FUNDING_COLUMN
from bootcamp_2021_01.domain.feature_engineering.target_definition import COMPANY_NAME_COLUMN, COUNTRY_CODE_COLUMN, \
    CITY_COLUMN
from bootcamp_2021_01.gui.ekilibr8_state import Ekilibr8

_NAME = "name"
_ID = "id"
_TYPE = "type"
_FORMAT = "format"

SCORE_COLUMN = 'score'
data_table = dash_table.DataTable(
    id='table',
    columns=[
        {_NAME: 'Company Name', _ID: COMPANY_NAME_COLUMN},
        {_NAME: 'Country', _ID: COUNTRY_CODE_COLUMN},
        {_NAME: 'City', _ID: CITY_COLUMN},
        {_NAME: 'Days since last funding', _ID: DAYS_SINCE_FIRST_FUNDING_COLUMN},
        {_NAME: 'Score', _ID: SCORE_COLUMN},
    ],
    data={},
    sort_action="native",
)

# %%
id_invest_input_dataset_with_success_status = input_dataset_with_success_status[input_dataset_with_success_status['investor_name'] == 'Idinvest Partners']

# %%
id_invest_input_dataset_with_success_status

# %%
time_since_first_funding = pd.to_datetime(id_invest_input_dataset_with_success_status[FUNDED_AT_AS_DATE_COLUMN]) \
                               - pd.to_datetime(id_invest_input_dataset_with_success_status[FIRST_FUNDING_AT_COLUMN])
number_of_days_since_first_funding = time_since_first_funding \
        .apply(lambda x: x.days) \
        .fillna(0) \
        .apply(int) \
        .apply(lambda x: x if x >= 0 else 0)

# %%
type(time_since_first_funding)

# %%
number_of_days_since_first_funding

# %%
VC_NAME = "Idinvest Partners"

# %%
from bootcamp_2021_01.domain.feature_engineering.feature_engineering import DAYS_SINCE_FIRST_FUNDING_COLUMN, \
    INVESTOR_EXPERIENCE_COLUMN, COUNTRY_CODE_COLUMN

# %%
model = models_persistence.load_sklearn_model(run_id='run_notebook')

# %%
vc_coutry_scope = id_invest_input_dataset_with_success_status[COUNTRY_CODE_COLUMN].unique()

# %%
vc_scope = input_dataset_with_success_status[input_dataset_with_success_status[COUNTRY_CODE_COLUMN].isin(vc_coutry_scope)]

# %%
from bootcamp_2021_01.domain.feature_engineering import feature_engineering

model_input, reality, company_name = feature_engineering.prepare_inputs_for_machine_learning(vc_scope, organizations)

# %%
only_this_vc = model_input[model_input[INVESTOR_EXPERIENCE_COLUMN] == VC_NAME]

model_input[INVESTOR_EXPERIENCE_COLUMN] = VC_NAME
model_input[INVESTOR_CITY_COLUMN] = only_this_vc[INVESTOR_CITY_COLUMN].iloc[0]
model_input[INVESTOR_REGION_COLUMN] = only_this_vc[INVESTOR_REGION_COLUMN].iloc[0]
model_input[INVESTOR_COUNTRY_CODE_COLUMN] = only_this_vc[INVESTOR_COUNTRY_CODE_COLUMN].iloc[0]

# %%

# %%
predictions = model.predict_proba(model_input)
success_proba = pd.DataFrame(predictions)[1]

scores = model_input \
    .reset_index() \
    .assign(score=success_proba,
            reality=reality.reset_index()[SUCCESSFUL_SERIES_A_COLUMN],
            company_name=company_name.reset_index()[COMPANY_NAME_COLUMN]) \
    .drop('index', axis=1)

# %%
scores.columns

# %%
graph_dataframe = id_invest_input_dataset_with_success_status.set_index("company_name", drop=False).join(scores.drop_duplicates("company_name").set_index("company_name")[['score']])


# %%
def define_color(score):
    if score >= 0.75:
        return 'green'
    elif score >= 0.5:
        return 'orange'
    else:
        return 'red'
        


# %%
graph_dataframe_with_color = graph_dataframe.assign(score_color=graph_dataframe['score'].apply(define_color))

# %%
import plotly.graph_objects as go

fig = go.Figure(data=[go.Table(header=dict(values=['Company Name', 'Country', 'City', 'Success', 'Scores']),
                 cells=dict(values=[
                     graph_dataframe['company_name'],
                                    graph_dataframe['country_code'],
                                    graph_dataframe['city'],
                                    graph_dataframe['successful_series_a'],
                                    graph_dataframe['score'].apply(lambda s: str(round(s * 100)) + "%")
                                   ],
                            fill=dict(color=[
                                'rgba(256,256,256,1)',
                                'rgba(256,256,256,1)',
                                'rgba(256,256,256,1)',
                                'rgba(256,256,256,1)',
                                graph_dataframe_with_color['score_color'],
                            ])
                           ))
                     ])
fig.show()

# %%

# %%
