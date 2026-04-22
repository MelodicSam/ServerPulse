#!/usr/bin/env bash
set -e

python -m flask --app app.main run --host=0.0.0.0 --port=5000
