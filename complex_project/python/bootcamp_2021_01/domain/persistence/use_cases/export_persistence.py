import pandas as pd
from ekinox_ds.directory_structure import export_dir_path
from ekinox_ds.io import IoAPI


class UseCaseExportPersistence:
    def __init__(
            self,
            io_api: IoAPI,
            use_case_name: str,
            export_name: str,
            export_file_name: str,
    ):
        self.io_api = io_api
        self.use_case_name = use_case_name
        self.export_name = export_name
        self.export_file_name = export_file_name

    def export_pandas_dataframe(self, dataset: pd.DataFrame, run_id: str):
        self.io_api.save_pandas_dataset(dataset, self._export_path(run_id))

    def reload_pandas_export(self, run_id: str) -> pd.DataFrame:
        return self.io_api.load_pandas_dataset([self._export_path(run_id)])

    def _export_path(self, run_id):
        return export_dir_path(self.use_case_name, self.export_name, run_id) / self.export_file_name
