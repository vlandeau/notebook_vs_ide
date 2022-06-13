import datetime

import pandas as pd
from hamcrest import assert_that, contains_inanyorder, equal_to, only_contains, has_items, is_

from bootcamp_2021_01.domain.feature_engineering.target_definition import COMPANY_NAME_COLUMN, \
    FUNDING_ROUND_CODE_COLUMN, ROUND_CODE_SERIE_A_VALUE, ROUND_CODE_SERIE_SEED_VALUE, ROUND_CODE_SERIE_B_VALUE, \
    STATUS_IPO_VALUE, STATUS_COLUMN, NAME_COLUMN, STATUS_ACQUIRED_VALUE, FUNDED_AT_COLUMN, SUCCESS_FLAG, FAILURE_FLAG, \
    COUNTRY_CODE_COLUMN, REGION_COLUMN, CITY_COLUMN, FIRST_FUNDING_AT_COLUMN, HOMEPAGE_URL_COLUMN, \
    INVESTOR_CITY_COLUMN, INVESTOR_REGION_COLUMN, INVESTOR_NAME_COLUMN, INVESTOR_COUNTRY_CODE_COLUMN
from bootcamp_2021_01.domain.feature_engineering.target_definition import add_series_a_success_status, \
    SUCCESSFUL_SERIES_A_COLUMN


def test_add_series_a_success_status_when_company_is_funded_another_time_after_series_a():
    # Given
    successful_company_name = "successful_series_a"
    not_successful_company_name = "not_successful_serie_a"
    old_date = "2010-01"
    another_old_date = "2011-01"
    investments = pd.DataFrame(
        {
            FUNDING_ROUND_CODE_COLUMN: [ROUND_CODE_SERIE_A_VALUE,
                                        ROUND_CODE_SERIE_B_VALUE,
                                        ROUND_CODE_SERIE_SEED_VALUE,
                                        ROUND_CODE_SERIE_A_VALUE],
            COMPANY_NAME_COLUMN: [successful_company_name,
                                  successful_company_name,
                                  not_successful_company_name,
                                  not_successful_company_name],
            FUNDED_AT_COLUMN: [old_date,
                               another_old_date,
                               old_date,
                               another_old_date]
        }
    )
    acquisitions = pd.DataFrame({
        COMPANY_NAME_COLUMN: []
    })
    companies = pd.DataFrame({
        NAME_COLUMN: [],
        STATUS_COLUMN: [],
        COUNTRY_CODE_COLUMN: [],
        REGION_COLUMN: [],
        CITY_COLUMN: [],
        FIRST_FUNDING_AT_COLUMN: [],
        HOMEPAGE_URL_COLUMN: []
    })

    # When
    df_with_target = add_series_a_success_status(investments, acquisitions, companies, datetime.date.today())

    # Then
    successful_company_success_status = df_with_target.loc[
        df_with_target[COMPANY_NAME_COLUMN] == successful_company_name, SUCCESSFUL_SERIES_A_COLUMN].tolist()
    assert_that(successful_company_success_status, contains_inanyorder(SUCCESS_FLAG))

    unsuccessful_company_success_status = df_with_target.loc[
        df_with_target[COMPANY_NAME_COLUMN] == not_successful_company_name, SUCCESSFUL_SERIES_A_COLUMN].tolist()
    assert_that(unsuccessful_company_success_status, contains_inanyorder(FAILURE_FLAG))


def test_that_add_series_a_success_status_outputs_all_the_expected_columns():
    # Given
    some_company_name = "some_series_a"
    some_date = "2010-01"
    investments = pd.DataFrame(
        {
            FUNDING_ROUND_CODE_COLUMN: [ROUND_CODE_SERIE_A_VALUE],
            COMPANY_NAME_COLUMN: [some_company_name],
            FUNDED_AT_COLUMN: [some_date],
            INVESTOR_COUNTRY_CODE_COLUMN: [None],
            INVESTOR_REGION_COLUMN: [None],
            INVESTOR_CITY_COLUMN: [None],
            INVESTOR_NAME_COLUMN: [None],
        }
    )
    acquisitions = pd.DataFrame({
        COMPANY_NAME_COLUMN: []
    })
    companies = pd.DataFrame({
        NAME_COLUMN: [],
        STATUS_COLUMN: [],
        COUNTRY_CODE_COLUMN: [],
        REGION_COLUMN: [],
        CITY_COLUMN: [],
        FIRST_FUNDING_AT_COLUMN: [],
        HOMEPAGE_URL_COLUMN: []
    })

    # When
    df_with_target: pd.DataFrame = add_series_a_success_status(investments, acquisitions, companies,
                                                               datetime.date.today())

    # Then
    assert_that(df_with_target.columns, has_items(COUNTRY_CODE_COLUMN,
                                                  REGION_COLUMN,
                                                  CITY_COLUMN,
                                                  FIRST_FUNDING_AT_COLUMN,
                                                  HOMEPAGE_URL_COLUMN,
                                                  INVESTOR_COUNTRY_CODE_COLUMN,
                                                  INVESTOR_REGION_COLUMN,
                                                  INVESTOR_CITY_COLUMN,
                                                  INVESTOR_NAME_COLUMN))


