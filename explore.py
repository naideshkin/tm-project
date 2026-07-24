import os
from datetime import date, timedelta

import requests
from dotenv import load_dotenv

from load_to_postgres import load

load_dotenv()

API_KEY = os.environ["API_FOOTBALL_KEY"]
headers = {"x-apisports-key": API_KEY}

TEAM_ID = 42  # Arsenal (England)

url = "https://v3.football.api-sports.io/transfers"
params = {"team": TEAM_ID}

response = requests.get(url, headers=headers, params=params)
print("Status:", response.status_code)
print(
    "Requests limit for today:", response.headers.get("x-ratelimit-requests-remaining")
)

data = response.json()
print("Rows found:", data.get("results"))

cutoff = date.today() - timedelta(days=60)
recent_transfers = []

for player_entry in data["response"]:
    player = player_entry["player"]
    for t in player_entry["transfers"]:
        if t["date"] is None:
            continue
        transfer_date = date.fromisoformat(t["date"])
        if transfer_date >= cutoff:
            recent_transfers.append(
                {
                    "player_id": player["id"],
                    "player_name": player["name"],
                    "transfer_date": t["date"],
                    "type": t["type"],
                    "team_in": t["teams"]["in"]["name"],
                    "team_out": t["teams"]["out"]["name"],
                }
            )

print(f"Fresh transfers in last 60 days: {len(recent_transfers)}")
for r in recent_transfers:
    print(r)

load(recent_transfers)
