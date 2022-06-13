from pathlib import Path

import joblib
from pilotis_io.directory_structure import model_dir_path
from pilotis_io.io import IoAPI
from sklearn.base import BaseEstimator


class UseCasesModelPersistence:
    def __init__(
            self, io_api: IoAPI, use_case_name: str, model_name: str
    ) -> None:
        self.io_api = io_api
        self.use_case_name = use_case_name
        self.model_name = model_name

    def save_sklearn_model(
            self, model: BaseEstimator, run_id: str, file_name: str = "model.pkl"
    ):
        model_local_copy_path: Path = Path("model.pkl")
        joblib.dump(model, model_local_copy_path)

        self.io_api.store_file(
            local_file_path=model_local_copy_path,
            relative_output_path=model_dir_path(
                self.use_case_name, self.model_name, run_id
            ) / file_name,
        )

    def load_sklearn_model(
            self, run_id: str, file_name: str = "model.pkl"
    ) -> BaseEstimator:
        model_local_copy_path: Path = Path("model.pkl")
        if model_local_copy_path.is_symlink():
            model_local_copy_path.unlink()

        self.io_api.copy_or_symlink_to_local(
            relative_target_path=model_dir_path(
                self.use_case_name, self.model_name, run_id
            ) / file_name,
            local_path=model_local_copy_path,
        )

        model = joblib.load(model_local_copy_path.resolve())
        model_local_copy_path.unlink()
        return model
