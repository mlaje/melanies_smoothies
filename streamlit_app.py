# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("My parents New Healthy Diner")

st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

st.write(
    """ Choose the fruits
    """
    )

#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Apple", "Banana", "Orange"))
#st.write("You selected:", option)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:' , name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Elegir hasta 5 frutas', my_dataframe, max_selections = 5)

import requests



if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    
    ingredients_string = ''
    
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        st.subheader(fruit + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
        #st.text(fruityvice_response.json())
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order, order_filled)  
                     values (' """ + ingredients_string + """','""" + name_on_order + """',""" + """false""" + """)"""

    st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
