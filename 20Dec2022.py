import streamlit as st
import pandas as pd
# Read the CSV file
df = pd.read_csv('/Users/fatinamanimohdali/Downloads/rims.csv')
del df["Unnamed: 0"]

# Create the first dropdown menu
section = st.selectbox('Select section:', ['parliamentName', 'dunName'])

# Create the second dropdown menu based on the selection in the first dropdown
if section == 'dunName':
    column = st.selectbox('Select column:', df['dunName'].unique())
elif section == 'parliamentName':
    column = st.selectbox('Select column:', df['parliamentName'].unique())

# Display the table
st.table(df[df[section] == column])
