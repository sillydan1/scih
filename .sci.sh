#!/bin/sh
set -e
echo "checking if required environment is set..."
test -n "$DOCKER_TOKEN"

echo "setting up environment..."
uv venv
source .venv/bin/activate
uv pip install -e .[dev]

echo "checking..."
python3 -m ruff check
python3 -m ruff format --check --diff
python3 -m basedpyright

echo "testing..."
python3 -m coverage run -m pytest tests

echo "building package..."
python3 -m build --outdir build/dist

echo "building docker image..."
docker build -t scih:latest -t git.gtz.dk/agj/scih:latest -f .dockerfile .

echo "pushing latest docker image..."
# TODO: user should be some sci-bot or something, not your account. This will do for now though
docker login git.gtz.dk -u agj -p "$DOCKER_TOKEN"
docker push git.gtz.dk/agj/scih:latest
