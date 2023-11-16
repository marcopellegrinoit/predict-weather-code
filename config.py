# HOPSWORKS

# 1) Feature Group about historical weather data
FG_HISTORG_NAME = 'weather_historical_fg'
FG_HISTORY_V = 1 # version
FG_HISTORY_PK = ["date"] # primary key
FG_HISTORY_DESC = 'Daily Weather Information' # description

# 2) Feature Group about forecast weather data
FG_FORECAST_NAME = 'weather_forecast_fg'
FG_FORECAST_V = 1 # version
FG_FORECAST_PK = ["date"] # primary key
FG_FORECAST_DESC = 'Daily Weather Forecast' # description

# 3) Feature View for historical weather data
FEATURE_VIEW_NAME = 'weather_fv'
FEATURE_VIEW_V = 1 # version

# MODEL
MODEL_NAME = 'weather_code_xgboost_model'
MODEL_METRIC = 'CV MSE mean'
OPTIMIZE_DIRECTION = 'min'
MODEL_PATH = 'weather_code_model'
N_FOLD_CV = 10 # number of folds for the k-fold Cross-Validation
LEARNING_RATE_RANGE = [0.01, 0.1, 0.2]
N_ESTIMATORS_RANGE = [50, 100, 200]
MAX_DEPTH_RANGE = [3, 5, 7]
SUBSAMPLE_RANGE = [0.8, 1.0]
COLSAMPLE_BYTREE_RANGE = [0.8, 1.0]

# Open-Meteo
BASELINE_URL_OPEN_METEO = 'https://api.open-meteo.com/v1/forecast'
TIMEZONE = 'Europe/Berlin'

# Stockholm coordinates
LATITUDE = '59.3294'
LONGITUDE = '18.0687'