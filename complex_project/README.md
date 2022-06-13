# bootcamp-2021-01

## What to do from here ?

First check that all tools are correctly installed and configured :
```bash
./scripts/check_tools.bash
```
Do not continue until you have no error.

Now you can install all dependencies
```bash
cd python
make setup-env-full
```

You are ready to go on your jupyter installation
```bash
make notebook
```

For all other automated commands, just run `make help` to see them :)

## Data Storage

For Data organization, everything should be stored in the `workdir` directory and respect the structure defined 
in the [notion documentation](https://www.notion.so/ekinox/Data-Structure-37ee5bbc31a14d9cb758d4d32d9d774c)

### Requirements

Every command that interact with AWS will use AWS credentials.
If you don't have any, please ask the infrastructure owner.
Set them using :
```bash
cd infrastructure
mkdir .secrets
cp set_ekinox_aws_credentials.bash.template .secrets/set_ekinox_aws_credentials.bash
chmod u+x .secrets/set_ekinox_aws_credentials.bash
vim .secrets/set_ekinox_aws_credentials.bash
source .secrets/set_ekinox_aws_credentials.bash 
```

### Synchronize DATA from AWS S3

To get raw data from s3, run
```bash
make sync-raw-data-s3-to-local
```

### Synchronize DATA to AWS S3

To send local raw data to s3, run
```bash
make sync-raw-data-local-to-s3
```

# Troubleshooting

## poetry could not be installed even if removed from path

Context :
- Poetry removed from path
- Trying to install poetry using `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

Observed error :
- Log saying poetry is already installed in the latest version event if this is not the case

How to fix :
```bash
mv ~/.poetry ~/.poetry.backup
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

## poetry issues an error about cleo

Usually, it happens when poetry has been upgraded from a version not compatible with the one that replaces it.

The solution is to uninstall and reinstall poetry :

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --uninstall
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
