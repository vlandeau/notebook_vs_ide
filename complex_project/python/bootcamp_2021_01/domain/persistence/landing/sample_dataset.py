import pandas as pd
from ekinox_ds.directory_structure import dataset_raw_dir_path
from ekinox_ds.io import IoAPI
from ekinox_ds.persistence import LandingDataSourcePersistence

COLUMN_NAME_VALUE = "value"
COLUMN_NAME_ID = "id"


class SampleDatasetPersistence(LandingDataSourcePersistence):
    schema = {
        COLUMN_NAME_ID: int,
        COLUMN_NAME_VALUE: str
    }

    def __init__(self, infrastructure_api: IoAPI) -> None:
        super().__init__(infrastructure_api, 'sample_dataset')

    def load_raw(self, dataset_version: str = None) -> pd.DataFrame:
        dataset_files = self.infrastructure_api.list_files_in_dir(dataset_raw_dir_path(self.dataset_name,
                                                                                       dataset_version))
        return self.infrastructure_api.load_pandas_dataset(dataset_files, sep=",", header=0, dtype=self.schema)
