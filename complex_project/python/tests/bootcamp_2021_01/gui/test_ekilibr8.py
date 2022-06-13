import os
import shutil
from pathlib import Path
from typing import List

from click.testing import CliRunner
from hamcrest import assert_that, contains_string

from bootcamp_2021_01.gui.ekilibr8 import ekilibr8
from tests.bootcamp_2021_01.gui.timeout_manager import timeout

CLI_RUNNER_TIMEOUT = 3


def test_ekilibr8_should_start_on_local_fs(tmp_path: Path):
    # Given
    _generate_sample_data(tmp_path)
    ekilibr8_parameters = [
        '--backend', 'local',
        '--work-dir', str(tmp_path)
    ]

    # When
    with timeout(CLI_RUNNER_TIMEOUT):
        result = CliRunner().invoke(ekilibr8, ekilibr8_parameters, catch_exceptions=False)

    # Then
    assert_that(str(result.stdout), contains_string('Dash is running on http://0.0.0.0:8052/'))


def _generate_sample_data(tmp_path: Path) -> None:
    current_path = Path(__file__)
    local_model_path = current_path.parent.parent.parent / 'resources' / 'model.pkl'
    target_model_path = tmp_path / 'use_cases' / 'bootcamp-2021-01' / 'models' / 'cat_boost' / 'run_notebook' / 'model.pkl'
    target_model_path.parent.mkdir(parents=True)
    shutil.copy(str(local_model_path), str(target_model_path))

    notpeter_version = '2015-12'
    _create_data(tmp_path,
                 'notpeter_investments',
                 notpeter_version,
                 'investments.csv',
                 'company_permalink,company_name,company_category_list,company_country_code,company_state_code,company_region,company_city,investor_permalink,investor_name,investor_country_code,investor_state_code,investor_region,investor_city,funding_round_permalink,funding_round_type,funding_round_code,funded_at,raised_amount_usd\n',
                 [
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/organization/idinvest-partners,Idinvest Partners,FRA,A8,Paris,Paris,/funding-round/4f8424a894d409ff99e0618b66bd8d18,venture,,2015-02-10,4099999\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/organization/idinvest-partners,Idinvest Partners,FRA,A8,Paris,Paris,/funding-round/b18085a3c0ab2305d7837cd0f32543a3,venture,A,2011-05-30,3600000\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/organization/lerer-ventures,Lerer Hippeau Ventures,USA,NY,New York City,New York,/funding-round/dd4fe3d88022819da4b041de01e0118b,angel,B,2010-02-03,1000000\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/person/fabrice-grinda,Fabrice Grinda,USA,,,New York,/funding-round/8fa9c785699722cbf1010d7b393ea264,seed,,2010-05-10,\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/person/fabrice-grinda,Fabrice Grinda,USA,,,New York,/funding-round/dd4fe3d88022819da4b041de01e0118b,angel,,2010-02-03,1000000\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/person/jacques-antoine-granjon,Jacques-Antoine Granjon,,,,,/funding-round/dd4fe3d88022819da4b041de01e0118b,angel,,2010-02-03,1000000\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/person/jean-david-blanc,Jean-David Blanc,,,,,/funding-round/dd4fe3d88022819da4b041de01e0118b,angel,,2010-02-03,1000000\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/person/marc-simoncini,Marc Simoncini,FRA,,,Paris,/funding-round/dd4fe3d88022819da4b041de01e0118b,angel,,2010-02-03,1000000\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/person/xavier-niel,Xavier Niel,,,,,/funding-round/4f8424a894d409ff99e0618b66bd8d18,venture,,2015-02-10,4099999\n',
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/person/xavier-niel,Xavier Niel,,,,,/funding-round/dd4fe3d88022819da4b041de01e0118b,angel,,2010-02-03,1000000\n',
                 ])

    _create_data(tmp_path,
                 'notpeter_acquisitions',
                 notpeter_version,
                 'acquisitions.csv',
                 'company_permalink,company_name,company_category_list,company_country_code,company_state_code,company_region,company_city,acquirer_permalink,acquirer_name,acquirer_category_list,acquirer_country_code,acquirer_state_code,acquirer_region,acquirer_city,acquired_at,acquired_month,price_amount,price_currency_code\n',
                 [
                     '/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,/organization/mobile-network-group,Mobile Network Group,Apps,FRA,A1,FRA - Other,Franceau,2015-02-10,2015-02,30000000,USD\n',
                     '/organization/wittified-llc,"Wittified, LLC",Developer Tools,USA,WA,Seattle,Seattle,/organization/appsfire,Appsfire,Advertising|Android|iOS|Mobile|Promotional,FRA,A8,Paris,Paris,2015-09-10,2015-09,,USD\n',
                 ])

    _create_data(tmp_path,
                 'notpeter_companies',
                 notpeter_version,
                 'companies.csv',
                 'permalink,name,homepage_url,category_list,funding_total_usd,status,country_code,state_code,region,city,funding_rounds,founded_at,first_funding_at,last_funding_at\n',
                 [
                     '/organization/appsfire,Appsfire,http://appsfire.com,Advertising|Android|iOS|Mobile|Promotional,8699999,acquired,FRA,A8,Paris,Paris,4,2009-01-01,2010-02-03,2015-02-10\n'
                 ])

    _create_data(tmp_path,
                 'bachelorarbeit_organizations',
                 '2013-12-cleaned',
                 'cleaned_organizations.csv',
                 '"crunchbase_uuid","name","type","primary_role","crunchbase_url","homepage_domain","homepage_url","profile_image_url","facebook_url","twitter_url","linkedin_url","stock_symbol","location_city","location_region","location_country_code","short_description"\n',
                 [
                     '"53d8758a-710b-7144-4505-e3c339526c8b","Appsfire","organization","company","https://www.crunchbase.com/organization/appsfire?utm_source=crunchbase&utm_medium=export&utm_campaign=odm_csv","appsfire.com","http://appsfire.com","https://crunchbase-production-res.cloudinary.com/image/upload/c_lpad,h_120,w_120,f_jpg/v1397183125/c734c1fd6b1eb5fa59a5504328d1b62b.png","http://www.facebook.com/appsfire","http://twitter.com/appsfire","http://www.linkedin.com/company/appsfire.com",":","Paris","Ile-de-France","FR","Appsfire operates an advertising platform for application developers and advertisers."\n'
                 ])

    _create_data(tmp_path,
                 'vc_holy_grail_people',
                 'vc_holy_grail_cleaned',
                 'people.csv',
                 'Full Name,Full Name URL,Primary Job Title,Organization Name,Primary Organization URL,Location,CB Rank,First Name,Last Name,Gender,Biography,Twitter,LinkedIn,Facebook,Number of News Articles,Number of Founded Organizations,Number of Portfolio Companies,Number of Investments,Number of Partner Investments,Number of Lead Investments,Number of Exits,Number of Events,Trend Score (7 Days),Trend Score (30 Days),Trend Score (90 Days),,,,,,,,,\n',
                 [
                     'Mark Cuban,/person/mark-cuban,Owner,Dallas Mavericks,/organization/dallas-mavericks,"Dallas, Texas, United States",1,Mark,Cuban,Male,"Since the age of 12, Mark has been a natural businessman. Selling garbage bags door to door, the seed was planted early on for what would eventually become long-term success. After graduating from Indiana University - where he briefly owned the most popular bar in town - Mark moved to Dallas. After a dispute with an employer who wanted him to clean instead of closing an important sale, Mark created MicroSolutions, a computer consulting service. He went on to later sell MicroSolutions in 1990 to CompuServe. In 1995, Mark and long-time friend Todd Wagner came up with an internet based solution to not being able to listen to Hoosiers Basketball games out in Texas. That solution was Broadcast.com - streaming audio over the internet. In just four short years, Broadcast.com (then Audionet) would be sold to Yahoo for $5.6 billion dollars. Since his acquisition of the Dallas Mavericks in 2000, he has overseen the Mavs competing in the NBA Finals for the first time in franchise history in 2006 - and becoming NBA World Champions in 2011. They are currently listed as one of Forbes\' most valuable franchises in sports. In addition to the Mavs, Mark is chairman and CEO of AXS tv, one of ABC\'s ""Sharks"" on the hit show Shark Tank, and an investor in an ever-growing portfolio of businesses. He lives in Dallas with wife Tiffany, daughters Alexis and Alyssa, and son Jake.",http://twitter.com/mcuban,https://www.linkedin.com/in/mark-cuban-06a0755b,http://www.facebook.com/markcuban,"2,366",4,72,96,3,8,14,11,0,0,0,,,,,,,,,'
                 ])


