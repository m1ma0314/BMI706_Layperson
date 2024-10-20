import altair as alt
from vega_datasets import data
import pandas as pd
import streamlit as st

@st.cache_data
def load_prevalence_data():
    df = pd.read_csv('data/prevalence_df.csv')
    df['Count'] = df['Number (in thousands)'] * 1000
    return df

@st.cache_data
def load_engagement_data():
    df = pd.read_csv('data/averaged_4topics.csv')
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    df['Data_Value'] = pd.to_numeric(df['Data_Value'], errors='coerce')
    
    # Mapping of states to regions
    regions = {
        'Northeast': ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York', 'New Jersey', 'Pennsylvania'],
        'Midwest': ['Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Missouri', 'North Dakota', 'South Dakota', 'Nebraska', 'Kansas'],
        'South': ['Delaware', 'Maryland', 'District_of_Columbia', 'Virginia', 'West Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida', 'Kentucky', 'Tennessee', 'Mississippi', 'Alabama', 'Oklahoma', 'Texas', 'Arkansas', 'Louisiana'],
        'West': ['Idaho', 'Montana', 'Wyoming', 'Nevada', 'Utah', 'Colorado', 'Arizona', 'New Mexico', 'Alaska', 'Washington', 'Oregon', 'California', 'Hawaii']
    }
    
    state_to_region = {state: region for region, states in regions.items() for state in states}
    df['Region'] = df['LocationDesc'].map(state_to_region)
    
    df_filtered = df.dropna(subset=['Region'])
    df_filtered['Data_Value'] = df_filtered['Data_Value'].fillna(0)
    
    df_aggregated_region = df_filtered.groupby(['Region', 'Class'], as_index=False).agg({'Data_Value': 'mean'})
    df_aggregated_state = df_filtered.groupby(['LocationDesc', 'Region', 'Class'], as_index=False).agg({'Data_Value': 'mean'})
    
    return df_aggregated_region, df_aggregated_state

df_prevalence = load_prevalence_data()
df_aggregated_region, df_aggregated_state = load_engagement_data()

# Alzheimer's prevalence page
def show_overall_page():

    st.title("Overview of Alzheimer's Prevalence Across the U.S. and Self-Reported Related Concerns and Behaviors by Regions")   

    states = alt.topo_feature(data.us_10m.url, feature='states')

    selector = alt.selection_point(fields=['state'], name='Select')

    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    )

    prevalence_scale = alt.Scale(domain=[df_prevalence['Percent'].min(), df_prevalence['Percent'].max()], scheme='oranges')
    prevalence_color = alt.Color(field="Percent", type="quantitative", scale=prevalence_scale, title="Prevalence (%)")

    # Prevalence map showing Alzheimer's prevalence per state
    prevalence_map = alt.Chart(states).mark_geoshape().encode(
        color=prevalence_color,
        tooltip=[alt.Tooltip('state:N', title='State'),
                alt.Tooltip('Percent:Q', title="Prevalence (%)"),
                alt.Tooltip('Count:Q', title="Count")]  
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_prevalence, 'id', ['state', 'Percent', 'Count'])
    ).add_params(
        selector
    ).transform_filter(
        selector
    ).project('albersUsa').properties(
        title="Alzheimer's Prevalence Across U.S. States"
    )

    # Highlight the selected state
    selected_outline = alt.Chart(states).mark_geoshape(
        fill=None,  
        stroke='black',  
        strokeWidth=2
    ).transform_filter(
        selector  
    )

    # Show top 10 states by number of people with Alzheimer's
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
        title="Top 10 States by Number of People"
    )

    st.markdown('<div class="centered-chart">', unsafe_allow_html=True)
    st.altair_chart(
        alt.hconcat(
            ranking_chart.properties(width=165),
            (background + prevalence_map + selected_outline).properties(width=500)  # Set map width
        ).resolve_scale(
            color='independent'
        ),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Regional bar chart with topic selector
    topic_selection = alt.selection_point(fields=['Class'], bind='legend')  

    grouped_bar = alt.Chart(df_aggregated_region).mark_bar().encode(
        x=alt.X('Region:N', title='Region', axis=alt.Axis(labelAngle=0)),  
        y=alt.Y('Data_Value:Q', title='Percentage of Elders with the Concern(%)', scale=alt.Scale(domain=[0, 50])),
        color=alt.condition(
        topic_selection,  
        alt.Color('Class:N', title='Type of Concern'),  
        alt.value('lightgray')  
    ),
        xOffset=alt.XOffset('Class:N'),  
        tooltip=[alt.Tooltip('Region:N'), alt.Tooltip('Class:N', title='Type of Concern'), 
                 alt.Tooltip('Data_Value:Q', title='Percentage of Elders with the Concern(%)')]
    ).add_params(
        topic_selection  
    ).properties(
        width=400,  
        height=400,
        title="Regional Self-Reported Concerns Related to Alzheimer's Disease"
    )

    # State-level bar chart for selected topic
    state_bar = alt.Chart(df_aggregated_state).mark_bar().encode(
        x=alt.X('LocationDesc:N', 
                title='State', 
                sort=alt.EncodingSortField(field='Data_Value', op='mean', order='descending'),
                axis=alt.Axis(labelAngle=315, 
                            labelFontSize=12,  
                            labelOverlap=False)  
        ),  
        y=alt.Y('Data_Value:Q', title='Percentage of Elders with the Concern(%)', scale=alt.Scale(domain=[0, 50]), stack=None), 
        color=alt.Color('Class:N', title='Type of Concern'),  
        tooltip=[alt.Tooltip('LocationDesc:N', title='State'), 
                alt.Tooltip('Class:N', title='Type of Concern'), 
                alt.Tooltip('Data_Value:Q', title='Percentage of Elders with the Concern(%)')]
    ).transform_filter(
        topic_selection  
    ).properties(
        width=1000, 
        height=400,
        title="State-Level Self-Reported Concern Related to Alzheimer's Disease"
    )

    # Combine the two charts into a linked view
    st.markdown('<div class="centered-chart">', unsafe_allow_html=True)
    st.altair_chart(alt.vconcat(grouped_bar, state_bar), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

#show_overall_page()

