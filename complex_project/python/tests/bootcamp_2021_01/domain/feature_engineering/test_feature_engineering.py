import pandas as pd
from hamcrest import assert_that, contains_exactly
from datetime import date

from bootcamp_2021_01.domain.feature_engineering.feature_engineering import _process_features, HAS_HOMEPAGE_URL_COLUMN, \
    DEFAULT_CATEGORICAL_FEATURE_VALUE, COMPANY_CATEGORY_LIST_COLUMN, COMPANY_FIRST_CATEGORY_COLUMN, \
    DAYS_SINCE_FIRST_FUNDING_COLUMN, COMPANY_AGE_COLUMN, EXPERIENCE_IN_FIRST_CATEGORY_COLUMN, FLAG_TRUE, FLAG_FALSE, \
    IS_INVESTOR_COUNTRY_SAME_AS_COMPANY_S, COMPANY_SECOND_CATEGORY_COLUMN, COMPANY_THIRD_CATEGORY_COLUMN, \
    COMPANY_FOURTH_CATEGORY_COLUMN, COMPANY_FIFTH_CATEGORY_COLUMN, _add_organization_information, HAS_FACEBOOK_COLUMN, \
    HAS_TWITTER_COLUMN, HAS_LINKEDIN_COLUMN, _add_people_information, PEOPLE_INFORMATION_PARSED_NAME_COLUMNS, \
    FLAG_NO_PEOPLE_INFO, _parse_people_information, PEOPLE_INFORMATION_COLUMNS

from bootcamp_2021_01.domain.feature_engineering.target_definition import COMPANY_NAME_COLUMN, HOMEPAGE_URL_COLUMN, \
    FUNDED_AT_AS_DATE_COLUMN, FIRST_FUNDING_AT_COLUMN, INVESTOR_NAME_COLUMN, COUNTRY_CODE_COLUMN, \
    INVESTOR_COUNTRY_CODE_COLUMN, NAME_COLUMN


def test_process_features_should_add_column_giving_company_homepage_url_presence():
    # Given
    company_with_homepage_url = "company_with_homepage_url"
    company_without_homepage_url = "company_without_homepage_url"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [company_with_homepage_url, company_without_homepage_url],
        HOMEPAGE_URL_COLUMN: ["www.my-website.com", None],
        FUNDED_AT_AS_DATE_COLUMN: [date(2013, 1, 1), date(2013, 1, 1)],
        FIRST_FUNDING_AT_COLUMN: ["2012-01-01", "2012-01-01"],
        COMPANY_CATEGORY_LIST_COLUMN: [None, None],
        INVESTOR_NAME_COLUMN: ["investor_name", "investor_name"],
        COUNTRY_CODE_COLUMN: [None, None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None, None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[HAS_HOMEPAGE_URL_COLUMN], contains_exactly(FLAG_TRUE, FLAG_FALSE))


def test_process_features_should_fill_empty_values():
    # Given
    some_feature = "some_feature"
    input_df = pd.DataFrame({
        HOMEPAGE_URL_COLUMN: ["www.my-website.com"],
        some_feature: [None],
        FUNDED_AT_AS_DATE_COLUMN: [date(2013, 1, 1)],
        FIRST_FUNDING_AT_COLUMN: ["2012-01-01"],
        COMPANY_CATEGORY_LIST_COLUMN: [None],
        INVESTOR_NAME_COLUMN: ["investor_name"],
        COUNTRY_CODE_COLUMN: [None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[some_feature], contains_exactly(DEFAULT_CATEGORICAL_FEATURE_VALUE))


def test_process_features_should_add_difference_between_first_and_current_funding():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company],
        HOMEPAGE_URL_COLUMN: [None],
        FUNDED_AT_AS_DATE_COLUMN: [date(2013, 1, 1)],
        FIRST_FUNDING_AT_COLUMN: ["2012-01-02"],
        COMPANY_CATEGORY_LIST_COLUMN: [None],
        INVESTOR_NAME_COLUMN: ["investor_name"],
        COUNTRY_CODE_COLUMN: [None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[DAYS_SINCE_FIRST_FUNDING_COLUMN], contains_exactly(365))


def test_process_features_should_add_zero_difference_between_first_and_current_funding_if_unknonw_first_funding():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company],
        HOMEPAGE_URL_COLUMN: [None],
        FUNDED_AT_AS_DATE_COLUMN: [date(2013, 1, 1)],
        FIRST_FUNDING_AT_COLUMN: [None],
        COMPANY_CATEGORY_LIST_COLUMN: [None],
        INVESTOR_NAME_COLUMN: ["investor_name"],
        COUNTRY_CODE_COLUMN: [None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[DAYS_SINCE_FIRST_FUNDING_COLUMN], contains_exactly(0))