def _create_data(tmp_path: Path, dataset_name: str, dataset_version: str, dataset_filename: str, header: str,
                 data: List[str]):
    dataset_directory = tmp_path / "landing" / "raw" / dataset_name / dataset_version
    dataset_directory.mkdir(parents=True)
    dataset_file = dataset_directory / dataset_filename
    with dataset_file.open('w') as file:
        file.write(header)
        for line in data:
            file.write(line)


def test_ekilibr8_should_start_on_local_fs_on_custom_dataset_version(tmp_path: Path):
    # Given
    export_run_id = 'some_run_id'
    _generate_sample_data(tmp_path)
    ekilibr8_parameters = [
        '--backend', 'local',
        '--work-dir', str(tmp_path),
        '--export-run-id', export_run_id
    ]

    # When
    with timeout(CLI_RUNNER_TIMEOUT):
        result = CliRunner().invoke(ekilibr8, ekilibr8_parameters, catch_exceptions=False)

    # Then
    assert_that(str(result.stdout), contains_string('Dash is running on http://0.0.0.0:8052/'))


def test_ekilibr8_should_start_on_local_fs_with_custom_port_using_cli_param(tmp_path: Path):
    # Given
    _generate_sample_data(tmp_path)
    custom_port = '8080'
    ekilibr8_parameters = [
        '--backend', 'local',
        '--work-dir', str(tmp_path),
        '--port', custom_port
    ]

    # When
    with timeout(CLI_RUNNER_TIMEOUT):
        result = CliRunner().invoke(ekilibr8, ekilibr8_parameters, catch_exceptions=False)

    # Then
    assert_that(str(result.stdout), contains_string(f'Dash is running on http://0.0.0.0:{custom_port}/'))


