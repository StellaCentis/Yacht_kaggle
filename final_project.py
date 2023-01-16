import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import io
import math
import new_functions as nf 

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
    st.write('''For sure, we know price, category and type of a given boat. Its length, model, location, history and type of fuel are known for the most of the candidates.
    \nIt can be noticed that "Length" is a column of strings: a float number followed by letter "m", which means meter. Therefore it is better to turn it into a float 
    column in order to take advantage of this parameter. Analogously it has been done with columns "Width" and "Depth".
    \nThese parameters are useful in order to choose the right berth and to know where the boat can navigate. In addiction, boats under 10 m length don't have to be declared to the tax authorities in Italy.
     In EU there are limitations on the boat license according to the length of the boat. Thus it's really important for buyer to know these data. Therefore, it's appropriate dropping all the rows that have
     a null entry in column "Width", as they are 63 over 10344. For this aim I used the method notna() to detect valid values in the DataFrame. The resulting DataFrame has 10281 rows. Then I filled the 
     null values of column "Depth" with its mean.
    ''')
    st.write('''
    One person can be embarked for each linear meter of boat's length: i.e., if the boat is 13.7m long, 13 people can be embarked. Thus we can use the information given by column 
    Length to fill up the missing values of column Cert Number of People. I replaced the null values with the second entry of the tuple returned by the function modf() from the library math, 
    using a for cycle on the indexes of Cert Number of People's null entries. In order to find the latter, I used a boolean mask with the function isnan() from the library numpy.
    We end up with 10281 non-null float values instead of 3597.''')
    st.write('''
    Knowing where the boat is located is an important decisional factor, since transport can be a huge cost. Antonio proposed an example that he saw with his eyes: a boat of 15 m long moved from Naples to Lignano Sabbiadoro
    has cost 10000 €. Therefore, if you're undecided between two boats but the first is near to you and the second is quite far, you'll choose the first one. The column concerning this parameter gives either
    the Nation and the city or only the first one. Thus, I created a function that returns the first word of a string and modified the original column. This leds the analysis be easier.
    
    ''')

boat_df.columns =  list(map(lambda x : x.replace(' ', '_').lower(), boat_df.columns)) #columns optimized by replacing spaces and lowering letters

#Length in float
new_length = []
for i in range(10344):
  item = str(boat_df.loc[i,'length'])
  new_item = item.replace(' m','')
  value = float(new_item)
  new_length.append(value)  
 
boat_df['length'] = new_length

#Width in float
new_width = []
for i in range(10344):
  item = str(boat_df.loc[i,'width'])
  new_item = item.replace(' m','')
  value = float(new_item)
  new_width.append(value)

boat_df['width'] = new_width

#Depth in float
new_depth = []
for i in range(10344):
  item = str(boat_df.loc[i,'depth'])
  new_item = item.replace(' m','')
  value = float(new_item)
  new_depth.append(value)

boat_df['depth'] = new_depth

#Dropping rows according to non-null values of the column Width
boat_df = boat_df[boat_df['width'].notna()]

#Null values of Depth filled with its mean
boat_df['depth'].fillna(boat_df['depth'].mean(), inplace=True)

#Filling the null values in Cert Number of People. Library math is used for the integer part of a number
null_cert_people_mask = np.isnan(boat_df['cert_number_of_people']) #mask for NaN values
for i in boat_df['cert_number_of_people'][null_cert_people_mask].index : 
  a = math.modf(boat_df.loc[i,'length']) #math.modf returns a tuple of two values. The second is the integer part of the input number
  boat_df.loc[i, 'cert_number_of_people'] = a[1]

boat_df['location'].fillna('Unknown', inplace=True) #firstly, fill the NaN values 
#Lets consider only the State. This process let value_counts() perform better, putting together boat of the same Nation
new_location = []
for i in range(len(boat_df)):
  position = nf.first_word(boat_df.iloc[i,32]) #location is the 32nd column
  new_location.append(position)
boat_df.location = new_location

#number_of_views_last_7_days in integer
new_views = []
for i in range(len(boat_df)):
  new_views.append(int(boat_df.iloc[i,9]))

boat_df['number_of_views_last_7_days'] = new_views
boat_df.number_of_views_last_7_days.fillna(boat_df.number_of_views_last_7_days.mean(), inplace=True) #fill the NaN values of Number of views last 7 days
boat_df.manufacturer.fillna('Unknown', inplace=True) #fill the NaN values of Manufacturer
boat_df.model.fillna('Unknown', inplace=True) #fill the NaN values of Model
boat_df.year_built.fillna(boat_df['year_built'].mean(), inplace=True) #fill the NaN values of Year built
boat_df.condition.fillna('Unknown', inplace=True) #fill the NaN values of Condition

#fill the NaN values of Fuel type
boat_df.engine = list(map(lambda x : str(x).replace(' ', '_').lower(), boat_df.engine)) #some engines are the same but are different accorting to Python as they are capital letters
boat_df.fuel_type.fillna('Diesel', inplace=True) #Ignoring the NaN values, the first five most common engines of the boats which have null-value fuel type are all diesel