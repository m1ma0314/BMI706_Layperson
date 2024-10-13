import altair as alt
from vega_datasets import data
import pandas as pd
import streamlit as st

df_main = pd.read_csv('state_filtered_df.csv')
df_prevalence = pd.read_csv('prevalence_df.csv')

states = alt.topo_feature(data.us_10m.url, feature='states')

max_percentage_df = pd.read_csv('max_percentage_df.csv')

selector = alt.selection_point(fields=['StateID'], name='Select')

background = alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project('albersUsa').properties(
    width=500,
    height=300
)

prevalence_scale = alt.Scale(domain=[df_prevalence['Percent'].min(), df_prevalence['Percent'].max()], scheme='oranges')

prevalence_map = alt.Chart(states).mark_geoshape().encode(
    color=alt.Color('Percent:Q', scale=prevalence_scale, title="Alzheimer's Prevalence (%)"),
    tooltip=[alt.Tooltip('State:N', title='State'),
             alt.Tooltip('Percent:Q', title='Prevalence (%)')]
             
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_prevalence, 'StateID', ['State', 'Percent'])
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
cognitive_scale = alt.Scale(domain=[max_percentage_df['Data_Value'].min(), max_percentage_df['Data_Value'].max()], scheme='blues')

cognitive_map = alt.Chart(states).mark_geoshape().encode(
    #color=alt.Color('Data_Value:Q', scale=cognitive_scale, title='Max Cognitive Decline (%)'),
    color=alt.Color('Question:N', scale=alt.Scale(scheme='category10'), title='Question'),
    tooltip=[alt.Tooltip('LocationDesc:N', title='State'),
             alt.Tooltip('Data_Value:Q', title='Max Decline (%)'),
             alt.Tooltip('Question:N', title='Question')]
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(max_percentage_df, 'StateID', ['LocationDesc', 'Data_Value', 'Question'])
).add_params(
    selector
).transform_filter(
    selector
).project('albersUsa').properties(
    width=500,
    height=300,
    title="Max Cognitive Decline Across U.S. States in 2022"
)

# Combine both maps vertically
final_chart = alt.vconcat(background+prevalence_map, background+cognitive_map).resolve_scale(
    color='independent'
)

# Display the final combined chart in Streamlit
st.altair_chart(final_chart, use_container_width=True)
