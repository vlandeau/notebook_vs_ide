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

python_dir = os.path.abspath('..')
sys.path.append(python_dir)

# %%
import bootcamp_2021_01

# %%
WORK_DIR = '../../workdir'

# %% [markdown]
# # Load raw data for schema discovery

# %% [markdown]
# ## Load data

# %%
from ekinox_ds.local.local_io_api import LocalIoApi
from ekinox_ds.directory_structure import dataset_raw_dir_path

# %%
io_api = LocalIoApi(WORK_DIR)

# %%
dataset_version = '2013-10'

acq_name = 'datahoarder_acquisition'
acq_path = dataset_raw_dir_path(acq_name, dataset_version)

rounds_name = 'datahoarder_rounds'
rounds_path = dataset_raw_dir_path(rounds_name, dataset_version)

invest_name = 'datahoarder_investment'
invest_path = dataset_raw_dir_path(invest_name, dataset_version)

# %%
acq_files = io_api.list_files_in_dir(acq_path)
rounds_files = io_api.list_files_in_dir(rounds_path)
invest_files = io_api.list_files_in_dir(invest_path)

# %%
acq = io_api.load_pandas_dataset(acq_files, encoding='unicode_escape')
rounds = io_api.load_pandas_dataset(rounds_files, encoding='unicode_escape')
invest = io_api.load_pandas_dataset(invest_files, encoding='unicode_escape')

# %% [markdown]
# ## Explore data

# %%
acq.head()

# %%
rounds.head()

# %%
len(rounds)

# %%
len(rounds[['company_name']].drop_duplicates())

# %%
all_unique_rounds = rounds[['company_name', 'funded_at']].drop_duplicates()

# %%
invest.head()

# %%
len(invest)

# %%
len(invest[['company_name']].drop_duplicates())

# %%
len(invest[['company_name', 'funded_at']].drop_duplicates())

# %%
all_unique_invest = invest[['company_name', 'funded_at']].drop_duplicates()

# %%
invest_and_rounds_joined = all_unique_invest\
                            .set_index(['company_name', 'funded_at'])\
                            .assign(invest=1)\
                            .join(
                                all_unique_rounds\
                                    .set_index(['company_name', 'funded_at'])\
                                    .assign(rounds=1), how='outer')
invest_and_rounds_joined

# %%
invest_and_rounds_joined.sum()

# %%
len(invest_and_rounds_joined)

# %%
rounds.funding_round_type.value_counts()

# %%
invest.funding_round_type.value_counts()

# %%
angels = invest[invest.funding_round_type == "angel"][["company_name"]].drop_duplicates()
seriesA = invest[invest.funding_round_type == "series-a"][["company_name"]].drop_duplicates()
seriesB = invest[invest.funding_round_type == "series-b"][["company_name"]].drop_duplicates()
seriesC = invest[invest.funding_round_type == "series-c+"][["company_name"]].drop_duplicates()
ventures = invest[invest.funding_round_type == "venture"][["company_name"]].drop_duplicates()

# %%
angels.set_index("company_name").assign(angel=1).join(
    seriesA.set_index("company_name").assign(seriesA=1),
    how="left").join(
    seriesB.set_index("company_name").assign(seriesB=1),
    how="left").join(
    seriesC.set_index("company_name").assign(seriesC=1),
    how="left").join(
    ventures.set_index("company_name").assign(ventures=1),
    how="left").sum()

# %%
651/2977.

# %%
seriesA.set_index("company_name").assign(seriesA=1).join(
    seriesB.set_index("company_name").assign(seriesB=1),
    how="left").join(
    seriesC.set_index("company_name").assign(seriesC=1),
    how="left").join(
    ventures.set_index("company_name").assign(ventures=1),
    how="left").sum()

# %%
1565.0 / 4590.0 

# %%

# %%
angels.head()

# %%

# %%

# %%
rounds[rounds.funding_round_type == "angel"]

# %%
rounds[rounds.company_name == "Zynga"][["funding_round_type", "funded_at", "raised_amount_usd"]].set_index("funded_at").sort_index()

# %%

# %%
invest[invest.company_name == "Zynga"][["funding_round_type", "funded_at", "raised_amount_usd", "investor_name"]].set_index("funded_at").sort_index()

# %%

# %% [markdown]
# plusieurs cas : 
# - VC en série A
# score = 0.8 -> si tu investi sur la compagnie X, celle-ci aura 80% de chances d'être rachetée ou de partir en bourse (IPO) ou d'avoir des investissements en série B et suivantes dans les n années
#
# - BA en seed
# score = 0.8 -> si tu investi sur la compagnie X, celle-ci aura 80% de chances d'être rachetée ou de partir en bourse (IPO) ou d'avoir des investissements en série A et suivantes
#
#
# dans le passé, le VC Y a investi sur X, puis X a été racheté par Z dans les n annéezs
# dans le passé, le BA A a investi sur B, qui n'a jamais été racheté/eu de nouvelles levées de fonds en succès dans les n années
#
# ? mesurer la plus-value du BA/VC ?
# ? creuser plus tard la réalité du statut d'échec/de succès ?

# %% [markdown]
# # Parse some files

# %%
# ! cd .. && poetry run python -m some_cool_project.application.parse --workdir ../workdir --dataset-name sample_dataset --dataset-version version_1


# %% [markdown]
# # Load parquet

# %%
from ekinox_ds.local.local_io_api import LocalIoApi
from ekinox_ds.directory_structure import dataset_parsed_dir_path

from bootcamp_2021_01.domain.persistence.landing.sample_dataset import SampleDatasetPersistence

# %%
dataset_version = 'version_1'

# %%
io_api = LocalIoApi(WORK_DIR)
persistence = SampleDatasetPersistence(io_api)

# %%
dataframe = persistence.load_parsed(dataset_version)

# %%
dataframe.head()

# %%
