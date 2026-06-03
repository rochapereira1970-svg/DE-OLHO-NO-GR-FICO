import os
import json
import requests
from datetime import datetime, timedelta

# ==========================================
# BETA SETUP - DIRECT CONFIGURATION
# ==========================================
API_KEY = "SUA_CHAVE_AQUI"  # Cole a sua chave da API-Football aqui dentro das aspas
API_URL = "https://v3.football.api-sports.io"
CURRENT_MONTH_PASSWORD = "VIP2026"

HEADERS = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}

def fetch_fixtures_for_today():
    today = datetime.now().strftime('%Y-%m-%d')
    endpoint = f"{API_URL}/fixtures?date={today}"
    try:
        response = requests.get(endpoint, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('response', [])
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def analyze_and_filter_markets(fixtures):
    analyzed_games = []
    
    for item in fixtures:
        fixture_id = item['fixture']['id']
        home_team = item['teams']['home']['name']
        away_team = item['teams']['away']['name']
        league_name = item['league']['name']
        
        # TIMEZONE CORRECTION (UTC to Brasília Time UTC-3)
        # API returns: "2026-06-03T18:00:00+00:00"
        raw_date = item['fixture']['date'] 
        try:
            # Parse the API string into a datetime object
            utc_time = datetime.strptime(raw_date[:19], '%Y-%m-%dT%H:%M:%S')
            # Subtract 3 hours to convert UTC to Brasília time zone
            local_time = utc_time - timedelta(hours=3)
            match_time = local_time.strftime('%H:%M')
        except Exception:
            # Fallback split if string parsing fails
            match_time = raw_date[11:16]

        # Simple rule for Beta phase: separate into FREE and VIP games
        is_vip_game = False
        if league_name in ["Premier League", "La Liga", "Serie A", "Bundesliga", "Champions League", "Serie A - Brazil", "Serie A"]:
            is_vip_game = True

        game_payload = {
            "home_team": home_team,
            "away_team": away_team,
            "league": league_name,
            "time": match_time,
            "odds": "1.85",
            "market": "Over 2.5 Goals" if is_vip_game else "Over 1.5 Goals",
            "graph_force": "85%" if is_vip_game else "76%",
            "status": "AGENDADO",
            "score": "",
            "next_day": False,
            "is_vip": is_vip_game,
            "analysis": "Beta analysis: High volume and statistical pressure detected for this market."
        }
        analyzed_games.append(game_payload)
    return analyzed_games

def main():
    print("Starting Football Bot...")
    raw_fixtures = fetch_fixtures_for_today()
    if not raw_fixtures:
        print("No matches found or API key error.")
        return
        
    processed_games = analyze_and_filter_markets(raw_fixtures)
    
    output_data = {
        "last_update": datetime.now().strftime('%d/%m/%Y %H:%M'),
        "assertiveness": "84%",
        "greens": "0",
        "reds": "0",
        "current_gate_key": CURRENT_MONTH_PASSWORD,
        "analyzed_games": processed_games
    }
    
    # Save directly in the same folder
    with open('jogos.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    print(f"Success! Generated {len(processed_games)} matches in 'jogos.json' with timezone correction.")

if __name__ == "__main__":
    main()
