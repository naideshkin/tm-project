import os
import requests
from dotenv import load_dotenv

load_dotenv()
headers = {"x-apisports-key": os.environ["API_FOOTBALL_KEY"]}

url = "https://v3.football.api-sports.io/teams"
params = {"search": "arsenal"}

response = requests.get(url, headers=headers, params=params)
data = response.json()

for item in data["response"]:
    team = item["team"]
    print(team["id"], team["name"], team["country"])
