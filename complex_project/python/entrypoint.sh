#!/bin/bash
set -e

env_full_path=$(poetry env list --full-path | cut -d' ' -f1)
source ${env_full_path}/bin/activate

exec "$@"