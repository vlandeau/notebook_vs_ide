#!/usr/bin/env bash

set -e

BASEDIR=$(dirname "$0")
PYTHON_DIR="${BASEDIR}/../python"

TARGET_PYTHON_VERSION=3.7

echo "Checking that pyenv is correctly installed..."

if ! command -v pyenv > /dev/null;
then
  echo "pyenv is not installed"
  exit 1
else
  printf "\tpyenv installation: OK\n"
fi

if ! pyenv versions | grep ${TARGET_PYTHON_VERSION} > /dev/null;
then
  echo "No python version '${TARGET_PYTHON_VERSION}' installed. Install one using 'pyenv install'"
  exit 1
else
  printf "\tPython %s: OK\n" "${TARGET_PYTHON_VERSION}"
fi

if [ ! -f "${PYTHON_DIR}/.python-version" ]
then
  echo "Please configure a local pyenv version with 'pyenv local <3.7.X>' inside the 'python' directory"
  exit 1
else
  printf "\tPyenv local: OK\n"
fi

if ! grep ${TARGET_PYTHON_VERSION} "${PYTHON_DIR}/.python-version" > /dev/null
then
  echo "Python local version invalid. It must contain a ${TARGET_PYTHON_VERSION} version"
  exit 1
else
  printf "\tPyenv local content: OK\n"
fi

echo "Checking that poetry is correctly installed..."

if ! command -v poetry > /dev/null;
then
  echo "poetry is not installed"
  exit 1
else
  printf "\tPoetry installation: OK\n"
fi

echo "Checking that terraform is correctly installed..."

if ! command -v terraform > /dev/null;
then
  echo "terraform is not installed"
  exit 1
else
  printf "\tTerraform installation: OK\n"
fi

echo "Checking that AWS CLI is correctly installed..."

if ! command -v aws > /dev/null;
then
  echo "AWS CLI is not installed ; please follow this documentation: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"
  exit 1
else
  printf "\tAWS CLI installation: OK\n"
fi

echo "Congratulations ! Your environment is ready for work."
