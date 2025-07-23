#!/bin/bash

# Start script for deployment
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn app:app --host=0.0.0.0 --port=${PORT:-8000}
