import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

#defines
def get_fruityvice_data(fruit_choices):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
def get_fruit_load_list():
    with my_cnx,cursor as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()




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

#Fruityvice query

streamlit.header('Fruityvice Fruit Advice')
#ask the user about the fruit they would like to know more about, and let the user know about what they entered
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please Select a fruit to get information.")
#get requests from fruityvice about the chosen fruit
    else:
        streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    streamlit.error("Oops!")

#Moved the following from the connection details block in row 5
streamlit.header("The fruit load list contains:")
#Snowflake connection details, start an sql cursor and load one row from the fruit_load_list
if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    #my_data_row = get_fruit_load_list()
    streamlit.dataframe(get_fruit_load_list())

fruit_request = streamlit.text_input('What fruit would you like to add?', 'Borange')
streamlit.write("Thanks for adding ", fruit_request)
if (my_cur.execute("select * from fruit_load_list where fruit_name = 'teststreamlit'").fetchall()) == []:
    my_cur.execute("insert into fruit_load_list values ('teststreamlit')")