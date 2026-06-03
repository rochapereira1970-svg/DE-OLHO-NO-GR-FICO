import requests

API_KEY = "SUA_CHAVE_API_FOOTBALL"

url = "https://v3.football.api-sports.io/fixtures?date=2026-06-03"

headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

r = requests.get(url, headers=headers)

print(r.status_code)
print(r.json())
