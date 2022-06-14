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
WORK_DIR = '../../workdir'

# %% [markdown]
# # Load raw data for schema discovery

# %% [markdown]
# ## Load data

# %%
from pilotis_io.local import LocalIoApi, LocalPandasApi
from pilotis_io.directory_structure import dataset_raw_dir_path

# %%
io_api = LocalIoApi(WORK_DIR)
pandas_api = LocalPandasApi(io_api)

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
acq = pandas_api.load_pandas_dataset(acq_files, encoding='unicode_escape')
rounds = pandas_api.load_pandas_dataset(rounds_files, encoding='unicode_escape')
invest = pandas_api.load_pandas_dataset(invest_files, encoding='unicode_escape')

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
invest_and_rounds_joined = all_unique_invest \
    .set_index(['company_name', 'funded_at']) \
    .assign(invest=1) \
    .join(
    all_unique_rounds \
        .set_index(['company_name', 'funded_at']) \
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
651 / 2977.

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
rounds[rounds.company_name == "Zynga"][["funding_round_type", "funded_at", "raised_amount_usd"]].set_index(
    "funded_at").sort_index()

# %%

# %%
invest[invest.company_name == "Zynga"][
    ["funding_round_type", "funded_at", "raised_amount_usd", "investor_name"]].set_index("funded_at").sort_index()