def test_process_features_should_add_zero_difference_between_first_and_current_funding_if_first_funding_after_current_one():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company],
        HOMEPAGE_URL_COLUMN: [None],
        FUNDED_AT_AS_DATE_COLUMN: [date(2013, 1, 1)],
        FIRST_FUNDING_AT_COLUMN: ["2014-01-02"],
        COMPANY_CATEGORY_LIST_COLUMN: [None],
        INVESTOR_NAME_COLUMN: ["investor_name"],
        COUNTRY_CODE_COLUMN: [None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[DAYS_SINCE_FIRST_FUNDING_COLUMN], contains_exactly(0))


def test_process_features_should_add_number_of_days_since_first_january_70():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company],
        HOMEPAGE_URL_COLUMN: [None],
        FUNDED_AT_AS_DATE_COLUMN: [date(1970, 1, 11)],
        FIRST_FUNDING_AT_COLUMN: [None],
        COMPANY_CATEGORY_LIST_COLUMN: [None],
        INVESTOR_NAME_COLUMN: ["investor_name"],
        COUNTRY_CODE_COLUMN: [None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[COMPANY_AGE_COLUMN], contains_exactly(10))


def test_process_features_should_extract_first_company_category():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company],
        HOMEPAGE_URL_COLUMN: [None],
        FUNDED_AT_AS_DATE_COLUMN: [date(1970, 1, 10)],
        FIRST_FUNDING_AT_COLUMN: [None],
        COMPANY_CATEGORY_LIST_COLUMN: ["a|b|c"],
        INVESTOR_NAME_COLUMN: ["investor_name"],
        COUNTRY_CODE_COLUMN: [None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[COMPANY_FIRST_CATEGORY_COLUMN], contains_exactly("a"))


def test_process_features_should_extract_second_company_category():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company, some_company],
        HOMEPAGE_URL_COLUMN: [None, None],
        FUNDED_AT_AS_DATE_COLUMN: [date(1970, 1, 10), date(1970, 1, 10)],
        FIRST_FUNDING_AT_COLUMN: [None, None],
        COMPANY_CATEGORY_LIST_COLUMN: ["a|b|c", "a"],
        INVESTOR_NAME_COLUMN: ["investor_name", "investor_name"],
        COUNTRY_CODE_COLUMN: [None, None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None, None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[COMPANY_SECOND_CATEGORY_COLUMN], contains_exactly("b", DEFAULT_CATEGORICAL_FEATURE_VALUE))


def test_process_features_should_extract_third_company_category():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company, some_company],
        HOMEPAGE_URL_COLUMN: [None, None],
        FUNDED_AT_AS_DATE_COLUMN: [date(1970, 1, 10), date(1970, 1, 10)],
        FIRST_FUNDING_AT_COLUMN: [None, None],
        COMPANY_CATEGORY_LIST_COLUMN: ["a|b|c", "a"],
        INVESTOR_NAME_COLUMN: ["investor_name", "investor_name"],
        COUNTRY_CODE_COLUMN: [None, None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None, None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[COMPANY_THIRD_CATEGORY_COLUMN], contains_exactly("c", DEFAULT_CATEGORICAL_FEATURE_VALUE))


