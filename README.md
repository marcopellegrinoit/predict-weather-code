![GitHub](https://img.shields.io/badge/license-GPL--3.0-blue)

# Weather Code Prediction using Serverless ML Services

Marco Pellegrino - November 2023

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

### Backfill pipeline

### Feature Pipeline

### Training Pipeline

### Inference Pipeline

### Web App

## Usage

1.  Set up Howsworks account
2.  Set up GitHub Actions with the configuration files:
    1.  [`feature-pipeline-action.yml`](https://github.com/marcopellegrinoit/predict-weather-code/blob/main/.github/workflows/feature-pipeline-action.yml) to automate fetching new daily weather and inserting it into the Hopsworks feature store. 
    2.  ?? to automate training of the ML regression model with updated historical weather data

## Built with

*   [Hopsworks](https://www.hopsworks.ai/)
*   [GitHub Actions](https://github.com/features/actions)
*   [Streamlit](https://streamlit.io/) and [Hugging Face](https://huggingface.co/)

## License

This repository is licensed under the GNU General Public License v3.0 (GPL-3.0). For more details, see the [LICENSE](LICENSE) file.