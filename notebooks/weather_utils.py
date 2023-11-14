import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry

def get_openmeteo_connection():
    """
    Setup the Open-Meteo API client with cache and retry on error
    """
    
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    return(openmeteo)

def process_weather_request(response):
    """
    Process the Open-Meteo response, formatting the data and returnin the correspondant Pandas dataframe.
    """
    
    # the order of variables needs to be the same as requested
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_min = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(3).ValuesAsNumpy()

    # arrange features into a Numpy array
    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["weather_code_wmo"] = daily_weather_code
    daily_data["temperature_min"] = daily_temperature_min
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["wind_gusts_max"] = daily_wind_speed_10m_max

    # transform table into Pandas dataframe
    df = pd.DataFrame(data = daily_data)

    # Format date column to include only the day
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    return(df)

def process_forecast_request(response):
    """
    Process the Open-Meteo response, formatting the data and returnin the correspondant Pandas dataframe.
    """
    
    # the order of variables needs to be the same as requested
    daily = response.Daily()
    daily_temperature_min = daily.Variables(0).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(1).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(2).ValuesAsNumpy()

    # arrange features into a Numpy array
    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["temperature_min"] = daily_temperature_min
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["wind_gusts_max"] = daily_wind_speed_10m_max

    # transform table into Pandas dataframe
    df = pd.DataFrame(data = daily_data)

    # Format date column to include only the day
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    return(df)

def group_wmo_weather_codes(df):
    """
    To each day of the dataframe, add the name of the WMO weather group and a more compact group ID using the mapping provided in the API documentation.
    """
    
    # Group WMO codes into labels and new group code label
    df_weather_mapping = pd.read_csv("../resources/weather_code_mapping.csv")

    # Create a dictionary to map weather codes to labels and group codes
    weather_mapping = {}
    for index, row in df_weather_mapping.iterrows():
        codes = [int(code) for code in row['weather_code_wmo'].split(',')] # WMO codes need to be split into a list
        label = row['weather_code_label']
        weather_code = row['weather_code']
        for code in codes:
            weather_mapping[code] = (label, weather_code)

    # Function to map WMO codes to labels and group codes
    def map_weather_code_to_label_and_code(code):
        mapping = weather_mapping.get(code, None)
        if mapping:
            label, weather_code = mapping
            return label, weather_code
        else:
            return None, None

    # Add new columns 'weather_code_label' and 'associated_code' based on the mapping
    df['weather_code_label'], df['weather_code'] = zip(*df['weather_code_wmo'].apply(map_weather_code_to_label_and_code))
    
    return(df)