def test_process_features_should_extract_fourth_company_category():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company, some_company],
        HOMEPAGE_URL_COLUMN: [None, None],
        FUNDED_AT_AS_DATE_COLUMN: [date(1970, 1, 10), date(1970, 1, 10)],
        FIRST_FUNDING_AT_COLUMN: [None, None],
        COMPANY_CATEGORY_LIST_COLUMN: ["a|b|c|d", "a"],
        INVESTOR_NAME_COLUMN: ["investor_name", "investor_name"],
        COUNTRY_CODE_COLUMN: [None, None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None, None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[COMPANY_FOURTH_CATEGORY_COLUMN], contains_exactly("d", DEFAULT_CATEGORICAL_FEATURE_VALUE))


def test_process_features_should_extract_fifth_company_category():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company, some_company],
        HOMEPAGE_URL_COLUMN: [None, None],
        FUNDED_AT_AS_DATE_COLUMN: [date(1970, 1, 10), date(1970, 1, 10)],
        FIRST_FUNDING_AT_COLUMN: [None, None],
        COMPANY_CATEGORY_LIST_COLUMN: ["a|b|c|d|e", "a"],
        INVESTOR_NAME_COLUMN: ["investor_name", "investor_name"],
        COUNTRY_CODE_COLUMN: [None, None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None, None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[COMPANY_FIFTH_CATEGORY_COLUMN], contains_exactly("e", DEFAULT_CATEGORICAL_FEATURE_VALUE))


def test_process_features_should_create_concatenation_of_investor_name_and_company_category():
    # The model will use this feature to evaluate the investor success rate when investing in startups of this category
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company],
        HOMEPAGE_URL_COLUMN: [None],
        FUNDED_AT_AS_DATE_COLUMN: [date(1970, 1, 10)],
        FIRST_FUNDING_AT_COLUMN: [None],
        COMPANY_CATEGORY_LIST_COLUMN: ["company_cagegory_1|company_category_2"],
        INVESTOR_NAME_COLUMN: ["investor_name"],
        COUNTRY_CODE_COLUMN: [None],
        INVESTOR_COUNTRY_CODE_COLUMN: [None]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[EXPERIENCE_IN_FIRST_CATEGORY_COLUMN], contains_exactly("investor_name-company_cagegory_1"))


def test_process_features_should_add_indicator_if_company_is_in_the_same_country_than_investor():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company, some_company],
        HOMEPAGE_URL_COLUMN: [None, None],
        FUNDED_AT_AS_DATE_COLUMN: [date(1970, 1, 10), date(1970, 1, 10)],
        FIRST_FUNDING_AT_COLUMN: [None, None],
        COMPANY_CATEGORY_LIST_COLUMN: ["", ""],
        INVESTOR_NAME_COLUMN: ["investor_name", "investor_name"],
        COUNTRY_CODE_COLUMN: ["FR", "FR"],
        INVESTOR_COUNTRY_CODE_COLUMN: ["FR", "US"]
    })

    # When
    processed_df = _process_features(input_df)

    # Then
    assert_that(processed_df[IS_INVESTOR_COUNTRY_SAME_AS_COMPANY_S], contains_exactly(FLAG_TRUE, FLAG_FALSE))


def test_add_organization_information_should_add_social_media_organization_infos():
    # Given
    some_company = "some_company"
    other_company = "other_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company, other_company],
    })
    organizations_info = pd.DataFrame({
        NAME_COLUMN: [some_company, other_company],
        "facebook_url": ["www.facebook.com", None],
        "twitter_url": [None, "www.twitter.com"],
        "linkedin_url": ["www.linkedin.com", None],
    })

    # When
    df_with_organizations_info = _add_organization_information(input_df, organizations_info)

    # Then
    assert_that(df_with_organizations_info[HAS_FACEBOOK_COLUMN], contains_exactly(FLAG_TRUE, FLAG_FALSE))
    assert_that(df_with_organizations_info[HAS_TWITTER_COLUMN], contains_exactly(FLAG_FALSE, FLAG_TRUE))
    assert_that(df_with_organizations_info[HAS_LINKEDIN_COLUMN], contains_exactly(FLAG_TRUE, FLAG_FALSE))


