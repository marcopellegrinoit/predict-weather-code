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
df = pd.read_csv('resources/forecast.csv', index_col=None)

#df_mapping = pd.read_csv('resources/weather_code_mapping.csv', index_col=None)
#df_mapping = df_mapping[['weather_code', 'weather_code_group']]
# Merge DataFrames on the 'weather_code' column
#df = pd.merge(df, df_mapping, left_on='weather_code_prediction', right_on='weather_code', how='left')
#df['weather_code_group_label'] = df['weather_code'].astype(str) + '-' + df['weather_code_group']

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
                           'weather_code_prediction':'Weather code',
                           'weather_code_group':'Weather'
                          }, inplace = True)


st.title('Weather Code Forecast for Stockholm')

st.dataframe(df_print, hide_index=True,)

# Define the base time-series chart.
def get_chart(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Evolution of Weather Code")
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date", axis=alt.Axis(labelAngle=-60)),  # Adjust labelAngle as needed
            y=alt.Y("weather_code_prediction:Q", title="Weather Code", scale=alt.Scale(domain=[1, 13]))
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
            y=alt.Y("weather_code_prediction:Q", title="Weather Code", scale=alt.Scale(domain=[1, 13])),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("weather_code_label", title="Weather code"),
                alt.Tooltip("weather_code_prediction", title="Weather code level"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

st.altair_chart(get_chart(df).interactive(),
    use_container_width=True)