def test_that_add_series_a_success_status_does_not_fail_if_any_column_is_redundant_among_datasets():
    # Given
    some_company_name = "some_series_a"
    some_date = "2010-01"
    redundant_column = "redundant_column"
    investments = pd.DataFrame(
        {
            COMPANY_NAME_COLUMN: [some_company_name],
            FUNDING_ROUND_CODE_COLUMN: [ROUND_CODE_SERIE_A_VALUE],
            FUNDED_AT_COLUMN: [some_date],
            redundant_column: [None],
        }
    )
    acquisitions = pd.DataFrame({
        redundant_column: [],
        COMPANY_NAME_COLUMN: [],
    })
    companies = pd.DataFrame({
        redundant_column: [],
        NAME_COLUMN: [],
        STATUS_COLUMN: [],
        COUNTRY_CODE_COLUMN: [],
        REGION_COLUMN: [],
        CITY_COLUMN: [],
        FIRST_FUNDING_AT_COLUMN: [],
        HOMEPAGE_URL_COLUMN: [],
    })

    # When / Then an error is expected if the implementation is incorrect
    add_series_a_success_status(investments, acquisitions, companies, datetime.date.today())


def test_add_series_a_success_status_should_exclude_unsuccessful_company_if_too_young():
    # Given
    not_successful_company_name = "not_successful_serie_a"
    recent_date = "2020-01"
    investments = pd.DataFrame(
        {
            FUNDING_ROUND_CODE_COLUMN: [ROUND_CODE_SERIE_A_VALUE],
            COMPANY_NAME_COLUMN: [not_successful_company_name],
            FUNDED_AT_COLUMN: [recent_date]
        }
    )
    acquisitions = pd.DataFrame({
        COMPANY_NAME_COLUMN: []
    })
    companies = pd.DataFrame({
        NAME_COLUMN: [],
        STATUS_COLUMN: [],
        COUNTRY_CODE_COLUMN: [],
        REGION_COLUMN: [],
        CITY_COLUMN: [],
        FIRST_FUNDING_AT_COLUMN: [],
        HOMEPAGE_URL_COLUMN: []
    })

    # When
    df_with_target = add_series_a_success_status(investments, acquisitions, companies, datetime.date(2020, 2, 1))

    # Then
    assert_that(len(df_with_target), equal_to(FAILURE_FLAG))


def test_add_series_a_success_status_when_company_is_acquired():
    # Given
    successful_company_name = "successful_series_a"
    not_successful_company_name = "not_successful_serie_a"
    old_date = "2010-01"
    another_old_date = "2011-01"
    investments = pd.DataFrame(
        {
            FUNDING_ROUND_CODE_COLUMN: [ROUND_CODE_SERIE_A_VALUE,
                                        ROUND_CODE_SERIE_SEED_VALUE,
                                        ROUND_CODE_SERIE_A_VALUE],
            COMPANY_NAME_COLUMN: [successful_company_name,
                                  not_successful_company_name,
                                  not_successful_company_name],
            FUNDED_AT_COLUMN: [old_date,
                               old_date,
                               another_old_date]
        }
    )
    acquisitions = pd.DataFrame({
        COMPANY_NAME_COLUMN: [successful_company_name],
    })

    companies = pd.DataFrame({
        NAME_COLUMN: [],
        STATUS_COLUMN: [],
        COUNTRY_CODE_COLUMN: [],
        REGION_COLUMN: [],
        CITY_COLUMN: [],
        FIRST_FUNDING_AT_COLUMN: [],
        HOMEPAGE_URL_COLUMN: []
    })

    # When
    df_with_target = add_series_a_success_status(investments, acquisitions, companies, datetime.date.today())

    # Then
    successful_company_success_status = df_with_target.loc[
        df_with_target[COMPANY_NAME_COLUMN] == successful_company_name, SUCCESSFUL_SERIES_A_COLUMN].tolist()
    assert_that(successful_company_success_status, contains_inanyorder(SUCCESS_FLAG))

    unsuccessful_company_success_status = df_with_target.loc[
        df_with_target[COMPANY_NAME_COLUMN] == not_successful_company_name, SUCCESSFUL_SERIES_A_COLUMN].tolist()
    assert_that(unsuccessful_company_success_status, contains_inanyorder(FAILURE_FLAG))


