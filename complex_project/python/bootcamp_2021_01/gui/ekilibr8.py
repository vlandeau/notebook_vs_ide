import logging.config
from typing import Optional, Union

import click
import dash
from click import UsageError
from pilotis_io.io import IoAPI
from pilotis_io.local.local_io_api import LocalIoApi
from pilotis_io.s3.s3_io_api import S3IoAPI

from bootcamp_2021_01.gui import options
from bootcamp_2021_01.gui.ekilibr8_state import Ekilibr8
from bootcamp_2021_01.gui.layout import layout

_logger = logging.getLogger("ekilibr8")
EXPORT_NAME = 'webapp_input'

BACKEND_CHOICE_LOCAL = 'local'
BACKEND_CHOICE_S3 = 'S3'

BACKEND_CHOICES = [
    BACKEND_CHOICE_LOCAL,
    BACKEND_CHOICE_S3
]

ENV_VAR_EKILIBR8_PORT = 'EKILIBR8_PORT'


@click.command()
@click.option(options.BACKEND.name, help=options.BACKEND.help_message, type=click.Choice(BACKEND_CHOICES),
              required=True)
@click.option(options.BUCKET_NAME.name, help=options.BUCKET_NAME.help_message, required=False)
@click.option(options.WORK_DIR.name, help=options.WORK_DIR.help_message, required=False)
@click.option(options.EXPORT_RUN_ID.name, help=options.EXPORT_RUN_ID.help_message, default='validation')
@click.option(options.PORT.name, help=options.PORT.help_message, type=int, envvar=ENV_VAR_EKILIBR8_PORT, default=8052)
def ekilibr8(port: int, export_run_id: str, work_dir: str, bucket_name: str, backend: str):
    """The Ekilibr8 all in one entry point"""

    maybe_api = io_api_factory(backend, work_dir, bucket_name)
    if isinstance(maybe_api, UsageError):
        raise maybe_api
    io_api: IoAPI = maybe_api

    start_dataviz(debug=True, host='0.0.0.0', port=port, io_api=io_api)


def io_api_factory(backend: str, work_dir: Optional[str], bucket_name: Optional[str]) -> Union[UsageError, IoAPI]:
    if backend == BACKEND_CHOICE_S3:
        if bucket_name is None:
            return click.BadOptionUsage(options.BUCKET_NAME.name,
                                        'A bucket must be provided when using S3 backend')
        else:
            return S3IoAPI(bucket_name)
    elif backend == BACKEND_CHOICE_LOCAL:
        if work_dir is None:
            return click.BadOptionUsage(options.WORK_DIR.name,
                                        'A working directory must be provided when using local backend')
        else:
            return LocalIoApi(work_dir)
    else:
        return click.BadOptionUsage(options.BACKEND.name, 'A valid backend must be selected')


def start_dataviz(debug: bool, host: str, port: int, io_api: IoAPI) -> None:
    state = Ekilibr8(io_api)

    app = dash.Dash(
        __name__,
        external_stylesheets=[],
    )
    app.layout = layout(state, app)
    app.run_server(host=host, port=port, debug=debug)


if __name__ == '__main__':
    ekilibr8()
