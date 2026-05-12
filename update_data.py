import requests
import pandas as pd
from datetime import datetime
import os

print("Starting global epi data fetch...")

# === GLOBAL KEY INDICATORS (OWID) ===
def fetch_global_owid():
    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        df = pd.read_csv(url, low_memory=False)
        latest = df.sort_values('date').groupby('location').last().reset_index()
        cols = ['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 
                'new_deaths', 'total_vaccinations', 'people_fully_vaccinated', 'population']
        latest = latest[cols]
        print(f"✅ OWID data: {len(latest)} locations")
        return latest
    except Exception as e:
        print(f"OWID error: {e}")
        return pd.DataFrame()

# === SIGNIFICANT EVENTS (WHO) ===
def fetch_who_events():
    try:
        r = requests.get("https://www.who.int/api/news/diseaseoutbreaknews", timeout=15)
        if r.status_code == 200:
            data = r.json().get('value', [])
            df = pd.DataFrame(data)
            if not df.empty:
                print(f"✅ WHO events: {len(df)} found")
                return df.head(20)
    except Exception as e:
        print(f"WHO error: {e}")
    return pd.DataFrame()

# === SAVE ===
if __name__ == "__main__":
    global_data = fetch_global_owid()
    events = fetch_who_events()
    
    os.makedirs("data", exist_ok=True)
    global_data.to_csv("data/global_indicators.csv", index=False)
    events.to_csv("data/significant_events.csv", index=False)
    
    print(f"✅ Dashboard updated at {datetime.now()}")
