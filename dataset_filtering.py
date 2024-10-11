import pandas as pd
import altair as alt

file_path = 'dataset.csv'

df = pd.read_csv(file_path)

# select cognitive decline
cognitive_decline_df = df[df['Class'] == 'Cognitive Decline']
cognitive_decline_df.to_csv('cognitive_decline_df.csv', index=False) 

# select only 2022
cognitive_decline_df_22 =cognitive_decline_df[cognitive_decline_df['YearStart'] == 2022]
cognitive_decline_df_22.to_csv('cognitive_decline_df_22.csv', index=False) 