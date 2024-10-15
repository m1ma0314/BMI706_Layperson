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

# Display the final combined chart in Streamlit
st.altair_chart(final_chart, use_container_width=True)

### Task 2

df = pd.read_csv('cognitive_decline_df_22.csv')
df['Question_Simple'] = df['Question'].map({
    'Percentage of older adults with subjective cognitive decline or memory loss who reported talking with a health care professional about it': 'Talked to Healthcare',
    'Percentage of older adults who reported subjective cognitive decline or memory loss that interferes with their ability to engage in social activities or household chores': 'Interferes with Activities',
    'Percentage of older adults who reported subjective cognitive decline or memory loss that is happening more often or is getting worse in the preceding 12 months': 'Getting Worse',
    'Percentage of older adults who reported that as a result of subjective cognitive decline or memory loss that they need assistance with day-to-day activities': 'Needs Assistance'
})

cognitive_decline_df = df[df['Data_Value_Unit'] == '%']

proportion_by_resp = cognitive_decline_df.groupby(['Stratification1', 'Question_Simple'])['Data_Value'].mean().reset_index()

alt_chart = alt.Chart(proportion_by_resp).mark_bar().encode(
    x=alt.X('Question_Simple:N', title=None, axis=alt.Axis(labelAngle=45)),
    y=alt.Y('Data_Value:Q', title='Proportion (%)'),
    color=alt.Color('Question_Simple:N', title='Cognitive Decline Questions'),
    column=alt.Column('Stratification1:N', title=None),
    tooltip=[alt.Tooltip('Stratification1', title='Age Group'),
             alt.Tooltip('Question_Simple', title='Question'),
             alt.Tooltip('Data_Value:Q', title='Proportion (%)', format='.1f')]
).properties(
    title="Proportion of Older Adults' Responses to Experiences of Cognitive Decline Across Age Groups",
    width=150,
    height=400
)

st.altair_chart(alt_chart, use_container_width=True)


race_data = cognitive_decline_df[cognitive_decline_df['StratificationCategory2'] == 'Race/Ethnicity']

mean_race_values = race_data.groupby(['Stratification2', 'Question_Simple'])['Data_Value'].mean().reset_index()

race_grouped_chart = alt.Chart(mean_race_values).mark_bar().encode(
    x=alt.X('Question_Simple:N', title=None, axis=alt.Axis(labelAngle=45)),
    y=alt.Y('Data_Value:Q', title='Proportion (%)'),
    color=alt.Color('Question_Simple:N', title='Cognitive Decline Questions'),
    column=alt.Column('Stratification2:N', title=None),
    tooltip=[alt.Tooltip('Stratification2', title='Race/Ethnicity'),
             alt.Tooltip('Question_Simple', title='Question'),
             alt.Tooltip('Data_Value:Q', title='Proportion (%)', format='.1f')]
).properties(
    title='Proportion of Responses by Race/Ethnicity for Cognitive Decline Questions',
    width=150,
    height=400
)

st.altair_chart(race_grouped_chart, use_container_width=True)

gender_data = df[df['StratificationCategory2'] == 'Gender']

mean_gender_values = gender_data.groupby(['Stratification2', 'Question_Simple'])['Data_Value'].mean().reset_index()

gender_grouped_chart = alt.Chart(mean_gender_values).mark_bar().encode(
    x=alt.X('Question_Simple:N', title=None, axis=alt.Axis(labelAngle=45)),
    y=alt.Y('Data_Value:Q', title='Proportion (%)'),
    color=alt.Color('Question_Simple:N', title='Cognitive Decline Questions'),
    column=alt.Column('Stratification2:N', title=None),
    tooltip=[alt.Tooltip('Stratification2', title='Gender'),
             alt.Tooltip('Question_Simple', title='Question'),
             alt.Tooltip('Data_Value:Q', title='Proportion (%)', format='.1f')]
).properties(
    title='Proportion of Responses by Gender for Cognitive Decline Questions',
    width=150,
    height=400
)

st.altair_chart(gender_grouped_chart, use_container_width=True)

from vega_datasets import data

us_states = alt.topo_feature(data.us_10m.url, 'states')

mean_location_values = df.groupby(['LocationDesc', 'Question_Simple'])['Data_Value'].mean().reset_index()

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

mean_location_values['state_id'] = mean_location_values['LocationDesc'].map(state_id_map)

base = alt.Chart(us_states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    type='albersUsa'
).properties(
    width=800,
    height=500
)

heatmap = alt.Chart(us_states).mark_geoshape().encode(
    color=alt.Color('Data_Value:Q', title='Proportion (%)', scale=alt.Scale(scheme='blues')),
    tooltip=['LocationDesc:N', 'Question_Simple:N', 'Data_Value:Q']
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(mean_location_values, 'state_id', ['LocationDesc', 'Data_Value', 'Question_Simple'])
)

map_chart = base + heatmap
st.altair_chart(map_chart, use_container_width=True)

us_states = alt.topo_feature(data.us_10m.url, 'states')

mean_location_values = df.groupby(['LocationDesc', 'Question_Simple'])['Data_Value'].mean().reset_index()

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

mean_location_values['state_id'] = mean_location_values['LocationDesc'].map(state_id_map)

questions = mean_location_values['Question_Simple'].unique()

