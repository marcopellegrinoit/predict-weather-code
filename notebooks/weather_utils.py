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
    return openmeteo

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
    
    return df

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

    # Rename date column to avoid confusing with the other prediction date feature
    df = df.rename(columns={'date': 'forecast_date'})

    # Sort the DataFrame by a date
    df = df.sort_values(by='forecast_date')

    # Drop the first row because it is about yesterday (Open-Meteo first next day is still yesterday)
    df = df.iloc[1:]
    
    return df

def group_wmo_weather_codes(df):
    """
    For each day of the dataframe, add the new weather code based on the WMO weather code
    """
    
    # Given mapping between WMO codes and new codes
    df_codes_mapping = pd.read_csv("../resources/weather_code_mapping.csv")

    # Select useful columns
    df_codes_mapping = df_codes_mapping[['weather_code_wmo', 'weather_code']]

    # Create a dictionary to map WMO weather codes to group codes
    weather_mapping = {}
    for index, row in df_codes_mapping.iterrows():
        codes = [int(code) for code in row['weather_code_wmo'].split(',')]  # WMO codes need to be split into a list
        weather_code = row['weather_code']
        for code in codes:
            weather_mapping[code] = weather_code  # Removed unnecessary parentheses

    # Function to map WMO codes to new codes
    def map_weather_code_to_code_wmo(code):
        return weather_mapping.get(code, None)

    # Add new columns 'weather_code_label' and 'associated_code' based on the mapping
    df['weather_code'] = df['weather_code_wmo'].apply(map_weather_code_to_code_wmo)
    
    return df

def add_weather_code_labels(df):
    """
    For each day of the dataframe, add both a long and a short description of the weather code
    """
    
    # Add label of weather code
    df_codes_mapping = pd.read_csv("../resources/weather_code_mapping.csv")

    # Select useful columns
    df_codes_mapping = df_codes_mapping[['weather_code', 'weather_code_desc', 'weather_code_desc_short']]
    
    # Merge DataFrames on the 'weather_code' column
    df = pd.merge(df, df_codes_mapping, on='weather_code', how='left')
    
    return df