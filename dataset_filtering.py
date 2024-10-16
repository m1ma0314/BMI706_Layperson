import pandas as pd
import altair as alt

file_path = 'filtered_4topics.csv'

df = pd.read_csv(file_path)

df_prevalence = pd.read_csv("prevalence.csv")

grouped_df = df.groupby(['LocationDesc', 'Class'])['Data_Value'].mean().reset_index()
race_df = df[df['StratificationCategory2']=='Race/Ethnicity']
sex_df = df[df['StratificationCategory2']=='Gender']
race_df = race_df.groupby(['LocationDesc', 'Class', 'Stratification2'])['Data_Value'].mean().reset_index()
sex_df = sex_df.groupby(['LocationDesc', 'Class', 'Stratification2'])['Data_Value'].mean().reset_index()


# Create a new column for each state-topic combination with descriptive names
grouped_df['Column_Name'] = grouped_df['LocationDesc'] + ' ' + grouped_df['Class'] + ' Average%'

ansi = pd.read_csv('https://www2.census.gov/geo/docs/reference/state.txt', sep='|')
ansi.columns = ['id', 'abbr', 'state', 'statens']
ansi = ansi[['id', 'abbr', 'state']]

us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 
             'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 
             'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 
             'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 
             'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 
             'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 
             'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 
             'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 
             'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
             'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 
             'District of Columbia']

df['state'] = df['LocationDesc']
grouped_df['state'] = grouped_df['LocationDesc']
race_df['state'] = race_df['LocationDesc']
sex_df['state'] = sex_df['LocationDesc']


state_filtered_df = df[df['state'].isin(us_states)]

state_filtered_df = pd.merge(state_filtered_df, ansi, how='left', on='state')
state_averaged_df = pd.merge(grouped_df, ansi, how='left', on='state')
race_averaged_df = pd.merge(race_df, ansi, how='left', on='state')
sex_averaged_df = pd.merge(sex_df, ansi, how='left', on='state')

df_prevalence.rename(columns={'State': 'state'}, inplace=True)

df_prevalence = pd.merge(df_prevalence, ansi, how='left', on='state')

columns_to_keep = [
    'YearEnd', 'LocationAbbr', 'state', 'id',
     'Class', 'Topic', 'Question', 'Data_Value_Unit',
    'Data_Value_Type', 'Data_Value', 'Data_Value_Alt',
    'Data_Value_Footnote_Symbol', 'Data_Value_Footnote', 'Stratification1'
]

state_filtered_df = state_filtered_df[columns_to_keep]
state_filtered_df = state_filtered_df[state_filtered_df['Stratification1']=='65 years or older']


grouped_df.to_csv('averaged_4topics.csv', index=False)
state_averaged_df.to_csv('state_averaged_df.csv', index=False)
state_filtered_df.to_csv('state_filtered_df.csv', index=False)
df_prevalence.to_csv('prevalence_df.csv', index=False)

race_averaged_df.to_csv('race_averaged_df.csv', index=False)
sex_averaged_df.to_csv('sex_averaged_df.csv', index=False)