base = alt.Chart(us_states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    type='albersUsa'
).properties(
    width=400,
    height=300
)

def create_heatmap(question):
    heatmap = alt.Chart(us_states).mark_geoshape().encode(
        color=alt.Color('Data_Value:Q', title=f'Proportion (%)', scale=alt.Scale(scheme='blues')),
        tooltip=[alt.Tooltip('LocationDesc:N', title='State'),
                 alt.Tooltip('Question_Simple:N', title='Question'),
                 alt.Tooltip('Data_Value:Q', title='Proportion (%)', format='.1f')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(mean_location_values[mean_location_values['Question_Simple'] == question],
                             'state_id', ['LocationDesc', 'Data_Value', 'Question_Simple'])
    ).properties(
        title=question
    )
    return base + heatmap

chart1 = create_heatmap(questions[0])
chart2 = create_heatmap(questions[1])
chart3 = create_heatmap(questions[2])
chart4 = create_heatmap(questions[3])

final_chart2 = (chart1 | chart2) & (chart3 | chart4)

st.altair_chart(final_chart2, use_container_width=True)

### Task 3 Angel
# Disable the row limit for large datasets
alt.data_transformers.disable_max_rows()

# Load the dataset
df = pd.read_csv('cognitive_decline_df.csv')

# Clean column names and ensure Data_Value is numeric
df.columns = df.columns.str.strip().str.replace(' ', '_')
df['Data_Value'] = pd.to_numeric(df['Data_Value'], errors='coerce')

# Define U.S. regions based on states
regions = {
    'Northeast': ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York', 'New Jersey', 'Pennsylvania'],
    'Midwest': ['Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Missouri', 'North Dakota', 'South Dakota', 'Nebraska', 'Kansas'],
    'South': ['Delaware', 'Maryland', 'District_of_Columbia', 'Virginia', 'West Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida', 'Kentucky', 'Tennessee', 'Mississippi', 'Alabama', 'Oklahoma', 'Texas', 'Arkansas', 'Louisiana'],
    'West': ['Idaho', 'Montana', 'Wyoming', 'Nevada', 'Utah', 'Colorado', 'Arizona', 'New Mexico', 'Alaska', 'Washington', 'Oregon', 'California', 'Hawaii']
}

# Create a reverse mapping from state to region
state_to_region = {state: region for region, states in regions.items() for state in states}

# Add a Region column to the dataframe
df['Region'] = df['LocationDesc'].map(state_to_region)

# Filter out rows where Region is not defined (in case there are missing states)
df_filtered = df.dropna(subset=['Region'])

# Replace NaN values in Data_Value with 0
df_filtered['Data_Value'] = df_filtered['Data_Value'].fillna(0)

# Step 1: Create a dropdown menu for Topic selection, initialized with the first topic
initial_topic = df_filtered['Topic'].unique()[0]  # Get the first topic
topic_dropdown = alt.binding_select(options=list(df_filtered['Topic'].unique()), name='Topic: ')
topic_selection = alt.selection_point(fields=['Topic'], bind=topic_dropdown, value=initial_topic)  # Pass the string value directly

# Step 2: Group by region to calculate the average percentage for each region
df_aggregated_region = df_filtered.groupby(['Region', 'Topic'], as_index=False).agg({'Data_Value': 'mean'})

# Group by state to calculate the average percentage for each state
df_aggregated_state = df_filtered.groupby(['LocationDesc', 'Region', 'Topic'], as_index=False).agg({'Data_Value': 'mean'})

# Step 3: Regional bar chart with topic and region selector
region_selection = alt.selection_point(fields=['Region'], bind='legend')

regional_bar = alt.Chart(df_aggregated_region).mark_bar().encode(
    x=alt.X('Region:N', title='Region'),
    y=alt.Y('Data_Value:Q', title='Avg. Engagement (%)', scale=alt.Scale(domain=[0, 50])),  # Limit y-axis to 100%
    color=alt.Color('Region:N', title='Region'),
    tooltip=[alt.Tooltip('Region:N'), alt.Tooltip('Data_Value:Q', title='Avg. Engagement (%)')]
).add_selection(
    region_selection
).transform_filter(
    topic_selection  # Filter based on selected topic
).properties(
    width=600,
    height=400,
    title="Regional Engagement in Cognitive Decline Discussions"
)

# Step 4: State-level bar charts
state_bar = alt.Chart(df_aggregated_state).mark_bar().encode(
    x=alt.X('LocationDesc:N', title='State', sort='-y'),  # Sort states by the engagement levels
    y=alt.Y('Data_Value:Q', title='Avg. Engagement (%)', scale=alt.Scale(domain=[0, 50])),  # Engagement in percentage
    color=alt.Color('Region:N', title='Region'),  # Same color as the region
    tooltip=[alt.Tooltip('LocationDesc:N', title='State'), alt.Tooltip('Data_Value:Q', title='Avg. Engagement (%)')]
).transform_filter(
    region_selection & topic_selection  # Filter based on both the region and selected topic
).properties(
    width=600,
    height=400,
    title="State-Level Engagement in Discussions by Topic"
)

# Step 5: Combine the two charts into a linked view and include the dropdown
linked_dashboard = alt.vconcat(
    regional_bar.add_selection(topic_selection),
    state_bar
)

st.altair_chart(linked_dashboard, use_container_width=True)





