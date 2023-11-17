![GitHub](https://img.shields.io/badge/license-GPL--3.0-blue) [![pipelines workflow](https://github.com/marcopellegrinoit/predict-weather-code/actions/workflows/pipelines-action.yml/badge.svg)](https://github.com/marcopellegrinoit/predict-weather-code/actions/workflows/pipelines-action.yml)


# Weather Code Prediction using Serverless ML Services

Author: Marco Pellegrino - November 2023

## Overview

This project uses Python and Hopsworks to forecast the weather code for Stockholm based on historical weather data. The predictive model, trained using machine learning techniques, provides public access to its forecasts through a user-friendly [web application](https://huggingface.co/spaces/marcopellegrino/predict-weather-code).

## Table of Contents

1.  [Description](#description)
2.  [Data Sources](#data-sources)
3.  [Architecture](#architecture)
4.  [Usage](#usage)
5.  [Built with](#built-with)
6.  [License](#license)

## Description

This project aims to forecast the daily weather code for Stockholm, utilizing key meteorological factors such as minimum temperature, precipitation sum, and maximum gust speed. The selection of these features is informed by an intuitive understanding of the factors that influence weather conditions.

The project workflow involves the following steps in order:

1. [Historical Data Collection](#1-backfill-pipeline): Historical weather data is initially retrieved.

2. [Daily Data Collection](#2-feature-pipeline): Every day, the weather information of the previous day is collected.

3. [Machine Learning Model Training](#3-training-pipeline): With the updated data, a new machine learning model is trained and stored in the collection of trained models.

4. [Weather Code Forecast](#4-inference-pipeline): Minimum temperature, precipitation sum, and maximum gust speed for the next 14 days are collected and used as model features. Using the best-trained model, a weather code forecast is generated for the upcoming 2 weeks.

This iterative process ensures that the predictive model adapts to the latest data, enhancing the accuracy of the weather forecasts over time.

## Data Sources

The weather data, including historical records, daily updates, and forecast features is sourced from [Open-Meteo](https://open-meteo.com/en/docs).

Retrieved features for each day:

*   Weather code: weather conditions as a numeric code and categorized by [WMO mapping](resources/weather_code_mapping.csv)
*   Minimum temperature reached during the day, in °C
*   Sum of daily precipitation, in mm
*   Maximum gusts speed on the day, in km/h

## Architecture

![Achitecture diagram](diagram.png)

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

1.  Install the required dependencies: `pip install -r requirements.txt`
2.  Set up [Howsworks account](https://app.hopsworks.ai/)
3.  Set up GitHub Actions with the [`feature-pipeline-action.yml`](.github/workflows/pipelines-action.yml) configuration files. It automates the feature, training, and inference pipelines one after the other.
4.  Run web app locally: `cd webapp` and `python -m streamlit run app.py`, or deploy it on [Hugging Face](https://huggingface.co/)

## Built with

*   [Hopsworks](https://www.hopsworks.ai/)
*   [GitHub Actions](https://github.com/features/actions)
*   [Streamlit](https://streamlit.io/) and [Hugging Face](https://huggingface.co/)

## License

This repository is licensed under the GNU General Public License v3.0 (GPL-3.0). For more details, see the [LICENSE](LICENSE) file.
