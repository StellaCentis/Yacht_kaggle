import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import io
import math
import new_functions as nf 
import seaborn as sb


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
st.write('Select the voice "Exploration and Cleaning of the DataFrame" to find more about it.')

st.sidebar.subheader('Settings')
if st.sidebar.checkbox('Exploration and Cleaning of the DataFrame'): 
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
    \nBefore going to next section, I have to convert all prices in Euro, in order to be able to compare them. First of all I simplified the notation of the price, by removing ',-'. After having 
    understood which are the currencies in the column 'price', I converted all the prices in Euro, excepted for the entries 'Price on request'. I computed the mean of the numerical entries, converted in float by using the method astype and I 
    used the value to fill the 'Price on request' entries.
    \nThe final DataFrame is visible by selecting 'Final DataFrame'
  
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

#Drop of the other columns:
boat_df.drop(['type','boat_name','year_built','displacement','ce_design_category','engine_performance','fuel_capacity','advertisement_date'],inplace= True, axis=1 )
boat_df.drop(boat_df.iloc[:, 10:20], inplace=True, axis = 1)
boat_df.drop(boat_df.iloc[:, 12:15], inplace=True, axis = 1)
boat_df.drop(boat_df.iloc[:, 14::], inplace=True, axis = 1)

#Simplification of the notation of the prices:
new_prices = []
for i in boat_df.price.index:
  item = str(boat_df.loc[i,'price'])
  new_item = item.replace(',-','')
  new_prices.append(new_item)

boat_df.price = new_prices

#All in Euro
#modification of all the column price in EUR
for i in boat_df.index:
  if 'CHF' in str(boat_df.loc[i, 'price']):
    words_price = boat_df.loc[i, 'price'].split()
    if len(words_price[1])<7:
      words_price[1] = (float(words_price[1])*1000)*1.01
      boat_df.loc[i, 'price'] = words_price[1]
    else:
      words_price[1] = float(words_price[1].replace('.',''))*1.01
      boat_df.loc[i, 'price'] = words_price[1]
  elif 'Â£' in str(boat_df.loc[i, 'price']):
    words_price = boat_df.loc[i, 'price'].split()
    if len(words_price[1])<7:
      words_price[1] = (float(words_price[1])*1000)*1.13
      boat_df.loc[i, 'price'] = words_price[1]
    else:
      words_price[1] = float(words_price[1].replace('.',''))*1.13
      boat_df.loc[i, 'price'] = words_price[1]
  elif 'DKK' in str(boat_df.loc[i, 'price']):
    words_price = boat_df.loc[i, 'price'].split()
    if len(words_price[1])<7:
      words_price[1] = (float(words_price[1])*1000)*0.13
      boat_df.loc[i, 'price'] = words_price[1]
    else:
      words_price[1] = float(words_price[1].replace('.',''))*0.13
      boat_df.loc[i, 'price'] = words_price[1]
  elif 'USD' in str(boat_df.loc[i, 'price']):
    words_price = boat_df.loc[i, 'price'].split()
    if len(words_price[1])<7:
      words_price[1] = (float(words_price[1])*1000)*0.93
      boat_df.loc[i, 'price'] = words_price[1]
    else:
      words_price[1] = float(words_price[1].replace('.',''))*0.93
      boat_df.loc[i, 'price'] = words_price[1]
  elif 'SEK' in str(boat_df.loc[i, 'price']):
    words_price = boat_df.loc[i, 'price'].split()
    if len(words_price[1])<7:
      words_price[1] = (float(words_price[1])*1000)*0.09
      boat_df.loc[i, 'price'] = words_price[1]
    else:
      words_price[1] = float(words_price[1].replace('.',''))*0.09
      boat_df.loc[i, 'price'] = words_price[1]
  elif 'EUR' in str(boat_df.loc[i, 'price']):
    words_price = boat_df.loc[i, 'price'].split()
    words_price[1] = float(words_price[1].replace('.',''))
    boat_df.loc[i, 'price'] = words_price[1]
  else: #there are entries of the type 'Price on request'
    pass

