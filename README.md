import requests
import pandas as pd
from datetime import datetime
import os

# === GLOBAL KEY INDICATORS (OWID) ===
def fetch_global_owid():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    # Keep latest global snapshot + key columns
    latest = df.sort_values('date').groupby('location').last().reset_index()
    latest = latest[['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 
                     'total_vaccinations', 'people_fully_vaccinated', 'population']]
    return latest

# === SIGNIFICANT EPIDEMIOLOGICAL EVENTS (WHO) ===
def fetch_who_events():
    try:
        r = requests.get("https://www.who.int/api/news/diseaseoutbreaknews", timeout=20)
        if r.status_code == 200:
            data = r.json().get('value', [])
            df = pd.DataFrame(data)
            if not df.empty:
                df = df[['title', 'description', 'date', 'countries']].head(20)  # recent events
                return df
    except:
        pass
    return pd.DataFrame(columns=['title', 'description', 'date', 'countries'])

# === RUN & SAVE ===
if __name__ == "__main__":
    print("Fetching global epi data...")
    global_data = fetch_global_owid()
    events = fetch_who_events()
    
    os.makedirs("data", exist_ok=True)
    global_data.to_csv("data/global_indicators.csv", index=False)
    events.to_csv("data/significant_events.csv", index=False)
    
    print(f"✅ Global dashboard updated at {datetime.now()}")
    print(f"   • Global indicators: {len(global_data)} countries")
    print(f"   • Significant events: {len(events)} recent outbreaks")
