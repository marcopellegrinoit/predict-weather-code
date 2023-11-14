import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('resources/forecasts.csv')

# Streamlit App
st.title('Weather Predictions for the Next 14 Days')

# Display DataFrame
st.write('## Weather Data')
st.dataframe(df)

# Line chart to visualize weather predictions
fig = px.line(df, x='date', y='weather_code_prediction', title='Weather Predictions for the Next 14 Days',
              labels={'weather_code_label': 'Weather Code'})
st.plotly_chart(fig)

# Bar chart to show the distribution of weather codes
bar_fig = px.bar(df, x='weather_code_prediction', title='Distribution of Weather Codes',
                 labels={'weather_code_label': 'Weather Code', 'count': 'Frequency'})
st.plotly_chart(bar_fig)
