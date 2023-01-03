import streamlit as st
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objs as go
import textwrap
import requests

# Replace link_to_file with the link to the file on the cloud storage service
link_to_file = 'https://drive.google.com/file/d/1GRvX-muzQXwC5njqugA5iQPHbUI34VYn/view?usp=share_link'

# Use the requests library to download the file from the cloud storage service
response = requests.get(link_to_file)

#df = pd.read_csv('/Users/fatinamanimohdali/Downloads/rims.csv')
df = pd.read_csv(response.content)
del df["Unnamed: 0"]

st.title("Trend 2022")
level = st.selectbox('Select Level:', ['parliament', 'dun'])
code = st.selectbox('Select Area:', df[level + 'Name'].dropna().unique().tolist())
dfori = df[df[level + 'Name'] == code]
pattern = r'[A-Z]+_voteCount'
column_names = filter(lambda x: re.match(pattern, x), dfori.columns)
column_names_filtered = [column_name for column_name in filter(lambda x: re.match(pattern, x), dfori.columns) if dfori[column_name].notnull().any()]

df_totals = dfori.groupby(['filename','date'])[list(column_names_filtered)].sum()
df_totals = df_totals.reset_index()
df_totals = df_totals.rename({'date': 'Date'}, axis=1)
traces = []
for column_name in column_names_filtered:
    df_totals[column_name] = pd.to_numeric(df_totals[column_name], downcast='integer')
    trace = {
        'x': df_totals['Date'],
        'y': df_totals[column_name],
        'name': column_name,
        'type': 'scatter',
        'mode': 'lines+markers',
        'hovertext': '<br>' + "Details" + '<br>' + "Date: " + df_totals['Date'] + '<br>' + column_name + ': ' + df_totals[column_name].astype(str),
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
    'xaxis': {'title': 'Date', 'showgrid': False},
    'yaxis': {'title': 'Vote Count', 'showgrid': False}
})
st.plotly_chart(figure)

###########

def wrap_justification(text):
   return '<br>'.join(textwrap.wrap(text, width=60))

# Create a list of dictionaries representing the data for each trace in the chart
traces = []
merged_dfs = []
folder = '/Users/fatinamanimohdali/Documents/RIMS/14Dec2022_new/justifi/'
for filename in df_totals['filename']:
    if filename in [os.path.basename(file) for file in os.listdir(folder)]:
        df1 = pd.read_csv(folder + filename)
        merged_dfs.append(df1)
    merged_df = pd.concat(merged_dfs, ignore_index=True)
    merged_df = merged_df[['justification','date']].reindex(columns=['date', 'justification'])
    merged_df['justification'] = merged_df['justification']
st.table(merged_df)
