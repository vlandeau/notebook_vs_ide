import datetime
from datetime import timedelta

import pandas as pd

FAILURE_FLAG = 0
SUCCESS_FLAG = 1

STATUS_CLOSED_VALUE = "closed"
HOMEPAGE_URL_COLUMN = "homepage_url"
FIRST_FUNDING_AT_COLUMN = "first_funding_at"
CITY_COLUMN = "city"
REGION_COLUMN = "region"
COUNTRY_CODE_COLUMN = "country_code"
TWO_YEARS_IN_DAYS = 365 * 2
FUNDED_AT_COLUMN = "funded_at"
STATUS_ACQUIRED_VALUE = "acquired"
LEFT_JOIN_TYPE = "left"
SUCCESSFUL_SERIES_A_COLUMN = "successful_series_a"
COMPANY_NAME_COLUMN = "company_name"
FUNDING_ROUND_CODE_COLUMN = "funding_round_code"
ROUND_CODE_SERIE_A_VALUE = "A"
ROUND_CODE_SERIE_SEED_VALUE = "seed"
ROUND_CODE_SERIE_B_VALUE = "B"
STATUS_IPO_VALUE = "ipo"
STATUS_COLUMN = "status"
NAME_COLUMN = "name"
FUNDED_AT_AS_DATE_COLUMN = "funded_at_as_date"
_IS_ACQUIRED_COL = "is_acquired"
_HAS_NEW_FUNDING_ROUND_COL = "has_new_funding_round"
INVESTOR_CITY_COLUMN = "investor_city"
INVESTOR_REGION_COLUMN = "investor_region"
INVESTOR_NAME_COLUMN = "investor_name"
INVESTOR_COUNTRY_CODE_COLUMN = "investor_country_code"


def add_series_a_success_status(investments: pd.DataFrame, acquisitions: pd.DataFrame, companies: pd.DataFrame,
                                current_date: datetime.date) -> pd.DataFrame:
    investments_with_parsed_date: pd.DataFrame = investments.assign(
        **{FUNDED_AT_AS_DATE_COLUMN: pd.to_datetime(investments[FUNDED_AT_COLUMN])}
    )

    series_a = investments_with_parsed_date[
        investments_with_parsed_date[FUNDING_ROUND_CODE_COLUMN] == ROUND_CODE_SERIE_A_VALUE]
    series_b = investments_with_parsed_date[
        investments_with_parsed_date[FUNDING_ROUND_CODE_COLUMN] == ROUND_CODE_SERIE_B_VALUE][
        [COMPANY_NAME_COLUMN]].drop_duplicates() \
        .set_index(COMPANY_NAME_COLUMN).assign(**{_HAS_NEW_FUNDING_ROUND_COL: True})
    acquired_companies = acquisitions[[COMPANY_NAME_COLUMN]] \
        .drop_duplicates() \
        .assign(**{_IS_ACQUIRED_COL: True}) \
        .set_index(COMPANY_NAME_COLUMN)
    company_info_columns = [STATUS_COLUMN, COUNTRY_CODE_COLUMN, REGION_COLUMN, CITY_COLUMN, NAME_COLUMN,
                            FIRST_FUNDING_AT_COLUMN, HOMEPAGE_URL_COLUMN]
    companies_info = companies[company_info_columns] \
        .drop_duplicates() \
        .set_index(NAME_COLUMN)
    companies_info.index = companies_info.index.map(str)
    companies_info.index.rename('company_name', inplace=True)

    series_a_follow_up = series_a \
        .set_index(COMPANY_NAME_COLUMN, drop=False) \
        .assign(series_a=1) \
        .join(series_b, how=LEFT_JOIN_TYPE) \
        .join(acquired_companies, how=LEFT_JOIN_TYPE) \
        .join(companies_info, how=LEFT_JOIN_TYPE) \
        .fillna({_IS_ACQUIRED_COL: False, _HAS_NEW_FUNDING_ROUND_COL: False})

    target_column = series_a_follow_up.apply(_is_successful_series_a, axis=1)
    labelled_data_without_date_consideration: pd.DataFrame = series_a_follow_up \
        .assign(**{SUCCESSFUL_SERIES_A_COLUMN: target_column})

    return _remove_uneligible_early_companies(current_date, labelled_data_without_date_consideration)


def _remove_uneligible_early_companies(current_date, labelled_data_without_date_consideration):
    max_date_for_failure_consideration = current_date - timedelta(days=TWO_YEARS_IN_DAYS)
    old_enough_funding = labelled_data_without_date_consideration[
                             FUNDED_AT_AS_DATE_COLUMN] < max_date_for_failure_consideration

    successful_series_a = labelled_data_without_date_consideration[SUCCESSFUL_SERIES_A_COLUMN] == SUCCESS_FLAG
    failed_exit = labelled_data_without_date_consideration[STATUS_COLUMN] == STATUS_CLOSED_VALUE

    return labelled_data_without_date_consideration[successful_series_a | failed_exit | old_enough_funding]


def _is_successful_series_a(local_series_a_follow_up: pd.Series) -> int:
    if (local_series_a_follow_up[_HAS_NEW_FUNDING_ROUND_COL] & (
            local_series_a_follow_up[STATUS_COLUMN] != STATUS_CLOSED_VALUE)) \
            | _has_successful_exit(local_series_a_follow_up):
        return SUCCESS_FLAG
    return FAILURE_FLAG


def _has_successful_exit(local_series_a_followup: pd.Series) -> bool:
    return local_series_a_followup[_IS_ACQUIRED_COL] | \
           (local_series_a_followup[STATUS_COLUMN] == STATUS_IPO_VALUE) | \
           (local_series_a_followup[STATUS_COLUMN] == STATUS_ACQUIRED_VALUE)
