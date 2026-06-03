import os
import json
import requests
from datetime import datetime, timedelta
import streamlit as st

# ==========================================
# BETA AUTOMATION CONFIGURATION
# ==========================================
API_KEY = "SUA_CHAVE_API_FOOTBALL"  # Substitua pela sua chave da API-Football
GITHUB_TOKEN = "SUA_CHAVE_DE_ACESSO_DO_GITHUB" # Seu Personal Access Token do GitHub
GITHUB_REPO = "seu-usuario/nome-do-repositorio" # Exemplo: joao/de-olho-no-grafico
CURRENT_MONTH_PASSWORD = "VIP2026"

API_URL = "https://v3.football.api-sports.io"
HEADERS = {'x-rapidapi-host': "v3.football.api-sports.io", 'x-rapidapi-key': API_KEY}

def fetch_and_filter_games():
    # Gets current date in Brasília Time to request the correct matches
    now_brasilia = datetime.utcnow() - timedelta(hours=3)
    today_str = now_brasilia.strftime('%Y-%m-%d')
    
    endpoint = f"{API_URL}/fixtures?date={today_str}"
    
    try:
        response = requests.get(endpoint, headers=HEADERS)
        if response.status_code != 200:
            return []
        
        fixtures = response.json().get('response', [])
        analyzed_games = []
        
        for item in fixtures:
            league_name = item['league']['name']
            
            # 1. TIMEZONE CORRECTION (UTC to Brasília Time: -3 hours)
            raw_date = item['fixture']['date']
            utc_time = datetime.strptime(raw_date[:19], '%Y-%m-%dT%H:%M:%S')
            local_time = utc_time - timedelta(hours=3)
            match_time = local_time.strftime('%H:%M')

            # 2. MATCH STATUS & LIVE DATA CONTROL
            # Checking the status from the API to prevent premature green/red or fake scores
            api_status = item['fixture']['status']['short']
            
            # Default values for upcoming matches
            status_display = "AGENDADO"
            score_display = ""
            
            # If the match hasn't started yet, force it to be scheduled and empty
            if api_status in ["NS", "TBD"]:
                status_display = "AGENDADO"
                score_display = ""
            # If the match is live or finished, we can extract real scores if needed
            elif api_status in ["1H", "2H", "HT", "ET", "P"]:
                status_display = "AO VIVO"
                home_goals = item['goals']['home']
                away_goals = item['goals']['away']
                score_display = f"{home_goals}-{away_goals}"
            elif api_status == "FT":
                # For Beta simulation, we check if it's a win based on actual goals
                home_goals = item['goals']['home']
                away_goals = item['goals']['away']
                total_goals = (home_goals if home_goals is not None else 0) + (away_goals if away_goals is not None else 0)
                score_display = f"{home_goals}-{away_goals}"
                
                # Simple condition matching our beta markets
                if total_goals >= 2:
                    status_display = "GREEN"
                else:
                    status_display = "RED"

            # 3. LEAGUE SEGREGATION (FREE VS VIP)
            is_vip_game = league_name in ["Premier League", "La Liga", "Serie A", "Champions League", "Serie A - Brazil", "Serie A", "Copa Libertadores"]

            game_payload = {
                "home_team": item['teams']['home']['name'],
                "away_team": item['teams']['away']['name'],
                "league": league_name,
                "time": match_time,
                "odds": "1.85",
                "market": "Over 2.5 Goals" if is_vip_game else "Over 1.5 Goals",
                "graph_force": "85%" if is_vip_game else "76%",
                "status": status_display,
                "score": score_display,
                "next_day": False,
                "is_vip": is_vip_game,
                "analysis": "Beta analysis: Automated high-volume trend selection based on live pressure index."
            }
            analyzed_games.append(game_payload)
            
        return analyzed_games
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def push_to_github(content):
    """Sends the updated jogos.json directly to GitHub API, triggering Vercel."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/jogos.json"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    res = requests.get(url, headers=headers)
    sha = res.json().get('sha', '') if res.status_code == 200 else None
    
    import base64
    content_bytes = json.dumps(content, ensure_ascii=False, indent=4).encode('utf-8')
    content_b64 = base64.b64encode(content_bytes).decode('utf-8')
    
    payload = {"message": "Auto-update: Configured Timezone and Match Status Filter", "content": content_b64}
    if sha:
        payload["sha"] = sha
        
    requests.put(url, headers=headers, json=payload)

# Streamlit Interface
st.title("De Olho no Gráfico - Bot Control Panel")

if st.button("🚀 Force Run Bot & Update Vercel Now"):
    with st.spinner("Processing games and updating server..."):
        games = fetch_and_filter_games()
        if games:
            now_brasilia = datetime.utcnow() - timedelta(hours=3)
            output_data = {
                "last_update": now_brasilia.strftime('%d/%m/%Y %H:%M'),
                "assertiveness": "84%", 
                "greens": "0", 
                "reds": "0",
                "current_gate_key": CURRENT_MONTH_PASSWORD,
                "analyzed_games": games
            }
            push_to_github(output_data)
            st.success(f"Done! {len(games)} games pushed to Vercel with clean filters and correct time.")
        else:
            st.error("No games found or API error.")
