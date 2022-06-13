from typing import Tuple

import pandas as pd

from bootcamp_2021_01.domain.feature_engineering.target_definition import HOMEPAGE_URL_COLUMN, COUNTRY_CODE_COLUMN, \
    REGION_COLUMN, CITY_COLUMN, SUCCESSFUL_SERIES_A_COLUMN, INVESTOR_COUNTRY_CODE_COLUMN, INVESTOR_REGION_COLUMN, \
    INVESTOR_CITY_COLUMN, INVESTOR_NAME_COLUMN, FUNDED_AT_AS_DATE_COLUMN, FIRST_FUNDING_AT_COLUMN, NAME_COLUMN, \
    LEFT_JOIN_TYPE, COMPANY_NAME_COLUMN

NO_EMPLOYEE = 0
TWITTER_URL_COLUMN = "twitter_url"
FACEBOOK_URL_COLUMN = "facebook_url"
LINKEDIN_URL_COLUMN = "linkedin_url"

FLAG_FALSE = 0
FLAG_TRUE = 1
FLAG_NO_PEOPLE_INFO = -1

COMPANY_CATEGORY_LIST_COLUMN = "company_category_list"
EXPERIENCE_IN_FIRST_CATEGORY_COLUMN = "investor_experience_in_first_category"
COMPANY_AGE_COLUMN = "number_of_days_since_first_january_70"
COMPANY_FIRST_CATEGORY_COLUMN = "company_first_category"
COMPANY_SECOND_CATEGORY_COLUMN = "company_second_category"
COMPANY_THIRD_CATEGORY_COLUMN = "company_third_category"
COMPANY_FOURTH_CATEGORY_COLUMN = "company_fourth_category"
COMPANY_FIFTH_CATEGORY_COLUMN = "company_fifth_category"
INVESTOR_EXPERIENCE_COLUMN = "investor_global_experience"
DAYS_SINCE_FIRST_FUNDING_COLUMN = "nb_days_since_first_funding"
HAS_HOMEPAGE_URL_COLUMN = "has_homepage_url"
HAS_FACEBOOK_COLUMN = "has_facebook"
HAS_TWITTER_COLUMN = "has_twitter"
HAS_LINKEDIN_COLUMN = "has_linkdedin"
DEFAULT_CATEGORICAL_FEATURE_VALUE = "Unknown"
IS_INVESTOR_COUNTRY_SAME_AS_COMPANY_S = "is_investor_country_same_as_company_s"
NUMBER_OF_FOUNDED_ORGANIZATIONS_COLUMN = 'Number of Founded Organizations'
NUMBER_OF_PORTFOLIO_COMPANIES_COLUMN = 'Number of Portfolio Companies'
NUMBER_OF_INVESTMENTS_COLUMN = 'Number of Investments'
NUMBER_OF_PARTNER_INVESTMENTS_COLUMN = 'Number of Partner Investments'
NUMBER_OF_NEWS_ARTICLES_COLUMN = 'Number of News Articles'
NUMBER_OF_LEAD_INVESTMENTS_COLUMN = 'Number of Lead Investments'
NUMBER_OF_EXITS_COLUMN = 'Number of Exits'
NUMBER_OF_EVENTS_COLUMN = 'Number of Events'

PEOPLE_INFORMATION_COLUMNS = [NUMBER_OF_FOUNDED_ORGANIZATIONS_COLUMN,
                              NUMBER_OF_PORTFOLIO_COMPANIES_COLUMN,
                              NUMBER_OF_INVESTMENTS_COLUMN,
                              NUMBER_OF_PARTNER_INVESTMENTS_COLUMN,
                              NUMBER_OF_NEWS_ARTICLES_COLUMN,
                              NUMBER_OF_LEAD_INVESTMENTS_COLUMN,
                              NUMBER_OF_EXITS_COLUMN,
                              NUMBER_OF_EVENTS_COLUMN]


def _clean_people_column(col_name: str) -> str:
    return col_name.replace("Number of ", "").replace(" ", "_").lower()


PEOPLE_INFORMATION_PARSED_NAME_COLUMNS = [_clean_people_column(col) for col in PEOPLE_INFORMATION_COLUMNS]
PEOPLE_INFORMATION_FEATURES_NAMES = [f'{agg}_{people_information_column}'
                                     for agg in ['min', 'max', 'mean']
                                     for people_information_column in PEOPLE_INFORMATION_PARSED_NAME_COLUMNS]

