import altair as alt
from vega_datasets import data
import pandas as pd
import streamlit as st

df_main = pd.read_csv('state_filtered_df.csv')
df_prevalence = pd.read_csv('prevalence_df.csv')

states = alt.topo_feature(data.us_10m.url, feature='states')

max_percentage_df = pd.read_csv('max_percentage_df.csv')

selector = alt.selection_point(fields=['id'], name='Select')

background = alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('albersUsa').properties(
    width=500,
    height=300
)

prevalence_scale = alt.Scale(domain=[df_prevalence['Percent'].min(), df_prevalence['Percent'].max()], scheme='oranges')
prevalence_color = alt.Color(field="Percent", type="quantitative", scale=prevalence_scale, title="Alzheimer's Prevalence (%)")

prevalence_map = alt.Chart(states).mark_geoshape().encode(
    color=prevalence_color,
    tooltip=[alt.Tooltip('state:N', title='State'),
             alt.Tooltip('Percent:Q', title='Prevalence (%)')]
             
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_prevalence, 'id', ['state', 'Percent'])
).add_params(
    selector
).transform_filter(
    selector
).project('albersUsa').properties(
    width=500,
    height=300,
    title="Alzheimer's Prevalence Across U.S. States in 2022"
)

# Cognitive Decline Map (showing the max percentage for each state)

max_percentage_df_filtered = max_percentage_df[max_percentage_df['Data_Value'].notnull()]

topic_color = alt.Color(
    'Topic:N',
    scale=alt.Scale(scheme='set3'), 
    title='Topic',
    legend=alt.Legend(),  
)

cognitive_map = alt.Chart(states).mark_geoshape().encode(
    color=alt.condition(
        alt.datum.Topic != None,  
        topic_color,  
        alt.value('lightgray')  
    ),
    tooltip=[alt.Tooltip('state:N', title='State'),
             alt.Tooltip('Data_Value:Q', title='Cognitive Decline Issue with most % reported'),
             alt.Tooltip('Topic:N', title='Topic')]
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(max_percentage_df_filtered, 'id', ['state', 'Data_Value', 'Topic'])
).add_params(
    selector 
).project('albersUsa').properties(
    width=500,
    height=300,
    title="Max Cognitive Decline Across U.S. States in 2022"
)

# Add an outline for the selected state without changing the color
selected_outline = alt.Chart(states).mark_geoshape(
    fill=None,  
    stroke='black',  
    strokeWidth=3
).transform_filter(
    selector  
).project('albersUsa').properties(
    width=500,
    height=300
)

# Combine both maps with their respective outlines
final_chart = alt.vconcat(
    background + prevalence_map + selected_outline,  
    background + cognitive_map + selected_outline 
).resolve_scale(
    color='independent'
)


final_chart2 = alt.vconcat(
    background + prevalence_map,
    background + cognitive_map,
).resolve_scale(
    color='independent'
)


# Display the final combined chart in Streamlit
st.altair_chart(final_chart, use_container_width=True)