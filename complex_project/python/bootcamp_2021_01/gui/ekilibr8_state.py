from datetime import date

import pandas as pd
from ekinox_ds.directory_structure import dataset_raw_dir_path
from ekinox_ds.io import IoAPI

from bootcamp_2021_01.domain.feature_engineering import feature_engineering
from bootcamp_2021_01.domain.feature_engineering import target_definition
from bootcamp_2021_01.domain.feature_engineering.target_definition import SUCCESSFUL_SERIES_A_COLUMN, \
    INVESTOR_NAME_COLUMN, COMPANY_NAME_COLUMN
from bootcamp_2021_01.domain.persistence.use_cases.models_persistence import UseCasesModelPersistence
from bootcamp_2021_01.domain.use_cases import USE_CASE_NAME

UNICODE_ENCODING = 'unicode_escape'
VC_NAME = "Idinvest Partners"

MODEL_NAME = 'cat_boost'
SCORE_COLUMN = 'score'


class Ekilibr8:

    def __init__(self, io_api: IoAPI):
        all_vc_with_success_status = self._load_all_vc_with_success_status(io_api)
        is_target_vc = (all_vc_with_success_status[INVESTOR_NAME_COLUMN] == VC_NAME)
        target_vc_with_success_status = all_vc_with_success_status[is_target_vc]

        organizations = _load_raw_dataset(io_api,
                                          'bachelorarbeit_organizations',
                                          '2013-12-cleaned')

        people = _load_raw_dataset(io_api,
                                   'vc_holy_grail_people',
                                   'vc_holy_grail_cleaned')

        features, reality, company_name = feature_engineering.prepare_inputs_for_machine_learning(
            target_vc_with_success_status, organizations, people)

        predicted_scores = Ekilibr8._compute_scores(io_api, features)

        scores_and_features = features \
            .reset_index() \
            .assign(score=predicted_scores,
                    reality=reality.reset_index()[SUCCESSFUL_SERIES_A_COLUMN],
                    company_name=company_name.reset_index(drop=True))

        self.input_data_with_features_and_scores = target_vc_with_success_status \
            .set_index(COMPANY_NAME_COLUMN, drop=False) \
            .join(scores_and_features
                  .drop_duplicates(COMPANY_NAME_COLUMN)
                  .set_index(COMPANY_NAME_COLUMN)[[SCORE_COLUMN]])

    @staticmethod
    def _load_all_vc_with_success_status(io_api):
        notpeter_dataset_version = '2015-12'
        invest = _load_raw_dataset(io_api,
                                   'notpeter_investments',
                                   notpeter_dataset_version,
                                   encoding=UNICODE_ENCODING)
        acq = _load_raw_dataset(io_api,
                                'notpeter_acquisitions',
                                notpeter_dataset_version,
                                encoding=UNICODE_ENCODING)
        companies = _load_raw_dataset(io_api,
                                      'notpeter_companies',
                                      notpeter_dataset_version,
                                      encoding=UNICODE_ENCODING)
        current_date = date(2015, 12, 1)
        all_vc_with_success_status = target_definition.add_series_a_success_status(
            invest, acq, companies, current_date)
        return all_vc_with_success_status

    @staticmethod
    def _compute_scores(io_api: IoAPI,
                        model_input: pd.DataFrame,
                        model_name: str = MODEL_NAME,
                        model_run_id: str = 'run_notebook') -> pd.Series:
        models_persistence = UseCasesModelPersistence(io_api, USE_CASE_NAME, model_name)
        model = models_persistence.load_sklearn_model(run_id=model_run_id)

        predictions = model.predict_proba(model_input)
        return pd.DataFrame(predictions)[1]

    @staticmethod
    def to_dict(data: pd.DataFrame):
        return data.to_dict('records')


def _load_raw_dataset(io_api: IoAPI, dataset_name: str, dataset_version: str, *args, **kwargs) -> pd.DataFrame:
    dataset_path = dataset_raw_dir_path(dataset_name, dataset_version)
    dataset_files = io_api.list_files_in_dir(dataset_path)
    return io_api.load_pandas_dataset(dataset_files, *args, **kwargs)