#mean of the numerical values of this column, that I'll use to fill the 'price on request' entries
mean_price = boat_df[boat_df.loc[:,'price'] != 'Price on request'].price.astype(float).mean()
boat_df.loc[boat_df.loc[:,'price'] == 'Price on request', 'price'] = mean_price 
boat_df.price = boat_df.price.astype(float) #in order to have a float column

if st.button('Final DataFrame'): #in order to visualize all the dataframe
    st.write(boat_df)
st.subheader('Relevant plots')
st.write('''
In the following plots I will compare some relevant relationships between the attributes chosen: price, category, boat type, manufacturer, model, condition, length, width, depth, cert number
 of people, engine, fuel type, location and number of views in last 7 days. 
 ''')

#Plot to have an overview of the manufacturers of the power boats in this dataframe
#In order to have a much more readable manufacturer (also because it is the main one):
mask = boat_df.manufacturer == 'BÃ©nÃ©teau power boats' 
boat_df.loc[mask,'manufacturer'] = 'Beneteau'
colors = plt.get_cmap('Blues')(np.linspace(0.1, 0.9, 10))
fig = plt.figure(figsize = (8,6))
plt.pie(boat_df.manufacturer.value_counts().head(10), labels = boat_df.manufacturer.value_counts().head(10).index, colors = colors, autopct = '%.1f%%', startangle = 335)

st.pyplot(fig)
st.caption('Top 10 manufacturers of the power boats considered.')
st.write('''
From the pie chart we can note that about one third of the boats have an unknown manufacturer; Bénéteau is one of the oldest family-run boatbuilders in the business and the world’s largest producer of yachts, launching more than 10,000 hulls per year. 
Based in the Vendée region of France, with a second manufacturing base in Marion, South Carolina, Bénéteau is a major player in both the motorboat and sailing yacht markets.
The Bénéteau Group’s wider portfolio includes a variety of boat brands, such as Four Winns, Glastron, Jeanneau, Prestige, Scarab and Wellcraft.
\nFounder Henri Jeanneau had a background in cars and planes when he set up this French boatbuilder in 1957. Today the company builds models ranging from the ubiquitous Merry Fisher to the luxury Prestige collection.
\nSunseeker is currently owned by Chinese group Dalian Wanda, but it remains a British company with manufacturing still based in Poole. Its emphasis is on having fun in the sun, focusing on superyachts and performance boats.
\nThe American Sea Ray promotes its brand as being a boating lifestyle with an owners club providing discounts on boating-related services and an application-based magazine. The company has won a 
variety of J.D. Power and Associate awards as well as from the NMMA and marine magazines including Boating. Additionally, Sea Ray is the recipient of a Five Star Diamond Award presented by the American Academy of Hospitality Science for their 
superb customer service.
\nPrincess Yachts is one of the true titans of the British boating industry. One of the distinguishing features of Princess is its design partnership with legendary British naval architecture firm Olesinski and Italian styling house Pininfarina.
Currently owned by L Capital, Princess Yachts are part of the same stable of brands as Louis Vuitton and Moet Hennessy, so their knowledge of the luxury lifestyle is unrivalled.
\nCantiere Nautico Cranchi, more commonly known as Cranchi Yachts, is one of Italy’s oldest boatbuilders, with a history that can be traced back to 1870.
Based in the Lombardy region, Cranchi works closely with designer Christian Grande to ensure a consistent Italian style throughout its range, while its primary engine supplier Volvo Penta has a relationship with the brand that has lasted more than 50 years.
\nAzimut Yachts is one of Italy’s foremost boatbuilders, based at a state-of-the-art 100,000 square metre facility in Avigliana, less than 20 miles west of Turin, which can produce up to 300 boats per year and has built more than 10,000 hulls to date.
Azimut has pioneered several key yachting trends over the years, such as large frameless windows, electric helm seats and walnut wood interiors.
\nFounded in 1978 as a sailboat builder, Bavaria Yachtbau is the largest yacht manufacturer in Germany with its headquarters in Giebelstadt.
Since 2001 the firm has also built motorboats and the current range includes open boats, sportscruisers and flybridges, ranging in size from 28ft to 55ft.
\nFrom humble beginnings in Oundle, England, Fairline has become an iconic name in yachting worldwide. Its Superboats category won the 2020 Motorboat of the Year awards.
''')

