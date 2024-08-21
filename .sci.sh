#!/bin/sh
set -e

echo "setting up environment..."
uv venv
source .venv/bin/activate
uv pip install -e .[dev]

echo "checking..."
python3 -m ruff check
python3 -m ruff format --check --diff
python3 -m basedpyright

echo "testing..."
python3 -m coverage -m pytest tests

echo "building package..."
python3 -m build --outdir build/dist