def test_add_people_information_should_add_people_information():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company],
    })
    people_df = pd.DataFrame({
        'Organization Name': [some_company, some_company],
        'Full Name': ['John Doe', 'John Smith'],
        'Number of News Articles': [2, 4],
        'Number of Founded Organizations': [2, 4],
        'Number of Portfolio Companies': [2, 4],
        'Number of Investments': [2, 4],
        'Number of Partner Investments': [2, 4],
        'Number of Lead Investments': [2, 4],
        'Number of Exits': [2, 4],
        'Number of Events': [2, 4]
    })

    # When
    df_with_people_info = _add_people_information(input_df, people_df)

    # Then
    assert_that(df_with_people_info['count_employee_in_crunchbase'], contains_exactly(2))
    for people_information_column in PEOPLE_INFORMATION_PARSED_NAME_COLUMNS:
        assert_that(df_with_people_info[f'min_{people_information_column}'], contains_exactly(2))
        assert_that(df_with_people_info[f'max_{people_information_column}'], contains_exactly(4))
        assert_that(df_with_people_info[f'mean_{people_information_column}'], contains_exactly(3))


def test_add_people_information_should_fill_info_with_none_if_no_info():
    # Given
    some_company = "some_company"
    input_df = pd.DataFrame({
        COMPANY_NAME_COLUMN: [some_company],
    })
    people_df = pd.DataFrame({
        'Organization Name': [],
        'Full Name': [],
        'Number of News Articles': [],
        'Number of Founded Organizations': [],
        'Number of Portfolio Companies': [],
        'Number of Investments': [],
        'Number of Partner Investments': [],
        'Number of Lead Investments': [],
        'Number of Exits': [],
        'Number of Events': []
    })

    # When
    df_with_people_info = _add_people_information(input_df, people_df)

    # Then
    assert_that(df_with_people_info['count_employee_in_crunchbase'], contains_exactly(0))
    for people_information_column in PEOPLE_INFORMATION_PARSED_NAME_COLUMNS:
        assert_that(df_with_people_info[f'min_{people_information_column}'], contains_exactly(FLAG_NO_PEOPLE_INFO))
        assert_that(df_with_people_info[f'max_{people_information_column}'], contains_exactly(FLAG_NO_PEOPLE_INFO))
        assert_that(df_with_people_info[f'mean_{people_information_column}'], contains_exactly(FLAG_NO_PEOPLE_INFO))


def test_parse_people_information():
    # Given
    people_df = pd.DataFrame({
        'Number of News Articles': ["0", "1", "1,234", None, 'Toto'],
        'Number of Founded Organizations': ["0", "1", "1,234", None, 'Toto'],
        'Number of Portfolio Companies': ["0", "1", "1,234", None, 'Toto'],
        'Number of Investments': ["0", "1", "1,234", None, 'Toto'],
        'Number of Partner Investments': ["0", "1", "1,234", None, 'Toto'],
        'Number of Lead Investments': ["0", "1", "1,234", None, 'Toto'],
        'Number of Exits': ["0", "1", "1,234", None, 'Toto'],
        'Number of Events': ["0", "1", "1,234", None, 'Toto']
    })

    # When
    parsed_people_info = _parse_people_information(people_df)

    # Then
    for people_information_column in PEOPLE_INFORMATION_COLUMNS:
        assert_that(parsed_people_info[people_information_column], contains_exactly(0, 1, 1234, 0, 0))
