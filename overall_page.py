import altair as alt
from vega_datasets import data
import pandas as pd
import streamlit as st

df_prevalence = pd.read_csv('prevalence_df.csv')
df_prevalence['Count'] = df_prevalence['Number (in thousands)'] * 1000

def show_overall_page():
    #st.markdown(
    #    """
    #    <style>
    #    .center-content {
    #        display: flex;
    #        justify-content: center;
    #    }
    #    </style>
    #    """,
    #    unsafe_allow_html=True
    #)

    st.markdown("<h1 style='text-align: center;'>Overview of Alzheimer's Prevalence Across the U.S.</h1>", unsafe_allow_html=True)

    states = alt.topo_feature(data.us_10m.url, feature='states')

    selector = alt.selection_point(fields=['state'], name='Select')

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=300, 
        height=250  
    )

    prevalence_scale = alt.Scale(domain=[df_prevalence['Percent'].min(), df_prevalence['Percent'].max()], scheme='oranges')
    prevalence_color = alt.Color(field="Percent", type="quantitative", scale=prevalence_scale, title="Alzheimer's Prevalence (%)")

    prevalence_map = alt.Chart(states).mark_geoshape().encode(
        color=prevalence_color,
        tooltip=[alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Percent:Q', title="Prevalence (%)"),
                alt.Tooltip('Count:Q', title="Count")]  # Added tooltip
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_prevalence, 'id', ['state', 'Percent', 'Count'])
    ).add_params(
        selector
    ).transform_filter(
        selector
    ).project('albersUsa').properties(
        width=300, 
        height=250, 
        title="Alzheimer's Prevalence Across U.S. States in 2022"
    )

    selected_outline = alt.Chart(states).mark_geoshape(
        fill=None,  
        stroke='black',  
        strokeWidth=2
    ).transform_filter(
        selector  
    ).project('albersUsa').properties(
        width=300,
        height=250
    )

    top_10 = df_prevalence.nlargest(10, 'Count')

    ranking_chart = alt.Chart(top_10).mark_bar().encode(
        y=alt.Y('state:N', sort='-x', title=None),  # Sort by prevalence
        x=alt.X('Count:Q', title="Number of People with Alzheimer's Disease"),
        color=alt.condition(
            selector,
            alt.value('orange'), 
            alt.value('lightgray')
        ),
        tooltip=[alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Percent:Q', title="Prevalence (%)"),
                alt.Tooltip('Count:Q', title="Number of People")]
    ).add_params(
        selector
    ).properties(
        width=130,  
        height=250, 
        title="Top 10 States by Number of People"
    )

    prevalence_chart = alt.hconcat(
        ranking_chart,
        background + prevalence_map + selected_outline
    ).resolve_scale(
        color='independent'
    )

    #st.markdown("<div class='center-content'>", unsafe_allow_html=True)
    st.altair_chart(prevalence_chart, use_container_width=True)
    #st.markdown("</div>", unsafe_allow_html=True)