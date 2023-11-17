![GitHub](https://img.shields.io/badge/license-GPL--3.0-blue) [![pipelines workflow](https://github.com/marcopellegrinoit/predict-weather-code/actions/workflows/pipelines-action.yml/badge.svg)](https://github.com/marcopellegrinoit/predict-weather-code/actions/workflows/pipelines-action.yml)



# Weather Code Prediction using Serverless ML Services

Author: Marco Pellegrino - November 2023

Click [here](https://huggingface.co/spaces/marcopellegrino/predict-weather-code) to access the webapp!

## Table of Contents

1.  [Description](#description)
2.  [Data Sources](#data-sources)
3.  [Architecture](#architecture)
4.  [Usage](#usage)
5.  [Built with](#built-with)
6.  [License](#license)

## Description

## Data Sources

The weather data, including both historical records and daily updates, is sourced from [Open-Meteo](https://open-meteo.com/en/docs).

Retrieved features for each day:

*   Weather code: weather conditions as a numeric code and categorized by [WMO mapping](resources/weather_code_mapping.csv)
*   Minimum temperature reached during the day, in °C
*   Sum of daily precipitation, in mm
*   Maximum gusts speed on the day, in km/h

## Architecture

### 1. Backfill pipeline
[Source code](notebooks/1_weather_code_feature_backfill.ipynb)

### 2. Feature Pipeline
[Source code](notebooks/2_weather_code_feature_pipeline.ipynb)

### 3. Training Pipeline
[Source code](notebooks/3_weather_code_training_pipeline.ipynb)

### 4. Inference Pipeline
[Source code](notebooks/4_weather_code_batch_inference.ipynb)

### 5. Web App
[Source code](webapp/app.py)

## Usage

1.  Set up [Howsworks account](https://app.hopsworks.ai/)
2.  Set up GitHub Actions with the [`feature-pipeline-action.yml`](.github/workflows/pipelines-action.yml) configuration files. It automates the feature, training, and inference pipelines one after the other.
3.  Run web app locally: `cd webapp` and `python -m streamlit run app.py`, or deploy it on [Hugging Face](https://huggingface.co/)

## Built with

*   [Hopsworks](https://www.hopsworks.ai/)
*   [GitHub Actions](https://github.com/features/actions)
*   [Streamlit](https://streamlit.io/) and [Hugging Face](https://huggingface.co/)

## License

This repository is licensed under the GNU General Public License v3.0 (GPL-3.0). For more details, see the [LICENSE](LICENSE) file.
