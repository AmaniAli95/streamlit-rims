import streamlit as st
import pandas as pd
import re
import plotly.express as px
import plotly.graph_objs as go
import os
import textwrap


# Read the CSV file
df = pd.read_csv('/Users/fatinamanimohdali/Downloads/rims12.csv')
del df["Unnamed: 0"]
del df["Unnamed: 0.1"]
df = df.replace('tiada', pd.np.nan)
df = df.reset_index(drop=True)

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
#st.dataframe(dfori)

# Create a regular expression pattern to match the desired column names
pattern = r'[A-Z]+_voteCount'
# Use the `filter` function and the `re.match` function to filter the column names
column_names = filter(lambda x: re.match(pattern, x), dfori.columns)
column_names_filtered = [column_name for column_name in filter(lambda x: re.match(pattern, x), dfori.columns) if dfori[column_name].notnull().any()]

##########

traces = []
for column_name in column_names_filtered:
    hovertext = '<br>' + "Details" + '<br>' + "Date: " + dfori['date'] + '<br>' + "DM: " + dfori['DM'] + '<br>' + column_name + ': ' + dfori[column_name].astype(str)
    dfori[column_name] = pd.to_numeric(dfori[column_name], downcast='integer')
    trace = {
        'x': dfori['date'],
        'y': dfori[column_name],
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

###########

def wrap_justification(text):
   return '<br>'.join(textwrap.wrap(text, width=60))

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
    #merged_df['justification'] = merged_df['justification'].apply(wrap_justification)
    merged_df['justification'] = merged_df['justification']
st.table(merged_df)

    
##########

traces = []
for column_name in column_names_filtered:
    folder = '/Users/fatinamanimohdali/Documents/RIMS/14Dec2022_new/justifi/'
    hovertext = '<br>' + "Details" + '<br>' + "Date: " + dfori['date'] + '<br>' + "DM: " + dfori['DM'] + '<br>' + column_name + ': ' + dfori[column_name].astype(str)
    for filename in dfori['filename']:
        if filename in [os.path.basename(file) for file in os.listdir(folder)]:
            df1 = pd.read_csv(folder + filename)
            justification = str(df1['justification'][0])
            justification = '<br>'.join(justification[i:i+60] for i in range(0, len(justification),60))
            #hovertext = '<br>' + "Details" + '<br>' + "Date: " + dfori['date'] + '<br>' + "DM: " + dfori['DM'] + '<br>' + column_name + ': ' + dfori[column_name].astype(str) + '<br>' + "Justification: " + justification
            hovertext += '<br>' + "Justification: " + justification
    dfori[column_name] = pd.to_numeric(dfori[column_name], downcast='integer')
    trace = {
        'x': dfori['date'],
        'y': dfori[column_name],
        'name': column_name,
        'type': 'scatter',
        'mode': 'lines+markers',
        'hovertext': hovertext,
        'hoverlabel': {
            'namelength': -1,
            'font': {
                'size': 2
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

##########

traces = []
for column_name in column_names_filtered:
    folder = '/Users/fatinamanimohdali/Documents/RIMS/14Dec2022_new/parliamentJus/'
    # Get a list of the filenames of the files in the folder
    filenames = [os.path.basename(file) for file in os.listdir(folder)]
    # Set the hovertext to include only the data in the dfori DataFrame
    hovertext = '<br>' + "Details" + '<br>' + "Date: " + dfori['date'] + '<br>' + "DM: " + dfori['DM'] + '<br>' + column_name + ': ' + dfori[column_name].astype(str)
    # Check if the dfori['filename'] is in the list of filenames of the files in the folder
    if dfori['filename'].astype(str).isin(filenames).any():
        indices = dfori['filename'].isin(filenames).index

        # Iterate over the indices
        for index in indices:
            #st.write(index)
            # Get the df1 DataFrame by reading the file with the matching filename
            df1 = pd.read_csv(folder + dfori.loc[index, 'filename'])
            #st.write(df1)
            justification = str(df1['justification'][0])
            #st.write(justification)
            # Wrap the justification text to the next line at every 50 characters
            justification = '<br>'.join(justification[i:i+60] for i in range(0, len(justification),60))
            # Set the hovertext to include the data in the df1 DataFrame
            hovertext += '<br>' + "Justification: " + justification
    dfori[column_name] = pd.to_numeric(dfori[column_name], downcast='integer')
    trace = {
        'x': dfori['date'],
        'y': dfori[column_name],
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
# Use the `go.Figure` function from `plotly` to create the chart figure
figure = go.Figure(data=traces, layout={
    'title': {'text': 'Vote Count by Date'},
    'xaxis': {'title': 'Date'},
    'yaxis': {'title': 'Vote Count'}
})
# Use the `st.plotly_chart` function to display the chart in Streamlit
st.plotly_chart(figure)


########

# Create a list of dictionaries representing the data for each trace in the chart
traces = []
hovertext_list = []
for column_name in column_names_filtered:
    folder = '/Users/fatinamanimohdali/Documents/RIMS/14Dec2022_new/justifi/'
    # Get a list of the filenames of the files in the folder
    filenames = [os.path.basename(file) for file in os.listdir(folder)]
    # Set the hovertext to include only the data in the dfori DataFrame
    hovertext = '<br>' + "Details:" + '<br>' + "Date: " + dfori['date'] + '<br>' + "DM: " + dfori['DM'] + '<br>' + column_name + ': ' + dfori[column_name].astype(str)

    # Check if the dfori['filename'] is in the list of filenames of the files in the folder
    if dfori['filename'].isin(filenames).any():
        # Get the index of the row with the matching filename
        index = dfori[dfori['filename'].isin(filenames)].index[0]
        # Get the df1 DataFrame by reading the file with the matching filename
        df1 = pd.read_csv(folder + dfori.loc[index, 'filename'])
        justification = str(df1['justification'][0])
        # Wrap the justification text to the next line at every 50 characters
        justification = '<br>'.join(justification[i:i+60] for i in range(0, len(justification),60))
        # Set the hovertext to include the data in the df1 DataFrame
        hovertext += '<br>' + "Justification: " + justification

    dfori[column_name] = pd.to_numeric(dfori[column_name], downcast='integer')
    trace = {
        'x': dfori['date'],
        'y': dfori[column_name],
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

# Use the `go.Figure` function from `plotly` to create the chart figure
figure = go.Figure(data=traces, layout={
    'title': {'text': 'Vote Count by Date'},
    'xaxis': {'title': 'Date'},
    'yaxis': {'title': 'Vote Count'},
})
# Use the `st.plotly_chart` function to display the chart in Streamlit
st.plotly_chart(figure)


