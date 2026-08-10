# Streamlit smoothie order form that inserts selections into Snowflake
# Import python packages
import streamlit as st
import os
import requests

from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()


# Write directly to the app
st.title(f":cup_with_straw: Custom Smoothie Order Form :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)
name_on_order = st.text_input('Name on Smoothie: ')
st.write ('The name on your Smooothie will be ', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    )
    
ingredients_string = ''    
#url = ['https://my.smoothiefroot.com/api/fruit/']
url = "https://my.smoothiefroot.com/api/fruit/"

if ingredients_list: 

  for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        st_url = url + fruit_chosen
        st.write (st_url)
        smoothiefroot_response = requests.get(url)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

        st.text(ingredients_string)

        my_insert_stmt = """ insert into SMOOTHIES.public.ORDERS(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

        
        time_to_insert = st.button('Submit Order')

        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

    

