import streamlit
import pandas as pd
import requests
import snowflake.connector
#Snowflake connection details, start an sql cursor and load one row from the fruit_load_list
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()


streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

#Add a pick list so the customers can choose the fruits they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#Display the table on the page
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice')
#ask the user about the fruit they would like to know more about, and let the user know about what they entered
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)
#get requests from fruityvice about the chosen fruit
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#display the request as a json result

#normalize the json result received earlier
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
#display a df of the normalized json
streamlit.dataframe(fruityvice_normalized)

#Moved the following from the connection details block in row 5
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)
fruit_request = streamlit.text_input('What fruit would you like to add?', 'Borange')
streamlit.write("Thanks for adding ", fruit_request)
if 'mango' in my_data_row:
    streamlit.text("There's an orange")
#my_cur.execute("insert into fruit_load_list values ('teststreamlit')")