def test_add_series_a_success_status_when_company_has_a_successful_exit():
    # Given
    ipo_status_company_name = "ipo_status_company_name"
    acquired_status_company_name = "acquired_status_company_name"
    any_date = "2015-01"
    investments = pd.DataFrame(
        {
            FUNDING_ROUND_CODE_COLUMN: [
                ROUND_CODE_SERIE_A_VALUE,
                ROUND_CODE_SERIE_A_VALUE,
            ],
            COMPANY_NAME_COLUMN: [
                ipo_status_company_name,
                acquired_status_company_name,
            ],
            FUNDED_AT_COLUMN: [
                any_date,
                any_date,
            ]
        }
    )
    acquisitions = pd.DataFrame({
        COMPANY_NAME_COLUMN: []
    })

    companies = pd.DataFrame({
        NAME_COLUMN: [
            ipo_status_company_name,
            acquired_status_company_name,
        ],
        STATUS_COLUMN: [
            STATUS_IPO_VALUE,
            STATUS_ACQUIRED_VALUE,
        ],
        COUNTRY_CODE_COLUMN: [None, None],
        REGION_COLUMN: [None, None],
        CITY_COLUMN: [None, None],
        FIRST_FUNDING_AT_COLUMN: [None, None],
        HOMEPAGE_URL_COLUMN: [None, None],
    })

    # When
    df_with_target = add_series_a_success_status(investments, acquisitions, companies, datetime.date.today())

    # Then
    assert_that(df_with_target[SUCCESSFUL_SERIES_A_COLUMN], only_contains(SUCCESS_FLAG))


def test_add_series_a_success_status_when_company_has_a_failed_exit():
    # Given
    closed_status_company_name = "closed_status_company_name"
    recent_date = "2020-01"
    investments = pd.DataFrame(
        {
            FUNDING_ROUND_CODE_COLUMN: [
                ROUND_CODE_SERIE_A_VALUE,
            ],
            COMPANY_NAME_COLUMN: [
                closed_status_company_name,
            ],
            FUNDED_AT_COLUMN: [
                recent_date,
            ]
        }
    )
    acquisitions = pd.DataFrame({
        COMPANY_NAME_COLUMN: []
    })

    companies = pd.DataFrame({
        NAME_COLUMN: [
            closed_status_company_name,
        ],
        STATUS_COLUMN: [
            "closed",
        ],
        COUNTRY_CODE_COLUMN: [None],
        REGION_COLUMN: [None],
        CITY_COLUMN: [None],
        FIRST_FUNDING_AT_COLUMN: [None],
        HOMEPAGE_URL_COLUMN: [None],
    })

    # When
    df_with_target = add_series_a_success_status(investments, acquisitions, companies, datetime.date.today())

    # Then
    assert_that(df_with_target[SUCCESSFUL_SERIES_A_COLUMN], only_contains(FAILURE_FLAG))


def test_add_series_a_success_status_when_duplicated_acquisition_or_company_info():
    some_company_name = "some_series_a"
    some_date = "2010-01"
    investments = pd.DataFrame(
        {
            COMPANY_NAME_COLUMN: [some_company_name],
            FUNDING_ROUND_CODE_COLUMN: [ROUND_CODE_SERIE_A_VALUE],
            FUNDED_AT_COLUMN: [some_date],
        }
    )
    acquisitions = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company_name, some_company_name],
    })
    companies = pd.DataFrame({
        NAME_COLUMN: [some_company_name, some_company_name],
        STATUS_COLUMN: ["ipo", "ipo"],
        COUNTRY_CODE_COLUMN: [None, None],
        REGION_COLUMN: [None, None],
        CITY_COLUMN: [None, None],
        FIRST_FUNDING_AT_COLUMN: [None, None],
        HOMEPAGE_URL_COLUMN: [None, None],
    })

    # When
    df_with_target = add_series_a_success_status(investments, acquisitions, companies, datetime.date.today())

    # Then
    assert_that(len(df_with_target), is_(SUCCESS_FLAG))
