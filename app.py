import streamlit as st
from streamlit_option_menu import option_menu

# Import page modules
import overall_page
import compare_topics_page
import compare_states_page

st.set_page_config(page_title='Test', 
                       layout='wide')

# Set up navigation with a sidebar
# with st.sidebar:
#     selected = option_menu(
#         "Main Menu", 
#         ["Overall", "Compare Topics", "Compare States"],
#         icons=['people-fill', 'capsule', 'bar-chart'],
#         menu_icon="cast", default_index=0,
#         styles={
#             "icon": {"color": "orange", "font-size": "25px"}, 
#             "nav-link": {
#                 "font-size": "16px", 
#                 "text-align": "left", 
#                 "margin": "0px", 
#                 "--hover-color": "#6a0dad",  # Purple on hover
#             },
#             "nav-link-selected": {
#                 "background-color": "#6a0dad",  # Purple when selected
#                 "color": "white"
#             },
#         }
#     )

# # Page navigation logic
# if selected == "Overall":
#     overall_page.show_overall_page()

# elif selected == "Compare Topics":
#     compare_topics_page.show_compare_topics_page()

# elif selected == "Compare States":
#     compare_states_page.show_compare_states_page()


st.markdown(
    """
    <style>
    /* Adjust the width of the sidebar */
    .css-1d391kg {
        width: 10px;  /* Adjust this value to make the sidebar narrower */
        min-width: 10px;  /* Ensures the sidebar doesn't shrink below this width */
    }

    /* Adjust the main content area to align properly with sidebar */
    .css-1outpf7 {
        margin-left: 10px;  /* Adjust the margin to align the content with the new sidebar width */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set up navigation with a sidebar
with st.sidebar:
    selected = option_menu(
        "Main Menu", 
        ["Overall", "Compare Topics", "Compare States"],
        icons=['people-fill', 'capsule', 'bar-chart'],
        menu_icon="cast", default_index=0,
        styles={
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "#6a0dad",  # Purple on hover
            },
            "nav-link-selected": {
                "background-color": "#6a0dad",  # Purple when selected
                "color": "white"
            },
        }
    )

# Page navigation logic
if selected == "Overall":
    overall_page.show_overall_page()

elif selected == "Compare Topics":
    compare_topics_page.show_compare_topics_page()

elif selected == "Compare States":
    compare_states_page.show_compare_states_page()
