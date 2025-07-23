#!/bin/bash

# Build script for deployment
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up Python path..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "Build completed successfully!"
