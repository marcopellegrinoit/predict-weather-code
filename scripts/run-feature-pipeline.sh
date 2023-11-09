#!/bin/bash

set -e

echo "Running feature pipeline"
cd notebooks

jupyter nbconvert --to notebook --execute 2_weather_code_feature_pipeline.ipynb