def test_ekilibr8_should_start_on_local_fs_with_custom_port_using_environment_variable(tmp_path: Path):
    # Given
    _generate_sample_data(tmp_path)
    custom_port = '8080'
    os.environ['EKILIBR8_PORT'] = custom_port
    ekilibr8_parameters = [
        '--backend', 'local',
        '--work-dir', str(tmp_path)
    ]

    # When
    with timeout(CLI_RUNNER_TIMEOUT):
        result = CliRunner().invoke(ekilibr8, ekilibr8_parameters, catch_exceptions=False)

    # Then
    assert_that(str(result.stdout), contains_string(f'Dash is running on http://0.0.0.0:{custom_port}/'))


def test_ekilibr8_should_not_start_on_local_fs_given_no_work_dir_provided():
    # Given
    ekilibr8_parameters = [
        '--backend', 'local',
    ]

    # When
    result = CliRunner().invoke(ekilibr8, ekilibr8_parameters, catch_exceptions=False)

    # Then
    stdout = str(result.stdout_bytes)
    assert_that(stdout, contains_string('A working directory must be provided when using local backend'))


def test_ekilibr8_should_not_start_on_s3_fs_given_no_bucket_name_provided():
    # Given
    ekilibr8_parameters = [
        '--backend', 'S3',
    ]

    # When
    result = CliRunner().invoke(ekilibr8, ekilibr8_parameters, catch_exceptions=False)

    # Then
    stdout = str(result.stdout_bytes)
    assert_that(stdout, contains_string('A bucket must be provided when using S3 backend'))


def test_ekilibr8_should_not_start_given_no_backend_provided():
    # Given
    ekilibr8_parameters = []

    # When
    result = CliRunner().invoke(ekilibr8, ekilibr8_parameters, catch_exceptions=False)

    # Then
    stdout = str(result.stdout_bytes)
    assert_that(stdout, contains_string('Missing option \'--backend\''))
