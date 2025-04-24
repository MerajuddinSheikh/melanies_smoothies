# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be',name_on_order )


cnx = st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'choose upto 5 ingredient:',my_dataframe)

if ingredients_list:
    

    ingredients_string=''

    for fruit_choosen in ingredients_list:
      ingredients_string += fruit_choosen + ' '
      st.subheader(fruit chosen + 'Nutrition Information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon"+fruit_choosen)
      sf_df=st.dataframe (data=smoothiefroot_response. json(), use_container_width=True)
      
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    #st.stop()

    time_to_insert=st.button('Submit Order')

    if time_to_insert:
     session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")





