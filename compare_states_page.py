import altair as alt
import pandas as pd
import streamlit as st


def show_compare_states_page():
                       
    # Load datasets (adjust paths as necessary)
    sex_data = pd.read_csv('sex_averaged_df.csv')
    race_data = pd.read_csv('race_averaged_df.csv')
    overall_data = pd.read_csv('state_averaged_df.csv')

    df_prevalence = pd.read_csv('prevalence_df.csv')
    df_prevalence['Count'] = df_prevalence['Number (in thousands)'] * 1000

    # Ensure LocationDesc and other necessary columns exist
    assert 'LocationDesc' in sex_data.columns, "LocationDesc not found in sex_data!"
    assert 'Class' in sex_data.columns, "Class column missing in sex_data!"
    assert 'Data_Value' in sex_data.columns, "Data_Value column missing in sex_data!"
    assert 'Stratification2' in sex_data.columns, "Stratification2 column missing in sex_data!"



    # Create two columns for the selectors
    col1_select, col2_select = st.columns(2)

    # Streamlit Selectbox for State 1 (left column)
    with col1_select:
        state_1 = st.selectbox('Select State 1:', sex_data['LocationDesc'].unique(), index=0)

    # Streamlit Selectbox for State 2 (right column)
    with col2_select:
        state_2 = st.selectbox('Select State 2:', sex_data['LocationDesc'].unique(), index=1)



    # Alzheimer's disease data for the selected states
    alz_state_1 = df_prevalence[df_prevalence['state'] == state_1]
    alz_state_2 = df_prevalence[df_prevalence['state'] == state_2]

    col1_prevalence, col2_prevalence = st.columns(2)

    # Display Prevalence for State 1
    with col1_prevalence:
        if not alz_state_1.empty:
            prevalence_1 = alz_state_1.iloc[0]['Percent']
            number_affected_1 = int(alz_state_1.iloc[0]['Count'])
            st.markdown(f"#### Prevalence of Alzheimer's Disease: {prevalence_1}%")
            st.markdown(f"#### Number of People with Alzheimer's Disease: {number_affected_1}")
        else:
            st.write(f"No data available for {state_1}")

    # Display Prevalence for State 2
    with col2_prevalence:
        #st.markdown(f"#### {prevalence_2}%")
        if not alz_state_2.empty:
            prevalence_2 = alz_state_2.iloc[0]['Percent']
            number_affected_2 = int(alz_state_2.iloc[0]['Count'])
            st.markdown(f"#### Prevalence of Alzheimer's Disease: {prevalence_2}%")
            st.markdown(f"#### Number of People with Alzheimer's Disease: {number_affected_2}")
        else:
            st.write(f"No data available for {state_2}")

    st.markdown(f"---")

    # Create two columns in Streamlit for the charts
    col1, col2 = st.columns(2)

    # Filter data based on the selected states
    sex_data_state_1 = sex_data[sex_data['LocationDesc'] == state_1]
    sex_data_state_2 = sex_data[sex_data['LocationDesc'] == state_2]
    race_data_state_1 = race_data[race_data['LocationDesc'] == state_1]
    race_data_state_2 = race_data[race_data['LocationDesc'] == state_2]

    overall_data_1 = overall_data[overall_data['LocationDesc'] == state_1]
    overall_data_2 = overall_data[overall_data['LocationDesc'] == state_2]

    # Function to create charts
    def create_plots():

        # Bar chart for overall comparison for State 1
        bar_chart_state_1 = alt.Chart(overall_data_1).mark_bar().encode(
            x=alt.X('Class:N', title='Topics', axis=alt.Axis(labelLimit=200, labelAngle=315, labelFontSize=12, labelOverlap=False)),
            y=alt.Y('Data_Value:Q', title='Average %'),
            color='Class:N',
            tooltip=['Class', 'Data_Value']
        ).properties(
            title=f'Average % by Topic for {state_1}'
        )

        # Bar chart for overall comparison for State 2
        bar_chart_state_2 = alt.Chart(overall_data_2).mark_bar().encode(
            x=alt.X('Class:N', title='Topics', axis=alt.Axis(labelLimit=200, labelAngle=315, labelFontSize=12, labelOverlap=False)),
            y=alt.Y('Data_Value:Q', title='Average %'),
            color='Class:N',
            tooltip=['Class', 'Data_Value']
        ).properties(
            title=f'Average % by Topic for {state_2}'
        )

        # Bar chart for Sex data comparison for State 1
        bar_chart_sex_1 = alt.Chart(sex_data_state_1).mark_bar(size=30).encode(
            x=alt.X('Class:N', title='Topics', axis=alt.Axis(labelLimit=200, labelAngle=315, labelFontSize=12, labelOverlap=False)),
            xOffset='Stratification2',
            y=alt.Y('Data_Value:Q', title='Average %'),
            color='Stratification2:N',
            tooltip=['Class', 'Stratification2', 'Data_Value']
        ).configure_view(
            stroke=None,
        ).properties(
            title=f'Average % by Topic and Sex for {state_1}'
        )

        # Bar chart for Sex data comparison for State 2
        bar_chart_sex_2 = alt.Chart(sex_data_state_2).mark_bar().encode(
            x=alt.X('Class:N', title='Topics', axis=alt.Axis(labelLimit=200, labelAngle=315, labelFontSize=12, labelOverlap=False)),
            xOffset='Stratification2',
            y=alt.Y('Data_Value:Q', title='Average %'),
            color='Stratification2:N',
            tooltip=['Class', 'Stratification2', 'Data_Value']
        ).configure_view(
            stroke=None,
        ).properties(
            title=f'Average % by Topic and Sex for {state_2}'
        )

        # Bar chart for Race data comparison for State 1
        bar_chart_race_1 = alt.Chart(race_data_state_1).mark_bar().encode(
            x=alt.X('Class:N', title='Topics', axis=alt.Axis(labelLimit=200, 
                    labelAngle=315, labelFontSize=12, labelOverlap=False)),
            xOffset='Stratification2',
            y=alt.Y('Data_Value', axis=alt.Axis(grid=False), title='Average %'),
            color=alt.Color('Stratification2', legend=alt.Legend(orient='top')),
            tooltip=['Class', 'Stratification2', 'Data_Value']
        ).configure_view(
            stroke=None,
        ).properties(
            title=f'Average % by Topic and Race for {state_1}'
        )

        # Bar chart for Race data comparison for State 2
        bar_chart_race_2 = alt.Chart(race_data_state_2).mark_bar().encode(
            x=alt.X('Class:N', title='Topics', axis=alt.Axis(labelLimit=200, 
                    labelAngle=315, labelFontSize=12, labelOverlap=False)),
            xOffset='Stratification2',
            y=alt.Y('Data_Value', axis=alt.Axis(grid=False), title='Average %'),
            color=alt.Color('Stratification2', legend=alt.Legend(orient='top')),
            tooltip=['Class', 'Stratification2', 'Data_Value']
        ).configure_view(
            stroke=None,
        ).properties(
            title=f'Average % by Topic and Race for {state_2}'
        )

        # Render charts in columns

        # State 1 Charts
        with col1:
            st.altair_chart(bar_chart_state_1, use_container_width=True)
            st.markdown(f"---")
            st.altair_chart(bar_chart_sex_1, use_container_width=True)
            st.markdown(f"---")
            st.altair_chart(bar_chart_race_1, use_container_width=True)

        # State 2 Charts
        with col2:
            st.altair_chart(bar_chart_state_2, use_container_width=True)
            st.markdown(f"---")
            st.altair_chart(bar_chart_sex_2, use_container_width=True)
            st.markdown(f"---")
            st.altair_chart(bar_chart_race_2, use_container_width=True)

    # Call the function to create plots
    create_plots()

#show_compare_states_page()