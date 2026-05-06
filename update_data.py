import pandas as pd
import requests
from datetime import datetime

print('Fetching latest epidemiological data from Our World in Data...')

# Main OWID COVID-19 dataset - very reliable and updated frequently
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Filter Australia data (very crisp & focused)
aus_df = df[df['iso_code'] == 'AUS'].copy()

# Save files
aus_df.to_csv('data/au_latest_epi.csv', index=False)
df.to_csv('data/global_latest_epi.csv', index=False)

print(f'Success! Saved {len(aus_df)} rows of Australia epi data.')
print('Files ready for your dashboard.')