import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import io
import math

boat_df = pd.read_csv('boat_dataset.csv', encoding = 'latin-1') #UTF-8 can't decode byte 0xc3, so we have to read the file in this way, because there are no invalid bytes in that encoding

st.header('Yacht and Motorboat Pricing')
st.write('''
In this project I'll present an overview on the main characteristics that affect the final price of power boats. In order to have an accurate and proper analysis,
I interviewed Antonio Centis, holder of Nautica Centis. Founded by Bruno Centis in 1974, Nautica Centis has been a nautical workshop specialized in assembling and 
repairing marine engines and generators in boats and power boats. They perform ordinary and extraordinary maintenance of marine engines and systems using only original spare parts.
\nOver the years, Bruno's reliable character led to agreements with important global manufacturers of engines (Man, of which they are a Master workshop, Volvo Penta, and Weber Motor), generators 
(Onan, Kohler), maneuvering propellers (Sleipner), diesel pre-filters (Separ), batteries and battery chargers (Mastervolt), air conditioning systems (Dometic) and control systems (Yachtcontroller).
\nToday the workshop is managed by his son, Antonio, with the help of his family, and supported by all the employees who work every day with commitment and passion to guarantee a comprehensive service 
to customers for the maintenance of their boats.
\nAntonio led my analysis be realistic and suitable with a person who wants to buy a power boat, having the following DataFrame avaiable.
''')
st.write('Its head:')
st.write(boat_df.head())
st.write('Its tail:')
st.write(boat_df.tail())
if st.button('Complete DataFrame'): #in order to visualize all the dataframe
    st.write(boat_df)
st.write('Select the voice "Explore the DataFrame" to find more about it.')

st.sidebar.subheader('Settings')
if st.sidebar.checkbox('Explore the DataFrame'): 
    st.write('The DataFrame has 38 columns and 10344 rows, from which we can discover important aspects of each boat. We can get these information by the next tabular.')
    buffer = io.StringIO() #these steps are necessary to show boat_df.info() on the page by streamlit
    boat_df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s) #text ratheer than write to print fixed-width and preformatted text
    st.write('''For sure, we know price, category and type of a given boat. Its length, model, history and type of fuel are known for the most of the candidates.
    \nIt can be noticed that "Length" is a column of strings: a float number followed by letter "m", which means meter. Therefore it is better to turn it into a float 
    column in order to take advantage of this parameter.
    ''')
    st.write('''
    One person can be embarked for each linear meter of boat's length: i.e., if the boat is 13.7m long, 13 people can be embarked. Thus we can use the information given by column 
    Length to fill up the missing values of column Cert Number of People. I replaced the null values with the second entry of the tuple returned by the function modf() from the library math, 
    using a for cycle on the indexes of Cert Number of People's null entries. In order to find the latter, I used a boolean mask with the function isnan() from the library numpy.
    We end up with 10336 non-null values instead of 3597.''')
#Length in float
new_Length = []
for i in range(10344):
  item = str(boat_df.loc[i,'Length'])
  new_item = item.replace(' m','')
  value = float(new_item)
  new_Length.append(value)  
 
boat_df['Length'] = new_Length

#Filling the null values in Cert Number of People. Library math is used for the integer part of a number
null_cert_people_mask = np.isnan(boat_df['Cert Number of People']) #mask for NaN values
for i in boat_df['Cert Number of People'][null_cert_people_mask].index : 
  a = math.modf(boat_df.loc[i,'Length']) #math.modf returns a tuple of two values. The second is the integer part of the input number
  boat_df.loc[i, 'Cert Number of People'] = a[1]
