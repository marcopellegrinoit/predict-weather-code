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

df["temperature_min"] = df["temperature_min"].astype(int)
df["precipitation_sum"] = df["precipitation_sum"].astype(int)
df["wind_gusts_max"] = df["wind_gusts_max"].astype(int)

# Drop the index column if it exists
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

df_print = df[['date', 'temperature_min', 'precipitation_sum', 'wind_gusts_max', 'weather_code', 'weather_code_desc_short']]
df_print.temperature_min = df_print.temperature_min.round()
df_print.precipitation_sum = df_print.precipitation_sum.round()
df_print.wind_gusts_max = df_print.wind_gusts_max.round()
df_print.rename(columns = {'date':'Day',
                           'temperature_min':'Temperature Min [°C]',
                           'precipitation_sum':'Precipitation Sum [mm]',
                           'wind_gusts_max':'Wind Gusts Max [km/h]',
                           'weather_code':'Weather Code [1-13]',
                           'weather_code_desc_short':'Info'
                          }, inplace = True)

df_print = df_print.reindex(columns=['Day', 'Weather Code [1-13]', 'Info', 'Temperature Min [°C]', 'Precipitation Sum [mm]', 'Wind Gusts Max [km/h]'])

st.title('Stockholm Weather Code Forecast')

st.write(f"Author: [Marco Pellegrino](https://www.linkedin.com/in/marco-pellegrino-it/) - November 2023. Click here for [project explanation](https://github.com/marcopellegrinoit/predict-weather-code).")

st.divider()

st.write('Welcome to the Stockholm Weather Code Forecast! This web application provides a detailed weather code forecast for the next 14 days, using machine-learning predictions based on rain, wind, and temperature from [Open-Meteo](https://open-meteo.com/).')

# return the coloured row based on the weather code
def color_weather_code(row):
    val = row['Weather Code [1-13]']
    if val <= 2:
        color = 'rgba(144, 238, 144, 0.7)'  # Light Green with alpha 0.7
    elif val <= 6:
        color = 'rgba(255, 255, 0, 0.7)'  # Yellow with alpha 0.7
    elif val <= 9:
        color = 'rgba(255, 165, 0, 0.7)'  # Orange with alpha 0.7
    else:
        color = 'rgba(255, 0, 0, 0.7)'  # Red with alpha 0.7

    return ['background-color: ' + color] * len(row)

# print forecast
styled_df = df_print.style.apply(color_weather_code, axis=1)
#styled_df.format({'Temperature Min [°C]': '{:.0f}'})
#styled_df.format({'Precipitation Sum [mm]': '{:.0f}'})
#styled_df.format({'Wind Gusts Max [km/h]': '{:.0f}'})

#st.table(styled_df)

st.dataframe(styled_df)

st.write('Legend: weather codes range from 1 (clear sky: green) to 13 (thunderstorm: red).')

st.divider()

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
            y=alt.Y("weather_code:Q", title="Weather Code [1-13]", scale=alt.Scale(domain=[1, 13]))
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
            y=alt.Y("weather_code:Q", title="Weather Code [1-13]", scale=alt.Scale(domain=[1, 13])),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("weather_code_desc", title="Info"),
                alt.Tooltip("weather_code", title="Weather Code"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

st.write('Explore the forecast trend and gain insights into the upcoming weather conditions. You can use the provided visualization to make informed decisions based on the predicted weather patterns:')

st.altair_chart(get_chart(df).interactive(),
    use_container_width=True)

st.divider()

st.write('Developed in Python with [Hopsworks](https://www.hopsworks.ai/), [GitHub Actions](https://github.com/features/actions) and [Hugging Face](https://huggingface.co/).')

st.write('**Disclaimer**: This forecast is based on predictions and subject to change. Always refer to official sources for the latest weather updates.')

st.write('This project is distributed under the [GNU General Public License (GPL) version 3.0](https://www.gnu.org/licenses/gpl-3.0.html).')