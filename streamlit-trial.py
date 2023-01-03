import streamlit as st
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objs as go
import os
import textwrap


# Read the CSV file
df = pd.read_csv('/Users/fatinamanimohdali/Downloads/rims.csv')
del df["Unnamed: 0"]

st.title("Trend 2022")
level = st.selectbox('Select Level:', df['parliamentordun'].unique().tolist())
dfori = df[df['parliamentordun'] == level]
st.dataframe(dfori)

pattern = r'[A-Z]+_voteCount'
column_names = filter(lambda x: re.match(pattern, x), dfori.columns)
column_names_filtered = [column_name for column_name in filter(lambda x: re.match(pattern, x), dfori.columns) if dfori[column_name].notnull().any()]
df_totals = dfori.groupby('date')[list(column_names_filtered)].sum()
df_totals = df_totals.reset_index()
df_totals = df_totals.rename({'date': 'Date'}, axis=1)

traces = []
for column_name in column_names_filtered:
    hovertext = '<br>' + "Details" + '<br>' + "Date: " + dfori['date'] + '<br>' + "DM: " + dfori['DM'] + '<br>' + column_name + ': ' + dfori[column_name].astype(str)
    dfori[column_name] = pd.to_numeric(dfori[column_name], downcast='integer')
    trace = {
        'x': df_totals['Date'],
        'y': df_totals[column_name],
        'name': column_name,
        'type': 'scatter',
        'mode': 'lines+markers',
        'hovertext': hovertext,
        'hoverlabel': {
            'namelength': -1,
            'font': {
                'size': 20
            }
        },
        'hovertemplate': '%{hovertext}<extra></extra>'
    }
    traces.append(trace)

figure = go.Figure(data=traces, layout={
    'title': {'text': 'Vote Count by Date'},
    'xaxis': {'title': 'Date'},
    'yaxis': {'title': 'Vote Count'}
})

st.plotly_chart(figure)

# Create a list of dictionaries representing the data for each trace in the chart
traces = []
merged_dfs = []
folder = '/Users/fatinamanimohdali/Documents/RIMS/14Dec2022_new/justifi/'
for filename in dfori['filename']:
    if filename in [os.path.basename(file) for file in os.listdir(folder)]:
        df1 = pd.read_csv(folder + filename)
        merged_dfs.append(df1)
    merged_df = pd.concat(merged_dfs, ignore_index=True)
    merged_df = merged_df[['justification','date']].reindex(columns=['date', 'justification'])
    merged_df['justification'] = merged_df['justification']
st.table(merged_df)
