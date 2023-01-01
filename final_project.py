import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

boat_df = pd.read_csv('boat_dataset.csv', encoding = 'latin-1') #UTF-8 can't decode byte 0xc3, so we have to read the file in this way, because there are no invalid bytes in that encoding

st.header('Yacht and Motorboat Pricing')
st.write("In this project I'll present an overview on the main characteristics that affect the final price of a yacht or a motor boat.\nThe DataFrame taken in exam is the following:")
st.write(boat_df)
st.write('Select the voice "Explore the DataFrame" to find more about it.')

st.sidebar.subheader('Settings')
if st.sidebar.checkbox('Explore the DataFrame'): 
    st.write('The DataFrame has 38 columns and 10344 rows, from which we can discover important aspects of each boat. We can get these information by the next tabular.')


