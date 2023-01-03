import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import io

boat_df = pd.read_csv('boat_dataset.csv', encoding = 'latin-1') #UTF-8 can't decode byte 0xc3, so we have to read the file in this way, because there are no invalid bytes in that encoding

st.header('Yacht and Motorboat Pricing')
st.write("In this project I'll present an overview on the main characteristics that affect the final price of a yacht or a motor boat.\nThe DataFrame taken in exam is the following:")
st.write(boat_df)
st.write('Select the voice "Explore the DataFrame" to find more about it.')

st.sidebar.subheader('Settings')
if st.sidebar.checkbox('Explore the DataFrame'): 
    st.write('The DataFrame has 38 columns and 10344 rows, from which we can discover important aspects of each boat. We can get these information by the next tabular.')
    buffer = io.StringIO() #these steps are necessary to show boat_df.info() on the page by streamlit
    boat_df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s) #text ratheer than write to print fixed-width and preformatted text
    st.write('For sure, we know price, category, type and leghth of a given boat. Its model, history and type of fuel are known for the most of the candidates.\nIt can be noticed that "Length" is a column of strings: a float number followed by letter "m", which means meter. Therefore it is better to turn it into a float column in order to take advantage of this parameter.')
    st.write("One person can be embarked for each linear meter of boat's length: i.e., if the boat is 13.7m long, 13 people can be embarked. Thus we can use the information given by Length to fill up the missing values of column Cert Number of People.")
#Length in float
new_Length = []
for i in range(10344):
  item = str(boat_df.loc[i,'Length'])
  new_item = item.replace(' m','')
  value = float(new_item)
  new_Length.append(value)  
 
boat_df['Length'] = new_Length


