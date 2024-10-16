import streamlit as st
from streamlit_option_menu import option_menu

# Import page modules
import overall_page
import compare_topics_page
import compare_states_page

# Set up navigation with a sidebar
with st.sidebar:
    selected = option_menu(
        "Main Menu", ["Overall", "Compare Topics", "Compare States"],
        icons=['people-fill', 'capsule', 'bar-chart'],
        menu_icon="cast", default_index=0,
    )

# Page navigation logic
if selected == "Overall":
    overall_page.show_overall_page()  

elif selected == "Compare Topics":
    compare_topics_page.show_compare_topics_page()  

elif selected == "Compare States":
    compare_states_page.show_compare_states_page()  
