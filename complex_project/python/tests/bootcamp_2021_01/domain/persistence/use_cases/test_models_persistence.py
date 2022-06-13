from pathlib import Path

from ekinox_ds.local.local_io_api import LocalIoApi
from hamcrest import assert_that
from hamcrest.core.core import is_, instance_of
from sklearn.tree import DecisionTreeClassifier

from bootcamp_2021_01.domain.persistence.use_cases.models_persistence import UseCasesModelPersistence
from bootcamp_2021_01.domain.use_cases import USE_CASE_NAME


def test_save_and_load_sklearn_model(tmp_path: Path):
    # Given
    model = DecisionTreeClassifier()
    model_name = 'test_model'
    model_run_id = 'some_run_id'
    io_api = LocalIoApi(str(tmp_path))
    model_persistence = UseCasesModelPersistence(io_api, USE_CASE_NAME, model_name)

    # When
    model_persistence.save_sklearn_model(model, model_run_id)

    # Then
    expected_model_file = tmp_path / "use_cases" / USE_CASE_NAME / "models" / model_name / model_run_id / "model.pkl"
    assert_that(expected_model_file.exists(), is_(True))

    # When
    restored_model = model_persistence.load_sklearn_model(model_run_id)

    # Then
    assert_that(restored_model, instance_of(DecisionTreeClassifier))
