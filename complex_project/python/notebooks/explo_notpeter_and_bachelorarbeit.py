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

pd.set_option("display.max_columns", None)

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

# %% [markdown]
# ### Notpeter

# %%
dataset_version = '2015-12'

rounds_name = 'notpeter_rounds'
rounds_path = dataset_raw_dir_path(rounds_name, dataset_version)

invest_name = 'notpeter_investments'
invest_path = dataset_raw_dir_path(invest_name, dataset_version)

acq_name = 'notpeter_acquisitions'
acq_path = dataset_raw_dir_path(acq_name, dataset_version)

comp_name = 'notpeter_companies'
comp_path = dataset_raw_dir_path(comp_name, dataset_version)

rounds_files = io_api.list_files_in_dir(rounds_path)
invest_files = io_api.list_files_in_dir(invest_path)
acq_files = io_api.list_files_in_dir(acq_path)
comp_files = io_api.list_files_in_dir(comp_path)

rounds = io_api.load_pandas_dataset(rounds_files, encoding='unicode_escape')
invest = io_api.load_pandas_dataset(invest_files, encoding='unicode_escape')
acq = io_api.load_pandas_dataset(acq_files, encoding='unicode_escape')
companies = io_api.load_pandas_dataset(comp_files, encoding='unicode_escape')

# %% [markdown]
# ### Bachelorarbeit

# %%
dataset_version_bachelorarbeit = '2013-12'
dataset_version_bachelorarbeit_clean = '2013-12-cleaned'

people_name = 'bachelorarbeit_people'
people_path = dataset_raw_dir_path(people_name, dataset_version_bachelorarbeit)

orga_name = 'bachelorarbeit_organizations'
orga_path = dataset_raw_dir_path(orga_name, dataset_version_bachelorarbeit_clean)

people_files = io_api.list_files_in_dir(people_path)
orga_files = io_api.list_files_in_dir(orga_path)

people = io_api.load_pandas_dataset(people_files)
organizations = io_api.load_pandas_dataset(orga_files)

# %% [markdown]
# ### VC_Holy_Grail

# %%
vc_holy_grail_people_dataset_version = 'vc_holy_grail_cleaned'

vc_holy_grail_people_name = 'vc_holy_grail_people'
vc_holy_grail_people_path = dataset_raw_dir_path(vc_holy_grail_people_name, vc_holy_grail_people_dataset_version)


vc_holy_grail_people_files =  io_api.list_files_in_dir(vc_holy_grail_people_path)

vc_holy_grail_people = io_api.load_pandas_dataset(vc_holy_grail_people_files)

# %% [markdown]
# ## Explore data

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

# %%
vc_holy_grail_people.head()

# %%
companies.head()

# %%
companies.status.value_counts()

# %%
people.head()

# %%
acq.head()

# %%
invest.head()

# %%
rounds.head()

# %% [markdown]
# ### Seed vs angel

# %%
angel_companies = rounds[rounds.funding_round_type == "angel"].company_name	
seeds_and_angels = rounds[(rounds.funding_round_type == "seed") & 
                         (rounds.company_name.isin(angel_companies))]
seeds_and_angels.head(10)

# %%
rounds[rounds.company_name == "3D Industri.es"].sort_values("funded_at")

# %% [markdown]
# ### Rounds vs invest

# %%
rounds.shape, invest.shape

# %%
all_unique_rounds = rounds[['company_name', 'funded_at']].drop_duplicates()

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
rounds.funding_round_type.value_counts()

# %%
invest.funding_round_type.value_counts()

# %%
invest.funding_round_code.value_counts()

# %% [markdown]
# ### Failures and successes

# %%
seriesA = invest[invest.funding_round_code == "A"][["company_name", "funded_at"]]
seriesB = invest[invest.funding_round_code == "B"][["company_name"]].drop_duplicates()
seriesC = invest[invest.funding_round_code == "C"][["company_name"]].drop_duplicates()
acq_companies = acq[["company_name"]].assign(acq=1).drop_duplicates()
companies_with_people_info = people[["organization"]].drop_duplicates()
orga_info = organizations[["name"]].drop_duplicates()
companies_state = companies[["name", "status"]].drop_duplicates()

# %%
series_a_follow_up = seriesA.set_index("company_name").assign(seriesA=1).join(
    seriesB.set_index("company_name").assign(seriesB=1),
    how="left").join(
    seriesC.set_index("company_name").assign(seriesC=1),
    how="left").join(
    acq_companies.set_index("company_name"),
    how="left").join(
    companies_with_people_info.assign(known_people=1).set_index("organization"),
    how="left").join(
    orga_info.assign(known_orga_suppl_infos=1).set_index("name"),
    how="left").join(
    companies.set_index("name"),
    how="left")
series_a_follow_up.sum()

# %%
failures_new_invests = series_a_follow_up[(series_a_follow_up.seriesB.isnull()) &
                                      (series_a_follow_up.acq.isnull()) &
                                      (series_a_follow_up.status == "operating") &
                                      (series_a_follow_up.funded_at < "2013-12")]
failures_closure = series_a_follow_up[(series_a_follow_up.status == "closed")]

successes = series_a_follow_up[((series_a_follow_up.seriesB.notnull()) |
                            (series_a_follow_up.acq.notnull()) | 
                              (series_a_follow_up.status == "ipo") |
                              (series_a_follow_up.status == "acquired")) &
                              (series_a_follow_up.status != "closed")]
print(f"""
On a en tout {len(failures_new_invests) + len(failures_closure) + len(successes)} startups qui
pourront appartenir à notre échantillon d'apprentissage.
Parmis elles, a {len(failures_new_invests) + len(failures_closure)} échecs, dont {len(failures_new_invests)} 
startups sans nouvel investissements dans les 2 dernières années et {len(failures_closure)} 
startups qui ont fermé.
On a par ailleurs {len(successes)} companies pour lesquels l'investissement a été en succès 
(nouvel investissement, aquisition, IPO)
""")

# %%
failures.known_people.sum() / len(failures), successes.known_people.sum() / len(successes)

# %%
failures.known_orga_suppl_infos.sum() / len(failures), successes.known_orga_suppl_infos.sum() / len(successes)

# %% [markdown]
# Infos de features sans enrichissements externes :
#  - info sur les personnes travaillant dans la startup (~75% des cas : colonnes facebook_url	twitter_url	linkedin_url dans dataset people, nombre)
#  - infos sur la présence de la startup sur les réseaux sociaux (~90% des cas : twitter_url, facebook_url, linkedin_url dans organizations)
#  - secteur d'activité (category_list dans companies, ? dans organizations)
#  - date de crétion
#  - zone géographique
#  - stats sur le VC qui cherche à investir dans la startup
#  - investissements et investisseurs antérieurs dans la startup

# %% [markdown]
# ## Join tests

# %%
company_names_in_holy = vc_holy_grail_people[['Organization Name']].drop_duplicates().set_index("Organization Name")
print(company_names_in_holy.shape)

company_names_in_invest = invest[['company_name']].drop_duplicates().set_index("company_name")
print(company_names_in_invest.shape)

company_names_in_invest.join(company_names_in_holy, how="inner").shape


# %%
vc_holy_grail_people

# %%