FEATURES_LIST = [
                    HAS_HOMEPAGE_URL_COLUMN,
                    DAYS_SINCE_FIRST_FUNDING_COLUMN,
                    COUNTRY_CODE_COLUMN,
                    REGION_COLUMN,
                    CITY_COLUMN,
                    INVESTOR_COUNTRY_CODE_COLUMN,
                    INVESTOR_REGION_COLUMN,
                    INVESTOR_CITY_COLUMN,
                    INVESTOR_EXPERIENCE_COLUMN,
                    COMPANY_FIRST_CATEGORY_COLUMN,
                    COMPANY_SECOND_CATEGORY_COLUMN,
                    COMPANY_THIRD_CATEGORY_COLUMN,
                    COMPANY_FOURTH_CATEGORY_COLUMN,
                    COMPANY_FIFTH_CATEGORY_COLUMN,
                    COMPANY_AGE_COLUMN,
                    EXPERIENCE_IN_FIRST_CATEGORY_COLUMN,
                    IS_INVESTOR_COUNTRY_SAME_AS_COMPANY_S,
                    HAS_FACEBOOK_COLUMN,
                    HAS_TWITTER_COLUMN,
                    HAS_LINKEDIN_COLUMN,
                    'count_employee_in_crunchbase'
                ] + PEOPLE_INFORMATION_FEATURES_NAMES


