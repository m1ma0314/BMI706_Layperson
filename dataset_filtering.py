import pandas as pd
import altair as alt

file_path = 'dataset.csv'

df = pd.read_csv(file_path)

df_prevalence = pd.read_csv("prevalence.csv")

ansi = pd.read_csv('https://www2.census.gov/geo/docs/reference/state.txt', sep='|')
ansi.columns = ['id', 'abbr', 'state', 'statens']
ansi = ansi[['id', 'abbr', 'state']]



# select cognitive decline
cognitive_decline_df = df[df['Class'] == 'Cognitive Decline']


# select only 2022
cognitive_decline_df_22 =cognitive_decline_df[cognitive_decline_df['YearEnd'] == 2022]

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

cognitive_decline_df_22.rename(columns={'LocationDesc': 'state'}, inplace=True)
cognitive_decline_df.to_csv('cognitive_decline_df.csv', index=False) 

state_filtered_df = cognitive_decline_df_22[cognitive_decline_df_22['state'].isin(us_states)]

state_filtered_df = pd.merge(state_filtered_df, ansi, how='left', on='state')


#non_state_filtered_df = cognitive_decline_df_22[~cognitive_decline_df['LocationDesc'].isin(us_states)]

#sorted_us_states = sorted(us_states)

#state_id_mapping = {state: idx + 1 for idx, state in enumerate(sorted_us_states)}
#state_filtered_df['StateID'] = state_filtered_df['LocationDesc'].map(state_id_mapping)

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


cognitive_decline_df_22.to_csv('cognitive_decline_df_22.csv', index=False) 
state_filtered_df.to_csv('state_filtered_df.csv', index=False)
df_prevalence.to_csv('prevalence_df.csv', index=False)

max_percentage_df = state_filtered_df.loc[state_filtered_df.groupby('state')['Data_Value'].idxmax()]

max_percentage_df.to_csv('max_percentage_df.csv', index=False)