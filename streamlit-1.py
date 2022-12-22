import streamlit as st
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objs as go


# Read the CSV file
df = pd.read_csv('/Users/fatinamanimohdali/Downloads/rims.csv')
del df["Unnamed: 0"]

st.title("Trend 2022")
# Create the first dropdown to select between 'parliament' and 'dun'
level = st.selectbox('Select Level:', ['parliament', 'dun'])
# Create the second dropdown to select a specific parliament or dun
code = st.selectbox('Select Area:', df[level + 'Name'].unique().tolist())
# Create the third dropdown to select a specific DM
dm = st.selectbox('Select DM:', df[df[level + 'Name'] == code]['DM'].unique().tolist())
# Filter the data frame based on the selected DM and display the resulting data frame using st.dataframe()
dfori = df[(df[level + 'Name'] == code) & (df['DM'] == dm)]
dfori = dfori.sort_values('date')
st.dataframe(dfori)

# Create a regular expression pattern to match the desired column names
pattern = r'[A-Z]+_voteCount'
# Use the `filter` function and the `re.match` function to filter the column names
column_names = filter(lambda x: re.match(pattern, x), dfori.columns)
column_names_filtered = [column_name for column_name in filter(lambda x: re.match(pattern, x), dfori.columns) if dfori[column_name].notnull().any()]

# Create a list of dictionaries representing the data for each trace in the chart
traces = []
for column_name in column_names_filtered:
    trace = {
        'x': dfori['date'],
        'y': dfori[column_name],
        'name': column_name,
        'type': 'scatter',
        'mode': 'lines+markers',
        'text': dfori['DM'],
        'hovertext': '<br>' + "Details" + '<br>' + "Date: " + dfori['date'] + '<br>' + "DM: " + dfori['DM'] + '<br>' + column_name + ': ' + dfori[column_name].astype(str),
        'hoverlabel': {
            'namelength': -1,
            'font': {
                'size': 20
            }
        }
    }
    traces.append(trace)

# Use the `go.Figure` function from `plotly` to create the chart figure
figure = go.Figure(data=traces, layout={
    'title': {'text': 'Vote Count by Date'},
    'xaxis': {'title': 'Date'},
    'yaxis': {'title': 'Vote Count'}
})

# Use the `st.plotly_chart` function to display the chart in Streamlit
st.plotly_chart(figure)