def prepare_inputs_for_machine_learning(raw_df: pd.DataFrame,
                                        organizations_infos: pd.DataFrame,
                                        people_infos: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    processed_features: pd.DataFrame = _process_features(raw_df)
    df_with_organizations_features = _add_organization_information(processed_features, organizations_infos)
    df_with_people_features = _add_people_information(df_with_organizations_features, people_infos)
    return (df_with_people_features[FEATURES_LIST],
            df_with_people_features[SUCCESSFUL_SERIES_A_COLUMN],
            df_with_people_features[COMPANY_NAME_COLUMN])


def _process_features(raw_df: pd.DataFrame) -> pd.DataFrame:
    time_since_first_funding = pd.to_datetime(raw_df[FUNDED_AT_AS_DATE_COLUMN]) \
                               - pd.to_datetime(raw_df[FIRST_FUNDING_AT_COLUMN])
    number_of_days_since_first_funding = time_since_first_funding \
        .apply(lambda x: x.days) \
        .fillna(0) \
        .apply(int) \
        .apply(lambda x: x if x >= 0 else 0)
    number_of_days_since_first_january_70 = \
        (pd.to_datetime(raw_df[FUNDED_AT_AS_DATE_COLUMN]) - pd.to_datetime("1970-01-01")) \
            .apply(lambda x: x.days) \
            .apply(int)
    company_categories_list = raw_df[COMPANY_CATEGORY_LIST_COLUMN].apply(lambda x: str(x).split("|"))
    company_first_category = company_categories_list.apply(lambda x: x[0])
    company_second_category = company_categories_list.apply(
        lambda x: x[1] if len(x) >= 2 else DEFAULT_CATEGORICAL_FEATURE_VALUE)
    company_third_category = company_categories_list.apply(
        lambda x: x[2] if len(x) >= 3 else DEFAULT_CATEGORICAL_FEATURE_VALUE)
    company_fourth_category = company_categories_list.apply(
        lambda x: x[3] if len(x) >= 4 else DEFAULT_CATEGORICAL_FEATURE_VALUE)
    company_fifth_category = company_categories_list.apply(
        lambda x: x[4] if len(x) >= 5 else DEFAULT_CATEGORICAL_FEATURE_VALUE)
    investor_name_and_startup_category = raw_df[INVESTOR_NAME_COLUMN] + "-" + company_first_category
    is_country_same = (raw_df[COUNTRY_CODE_COLUMN] == raw_df[INVESTOR_COUNTRY_CODE_COLUMN]).apply(
        lambda is_same_country: FLAG_TRUE if is_same_country else FLAG_FALSE
    )

    df_with_new_features = raw_df.assign(**{HAS_HOMEPAGE_URL_COLUMN: _is_column_not_null(raw_df, HOMEPAGE_URL_COLUMN),
                                            DAYS_SINCE_FIRST_FUNDING_COLUMN: number_of_days_since_first_funding,
                                            COMPANY_FIRST_CATEGORY_COLUMN: company_first_category,
                                            COMPANY_SECOND_CATEGORY_COLUMN: company_second_category,
                                            COMPANY_THIRD_CATEGORY_COLUMN: company_third_category,
                                            COMPANY_FOURTH_CATEGORY_COLUMN: company_fourth_category,
                                            COMPANY_FIFTH_CATEGORY_COLUMN: company_fifth_category,
                                            COMPANY_AGE_COLUMN: number_of_days_since_first_january_70,
                                            EXPERIENCE_IN_FIRST_CATEGORY_COLUMN: investor_name_and_startup_category,
                                            # The model will use this feature to evaluate the investor success rate when
                                            # investing in startups of this category
                                            INVESTOR_EXPERIENCE_COLUMN: raw_df[INVESTOR_NAME_COLUMN],
                                            # The model will use this feature to evaluate the investor
                                            # global success rate
                                            IS_INVESTOR_COUNTRY_SAME_AS_COMPANY_S: is_country_same})
    return df_with_new_features.fillna(DEFAULT_CATEGORICAL_FEATURE_VALUE)


def _add_organization_information(df: pd.DataFrame, organizations_informations: pd.DataFrame) -> pd.DataFrame:
    organization_infos_to_retrieve = organizations_informations.set_index(NAME_COLUMN)[[
        FACEBOOK_URL_COLUMN, TWITTER_URL_COLUMN, LINKEDIN_URL_COLUMN]].drop_duplicates()
    df_with_organizations_raw_infos = df.set_index(COMPANY_NAME_COLUMN, drop=False) \
        .join(organization_infos_to_retrieve, how=LEFT_JOIN_TYPE)

    return df_with_organizations_raw_infos \
        .assign(**{HAS_FACEBOOK_COLUMN: _is_column_not_null(df_with_organizations_raw_infos, FACEBOOK_URL_COLUMN),
                   HAS_TWITTER_COLUMN: _is_column_not_null(df_with_organizations_raw_infos, TWITTER_URL_COLUMN),
                   HAS_LINKEDIN_COLUMN: _is_column_not_null(df_with_organizations_raw_infos, LINKEDIN_URL_COLUMN)})


def _is_column_not_null(df: pd.DataFrame, column: str) -> pd.Series:
    return df[column].notnull().apply(lambda has_url: FLAG_TRUE if has_url else FLAG_FALSE)


def _add_people_information(df: pd.DataFrame, people: pd.DataFrame) -> pd.DataFrame:
    parsed_people = _parse_people_information(people)

    aggregations = {
        people_information_column: ["min", "mean", "max"]
        for people_information_column in PEOPLE_INFORMATION_COLUMNS
    }
    aggregations.update({'employee_in_crunchbase': 'count'})

    fills = {col_name: FLAG_NO_PEOPLE_INFO for col_name in PEOPLE_INFORMATION_FEATURES_NAMES}
    fills.update({'count_employee_in_crunchbase': NO_EMPLOYEE})

    people_by_company = parsed_people \
        .assign(employee_in_crunchbase=1) \
        .groupby("Organization Name") \
        .agg(aggregations) \
        .rename(columns=_clean_people_column)
    people_by_company.columns = [f"{col_name_tuple[1]}_{col_name_tuple[0]}"
                                 for col_name_tuple in people_by_company.columns]

    return df \
        .set_index(COMPANY_NAME_COLUMN, drop=False) \
        .join(people_by_company, how=LEFT_JOIN_TYPE) \
        .fillna(fills)


def _parse_people_information(raw_people_df: pd.DataFrame) -> pd.DataFrame:
    def parse_str_representation(str_representation: str) -> int:
        if str_representation is not None:
            try:
                return int(str(str_representation).replace(",", ""))
            except ValueError:
                return 0
        return 0

    return raw_people_df.assign(**{
        people_info_col: raw_people_df[people_info_col].apply(parse_str_representation)
        for people_info_col in PEOPLE_INFORMATION_COLUMNS
    })
