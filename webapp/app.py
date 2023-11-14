import altair as alt
import pandas as pd
import streamlit as st
import hopsworks

# Connect to Hopsworks
project = hopsworks.login()
fs = project.get_feature_store()
dataset_api = project.get_dataset_api()

# download the forecast to the local environment
dataset_api.download('Resources/weather_forecast/forecast.csv', overwrite=True)

# Read CSV file without setting any column as the index
df = pd.read_csv('forecast.csv', index_col=None)

# Drop the index column if it exists
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

df_print = df[['date', 'temperature_min', 'precipitation_sum', 'wind_gusts_max', 'weather_code_prediction','weather_code_group']]
df_print.temperature_min = df_print.temperature_min.round()
df_print.precipitation_sum = df_print.precipitation_sum.round()
df_print.wind_gusts_max = df_print.wind_gusts_max.round()
df_print.rename(columns = {'date':'Day',
                           'temperature_min':'Temperature Min [°C]',
                           'precipitation_sum':'Precipitation Sum [mm]',
                           'wind_gusts_max':'Wind Gusts Max [km/h]',
                           'weather_code_prediction':'Weather Code [1-13]',
                           'weather_code_group':'Info'
                          }, inplace = True)

df_print = df_print.reindex(columns=['Day', 'Weather Code [1-13]', 'Info', 'Temperature Min [°C]', 'Precipitation Sum [mm]', 'Wind Gusts Max [km/h]'])

st.title('Weather Code Forecast for Stockholm')

# Set the hyperlink
open_meteo_link = "[Open-Meteo](https://open-meteo.com/)"

linkedin = "[Marco Pellegrino](https://www.linkedin.com/in/marco-pellegrino-it/)"

st.write(f"Data sourced from {open_meteo_link}.")

st.write(f"Author: {linkedin} - November 2023")

st.write('Weather code forecast for the next 14 days, based on Open-Meteo predictions about rain, wind and temperature.')

def color_weather_code(val):
    if val <= 2:
        color = 'rgba(144, 238, 144, 0.7)'  # Light Green with alpha 0.7
    elif val <= 6:
        color = 'rgba(255, 255, 0, 0.7)'  # Yellow with alpha 0.7
    elif val <= 9:
        color = 'rgba(255, 165, 0, 0.7)'  # Orange with alpha 0.7
    else:
        color = 'rgba(255, 0, 0, 0.7)'  # Red with alpha 0.7

    return f'background-color: {color}'

st.dataframe(df_print.style.applymap(color_weather_code, subset=['Weather Code [1-13]']))

#st.dataframe(df_print, hide_index=True,)

# Define the base time-series chart.
def get_chart(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Weather Code Trend")
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date", axis=alt.Axis(labelAngle=-60)),  # Adjust labelAngle as needed
            y=alt.Y("weather_code_prediction:Q", title="Weather Code [1-13]", scale=alt.Scale(domain=[1, 13]))
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x=alt.X("yearmonthdate(date):T", title="Date"),
            y=alt.Y("weather_code_prediction:Q", title="Weather Code [1-13]", scale=alt.Scale(domain=[1, 13])),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("weather_code_label", title="Info"),
                alt.Tooltip("weather_code_prediction", title="Weather Code"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

st.altair_chart(get_chart(df).interactive(),
    use_container_width=True)
