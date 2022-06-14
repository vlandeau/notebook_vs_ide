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

# %% [markdown]
# # VC Validation

# %% [markdown]
# Objectifs du notebook
#
# - Obtenir une différence de taux de réussite d'investissement pour un VC donné
# - Exporter les prédictions pour un VC donné pour les charger dans la webapp

# %% [markdown]
# ## Tech

# %%
import os.path
import sys
import pandas as pd

pd.set_option("display.max_columns", 100)
python_dir = os.path.abspath('..')
sys.path.append(python_dir)

# %%
from ekinox_ds.local.local_io_api import LocalIoApi
from ekinox_ds.directory_structure import dataset_raw_dir_path

WORKDIR = '../../workdir'
io_api = LocalIoApi(WORKDIR)

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
organizations = io_api.load_pandas_dataset(orga_files)

# %%
vc_holy_grail_people_dataset_version = 'vc_holy_grail_cleaned'

vc_holy_grail_people_name = 'vc_holy_grail_people'
vc_holy_grail_people_path = dataset_raw_dir_path(vc_holy_grail_people_name, vc_holy_grail_people_dataset_version)

# %%
invest_files = io_api.list_files_in_dir(invest_path)
acq_files = io_api.list_files_in_dir(acq_path)
comp_files = io_api.list_files_in_dir(comp_path)
vc_holy_grail_people_files =  io_api.list_files_in_dir(vc_holy_grail_people_path)

# %%
invest = io_api.load_pandas_dataset(invest_files, encoding='unicode_escape')
acq = io_api.load_pandas_dataset(acq_files, encoding='unicode_escape')
companies = io_api.load_pandas_dataset(comp_files, encoding='unicode_escape')
vc_holy_grail_people = io_api.load_pandas_dataset(vc_holy_grail_people_files)

# %%
from datetime import date
from bootcamp_2021_01.domain.feature_engineering.target_definition import add_series_a_success_status

series_a_success_or_not_df = add_series_a_success_status(invest, acq, companies, date(2015, 12, 1))

# %% [markdown]
# ## Input

# %%
VC_NAME = 'Idinvest Partners'

# %% [markdown]
# ## Success rate comparison

# %%
from bootcamp_2021_01.domain.feature_engineering.target_definition import INVESTOR_NAME_COLUMN, \
    SUCCESSFUL_SERIES_A_COLUMN, COUNTRY_CODE_COLUMN, INVESTOR_CITY_COLUMN, CITY_COLUMN, \
    INVESTOR_COUNTRY_CODE_COLUMN, INVESTOR_REGION_COLUMN, COMPANY_NAME_COLUMN, REGION_COLUMN

from bootcamp_2021_01.domain.feature_engineering.feature_engineering import DAYS_SINCE_FIRST_FUNDING_COLUMN, \
    INVESTOR_EXPERIENCE_COLUMN

from bootcamp_2021_01.gui.ekilibr8_state import SCORE_COLUMN

# %% [markdown]
# ### Real success rate

# %%
invest_by_vc = series_a_success_or_not_df[series_a_success_or_not_df[INVESTOR_NAME_COLUMN] == VC_NAME]

# %%
invest_by_vc

# %%
invest_by_vc[['company_name', 'successful_series_a']]

# %%
invest_by_vc_count = len(invest_by_vc)

# %%
success_by_vc = invest_by_vc[invest_by_vc[SUCCESSFUL_SERIES_A_COLUMN] == 1]

# %%
success_count_by_vc = len(success_by_vc)

# %%
real_success_rate = success_count_by_vc / invest_by_vc_count

# %%
print(f'Invest count : {invest_by_vc_count}')
print(f'Success count : {success_count_by_vc}')
print(f'Success rate : {(real_success_rate*100):.2f} %')

# %% [markdown]
# ### Success rate using the model

# %%
vc_coutry_scope = invest_by_vc[COUNTRY_CODE_COLUMN].unique()

# %%
vc_scope = series_a_success_or_not_df[series_a_success_or_not_df[COUNTRY_CODE_COLUMN].isin(vc_coutry_scope)]

# %%
from bootcamp_2021_01.domain.feature_engineering import feature_engineering

model_input, reality, company_name = feature_engineering.prepare_inputs_for_machine_learning(vc_scope, 
                                                                                             organizations,
                                                                                             vc_holy_grail_people)

# %%
model_input

# %%
only_this_vc = model_input[model_input[INVESTOR_EXPERIENCE_COLUMN] == VC_NAME]

