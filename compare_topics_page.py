import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

def show_compare_topics_page():
    file_path = 'data/averaged_4topics.csv'

    df = pd.read_csv(file_path)

    if 'LocationDesc' not in df.columns:
        st.error("The column 'LocationDesc' was not found in the dataset. Please check the dataset for column names.")
    else:
        state_id_map = {
            'Alabama': 1, 'Alaska': 2, 'Arizona': 4, 'Arkansas': 5, 'California': 6, 'Colorado': 8,
            'Connecticut': 9, 'Delaware': 10, 'Florida': 12, 'Georgia': 13, 'Hawaii': 15, 'Idaho': 16,
            'Illinois': 17, 'Indiana': 18, 'Iowa': 19, 'Kansas': 20, 'Kentucky': 21, 'Louisiana': 22,
            'Maine': 23, 'Maryland': 24, 'Massachusetts': 25, 'Michigan': 26, 'Minnesota': 27,
            'Mississippi': 28, 'Missouri': 29, 'Montana': 30, 'Nebraska': 31, 'Nevada': 32,
            'New Hampshire': 33, 'New Jersey': 34, 'New Mexico': 35, 'New York': 36, 'North Carolina': 37,
            'North Dakota': 38, 'Ohio': 39, 'Oklahoma': 40, 'Oregon': 41, 'Pennsylvania': 42,
            'Rhode Island': 44, 'South Carolina': 45, 'South Dakota': 46, 'Tennessee': 47, 'Texas': 48,
            'Utah': 49, 'Vermont': 50, 'Virginia': 51, 'Washington': 53, 'West Virginia': 54,
            'Wisconsin': 55, 'Wyoming': 56
        }

        df['state_id'] = df['LocationDesc'].map(state_id_map)

        categories = df['Class'].unique()

        us_states = alt.topo_feature(data.us_10m.url, 'states')
        base = alt.Chart(us_states).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ).project(
            type='albersUsa'
        ).properties(
            width=500,
            height=400
        )

        def create_heatmap(category):
            filtered_df = df[df['Class'] == category].dropna(subset=['Data_Value'])

            heatmap = alt.Chart(us_states).mark_geoshape().encode(
                color=alt.Color('Data_Value:Q', title=f'Proportion (%)', scale=alt.Scale(scheme='blues')),
                tooltip=[alt.Tooltip('LocationDesc:N', title='State'),
                         alt.Tooltip('Class:N', title='Category'),
                         alt.Tooltip('Data_Value:Q', title='Proportion (%)', format='.1f')]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(filtered_df, 'state_id', ['LocationDesc', 'Data_Value', 'Class'])
            ).properties(
                title=f"Map for: **{category}**"
            )
            return base + heatmap

        st.markdown("<h1 style='text-align: center;'>Compare Health-Related Topics Across the US</h1>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            selected_category1 = st.selectbox('Select Category for Plot 1:', categories, index=0, key='plot1')
            heatmap_chart1 = create_heatmap(selected_category1)
            st.altair_chart(heatmap_chart1, use_container_width=True)

        with col2:
            selected_category2 = st.selectbox('Select Category for Plot 2:', categories, index=1, key='plot2')
            heatmap_chart2 = create_heatmap(selected_category2)
            st.altair_chart(heatmap_chart2, use_container_width=True)