#Bar chart to compare the most common manufacturers chosen power boats' mean value 
labels = boat_df.manufacturer.value_counts().head(10).index[1::]
data = np.array([boat_df[boat_df.loc[:, 'manufacturer'] == x].price.mean() for x in labels ])
fig2, ax2 = plt.subplots(figsize=(10,5))
plt.barh(labels, data, color = colors)
plt.xlabel('Mean price')
plt.ylabel('Manufacturer')
st.write(fig2)
st.caption("Comparison of the power boats' mean value between the most common manufacturers chosen previously")
st.write('''
As we can notice, Sunseeker has the highest mean value for boats, as it focuses on superyachts; followed by Princess, which concernes with luxury lifestyle.
\nThe next plots reflect the considerations that can be taken from the correlation matrix.
''')
fig3 = plt.figure(figsize=(8,6))
sb.heatmap(boat_df.corr(), annot=True)
st.write(fig3)
st.caption('Correlation matrix')
st.write('''
Select the correlation you want to deepen in the following multi-selection choice.
''')

option = st.selectbox(
    'Choose two attributes to compare:',
    ('Length - Price', 'Width - Price', 'Length - Width', 'Length - Depth','Width - Number of views last 7 days','Length - Number of views last 7 days'))

if option == 'Length - Price':
  x = boat_df.length
  y = boat_df.price

  fig4, (ax4_1, ax4_2) = plt.subplots(2, 1, sharex=True)
  fig4.subplots_adjust(hspace=0.2)  # adjust space between axes

  ax4_1.scatter(x,y, s = 6, facecolors='none', edgecolors='b')
  ax4_2.scatter(x,y, s = 6, facecolors='none', edgecolors='b')

  # zoom-in / limit the view to different portions of the data
  ax4_1.set_ylim(1.4e7,3.1e7)  # outliers only
  ax4_2.set_ylim(0,0.5e7)  # most of the data
  ax4_1.set_yticks([1.5e7,2.4e7,3.2e7])
  
  # hide the spines between ax and ax2
  ax4_1.spines['bottom'].set_visible(False)
  ax4_2.spines['top'].set_visible(False)
  ax4_1.xaxis.tick_top()
  ax4_1.tick_params(labeltop=False)  # don't put tick labels at the top
  ax4_2.xaxis.tick_bottom()

  d = .15  # proportion of vertical to horizontal extent of the slanted line
  kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12, linestyle="none", color='k', mec='k', mew=1, clip_on=False)
  ax4_1.plot([0, 1], [0, 0], transform=ax4_1.transAxes, **kwargs)
  ax4_2.plot([0, 1], [1, 1], transform=ax4_2.transAxes, **kwargs)

  st.pyplot(fig4)
  expander = st.expander("See explanation")
  expander.write('''
  How can be noted, length is not correlated with price. That is because price is determined also by the 
  condition of the boat, its engine, its manufacturer, its year of construction. The latter can be really meaningful as
  every boat loses its 30% of value after just one year and its 10% in each following year.
  ''')

if option == 'Width - Price':
  x = boat_df.width
  y = boat_df.price

  fig5 = plt.figure()
  plt.scatter(x,y, s = 6,  facecolors='none', edgecolors='b')
  st.pyplot(fig5)
  expander = st.expander("See explanation")
  expander.write('''
  How can be noted, width is not correlated with price. That is because width doesn't impact the final price of a boat. 
  Customers could look for a certain level of width according to the marina they will be in; width does not concerne with their wallet.
  ''')
  