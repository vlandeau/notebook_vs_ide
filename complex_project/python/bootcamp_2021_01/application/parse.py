import click
from ekinox_ds.local.local_io_api import LocalIoApi
from ekinox_ds.parser import parse_dataset

from bootcamp_2021_01.domain.persistence.landing.sample_dataset import SampleDatasetPersistence


DATASET_PERSISTENCE = {
    'sample_dataset': SampleDatasetPersistence
}


@click.command(name="parse")
@click.option("--workdir")
@click.option("--dataset-name")
@click.option("--dataset-version")
def main(workdir: str, dataset_name: str, dataset_version: str) -> None:
    parse_dataset(DATASET_PERSISTENCE[dataset_name](LocalIoApi(workdir)), dataset_version)


if __name__ == '__main__':
    main()
