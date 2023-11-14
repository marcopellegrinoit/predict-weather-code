#!/bin/bash

set -e

cd notebooks

echo "Running feature pipeline"

jupyter nbconvert --to notebook --execute 2_weather_code_feature_pipeline.ipynb

echo "Running training pipeline"

jupyter nbconvert --to notebook --execute 3_weather_code_training_pipeline.ipynb

echo "Running inference pipeline"

jupyter nbconvert --to notebook --4_weather_code_batch_inference.ipynb
