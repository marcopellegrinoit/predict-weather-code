#!/bin/bash

set -e

echo "Running training pipeline"
cd notebooks

jupyter nbconvert --to notebook --execute 3_weather_code_training_pipeline.ipynb

