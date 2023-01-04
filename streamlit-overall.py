import streamlit as st
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objs as go
import textwrap
import requests
import base64
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

url = "https://github.com/AmaniAli95/streamlit-rims/raw/main/rims.csv"
response = requests.get(url)

#df = pd.read_csv('/Users/fatinamanimohdali/Downloads/rims.csv')
df = pd.read_csv(url)
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

url1 = "https://api.github.com/repos/AmaniAli95/streamlit-rims/contents/justification/folder1"
responseq = requests.get(url1)
filesq = responseq.json()
st.write(filesq)

subfolders = ['folder1', 'folder2', 'folder3', 'folder4', 'folder5']
url = "https://api.github.com/repos/AmaniAli95/streamlit-rims/contents/justification"
merged_dfs = []
for filename in df_totals['filename']:
    st.write(filename)
    for subfolder in subfolders:
        subfolder_url = f"{url}/{subfolder}" 
        st.write(subfolder_url)
        response = requests.get(subfolder_url)
        subfolder_files = response.json()
        st.write(subfolder_files)
        for file in subfolder_files:
            if file['name'] == filename:
                file_obj = file
                url1 = file_obj['html_url']
                raw_url = url1.replace("/blob/", "/raw/")
                df1 = pd.read_csv(raw_url)
                merged_dfs.append(df1)
            merged_df = pd.concat(merged_dfs, ignore_index=True)
            merged_df = merged_df[['justification','date']].reindex(columns=['date', 'justification'])
st.table(merged_df)
        
        #file_obj = next((file for file in subfolder_files if file['name'] == filename), None)
        #if file_obj is not None:
         #   url1 = file_obj['html_url']
          #  raw_url = url1.replace("/blob/", "/raw/")
           # df1 = pd.read_csv(raw_url)
            #merged_dfs.append(df1)
            #merged_df = pd.concat(merged_dfs, ignore_index=True)
            #merged_df = merged_df[['justification','date']].reindex(columns=['date', 'justification'])
#st.table(merged_df)



#url = "https://api.github.com/repos/AmaniAli95/streamlit-rims/contents/justifi"
#response = requests.get(url)
#files = response.json()
#merged_dfs = []

#for filename in df_totals['filename']:
#    # Find the file object with a matching name in the files list
#    file_obj = next((file for file in files if file['name'] == filename), None)
#    # If a matching file was found, read it and append it to the merged_dfs list
#    if file_obj is not None:
#        url1 = file_obj['html_url']
#        raw_url = url1.replace("/blob/", "/raw/")
#        df1 = pd.read_csv(raw_url)
#        merged_dfs.append(df1)
# Concatenate all the dataframes and display the table
#    merged_df = pd.concat(merged_dfs, ignore_index=True)
#    merged_df = merged_df[['justification','date']].reindex(columns=['date', 'justification'])
#st.table(merged_df)




#folder = '/workspaces/streamlit-rims/justifi'
#for filename in df_totals['filename']:
#    if filename in [os.path.basename(file) for file in files]:
#        df1 = pd.read_csv(folder + filename)
#        merged_dfs.append(df1)
#    merged_df = pd.concat(merged_dfs, ignore_index=True)
#    merged_df = merged_df[['justification','date']].reindex(columns=['date', 'justification'])
#    merged_df['justification'] = merged_df['justification']
#st.table(merged_df)