model_input[INVESTOR_EXPERIENCE_COLUMN] = VC_NAME
model_input[INVESTOR_CITY_COLUMN] = only_this_vc[INVESTOR_CITY_COLUMN].iloc[0]
model_input[INVESTOR_REGION_COLUMN] = only_this_vc[INVESTOR_REGION_COLUMN].iloc[0]
model_input[INVESTOR_COUNTRY_CODE_COLUMN] = only_this_vc[INVESTOR_COUNTRY_CODE_COLUMN].iloc[0]

# %%
from bootcamp_2021_01.domain.persistence.use_cases.models_persistence import UseCasesModelPersistence
from bootcamp_2021_01.domain.use_cases import USE_CASE_NAME

MODEL_NAME = 'cat_boost'
models_persistence = UseCasesModelPersistence(io_api, USE_CASE_NAME, MODEL_NAME)

# %%
model = models_persistence.load_sklearn_model(run_id='run_notebook')

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
unique_scores = scores.drop(columns=['investor_experience_in_first_category', 
                                     'is_investor_country_same_as_company_s']).drop_duplicates()

# %%
sorted_scores = unique_scores.sort_values(by=SCORE_COLUMN, ascending=False)

# %%
preds_invest_by_vc = sorted_scores.head(invest_by_vc_count)

# %%
preds_invest_by_vc_count = len(preds_invest_by_vc)
preds_success_count_by_vc = len(preds_invest_by_vc[preds_invest_by_vc['reality'] == 1])
preds_success_rate = preds_success_count_by_vc / preds_invest_by_vc_count

# %%
print(f'Invest count : {preds_invest_by_vc_count}')
print(f'Success count : {preds_success_count_by_vc}')
print(f'Success rate : {(preds_success_rate*100):.2f} %')

# %% [markdown]
# ### Ekilibr8 prediction on VC failed investments

# %%
failed_invests = invest_by_vc#[invest_by_vc[SUCCESSFUL_SERIES_A_COLUMN] == 0]

# %%
failed_invests

# %%
company_scope = list(failed_invests[COMPANY_NAME_COLUMN])

# %%
failing_company_scope = series_a_success_or_not_df[series_a_success_or_not_df[COMPANY_NAME_COLUMN].isin(company_scope)]

# %%
from bootcamp_2021_01.domain.feature_engineering import feature_engineering

model_input, reality, company_name = feature_engineering.prepare_inputs_for_machine_learning(failing_company_scope, 
                                                                                             organizations,
                                                                                             vc_holy_grail_people)

# %%
only_this_vc = model_input[model_input[INVESTOR_EXPERIENCE_COLUMN] == VC_NAME]

model_input[INVESTOR_EXPERIENCE_COLUMN] = VC_NAME
model_input[INVESTOR_CITY_COLUMN] = only_this_vc[INVESTOR_CITY_COLUMN].iloc[0]
model_input[INVESTOR_REGION_COLUMN] = only_this_vc[INVESTOR_REGION_COLUMN].iloc[0]
model_input[INVESTOR_COUNTRY_CODE_COLUMN] = only_this_vc[INVESTOR_COUNTRY_CODE_COLUMN].iloc[0]

# %%
from bootcamp_2021_01.domain.persistence.use_cases.models_persistence import UseCasesModelPersistence
from bootcamp_2021_01.domain.use_cases import USE_CASE_NAME

MODEL_NAME = 'cat_boost'
models_persistence = UseCasesModelPersistence(io_api, USE_CASE_NAME, MODEL_NAME)

# %%
model = models_persistence.load_sklearn_model(run_id='run_notebook_id_invest')

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
unique_scores = scores.drop(columns=['investor_experience_in_first_category', 
                                     'is_investor_country_same_as_company_s']).drop_duplicates()

# %%
from bootcamp_2021_01.domain.persistence.use_cases.export_persistence import UseCaseExportPersistence

data_persistence = UseCaseExportPersistence(io_api, USE_CASE_NAME, 'demo', 'demo.csv')

# %%
export = scores[['company_name', 'country_code', 'city', 'reality', 'score']]

# %%
data_persistence.export_pandas_dataframe(export, 'demo')

# %%

# %% [markdown]
# ## Export predictions

# %%
from bootcamp_2021_01.domain.persistence.use_cases.export_persistence import UseCaseExportPersistence

# %%
export_persistence = UseCaseExportPersistence(
    io_api=io_api,
    use_case_name=USE_CASE_NAME,
    export_name='webapp_input',
    export_file_name='predictions.csv'
)

# %%
export_df = sorted_scores[[
    COMPANY_NAME_COLUMN, 
    COUNTRY_CODE_COLUMN, 
    REGION_COLUMN, 
    CITY_COLUMN, 
    DAYS_SINCE_FIRST_FUNDING_COLUMN, 
    SCORE_COLUMN
]]


# %%
export_persistence.export_pandas_dataframe(export_df, run_id='validation')


# %%
