import json
import requests
from datetime import datetime, timedelta

# ==========================================
# CONFIGURAÇÃO
# ==========================================
API_KEY = "SUA_CHAVE_API_FOOTBALL"
GITHUB_TOKEN = "SUA_CHAVE_DE_ACESSO_DO_GITHUB"
GITHUB_REPO = "seu-usuario/nome-do-repositorio"

API_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

# IMPORT DO ICOM
from robots.icom import calcular_icom_over15, classificar_icom


# ==========================================
# BUSCA DE JOGOS
# ==========================================
def fetch_and_filter_games():
    now_brasilia = datetime.utcnow() - timedelta(hours=3)
    today_str = now_brasilia.strftime('%Y-%m-%d')

    endpoint = f"{API_URL}/fixtures?date={today_str}"

    try:
        response = requests.get(endpoint, headers=HEADERS)

        if response.status_code != 200:
            print("Erro API:", response.text)
            return []

        fixtures = response.json().get("response", [])
        analyzed_games = []

        for item in fixtures:
            league_name = item["league"]["name"]

            # horário local
            raw_date = item["fixture"]["date"]
            utc_time = datetime.strptime(raw_date[:19], "%Y-%m-%dT%H:%M:%S")
            local_time = utc_time - timedelta(hours=3)
            match_time = local_time.strftime("%H:%M")

            api_status = item["fixture"]["status"]["short"]

            status_display = "AGENDADO"
            score_display = ""

            if api_status in ["NS", "TBD"]:
                status_display = "AGENDADO"

            elif api_status in ["1H", "2H", "HT", "ET", "P"]:
                status_display = "AO VIVO"
                home_goals = item["goals"]["home"]
                away_goals = item["goals"]["away"]
                score_display = f"{home_goals}-{away_goals}"

            elif api_status == "FT":
                home_goals = item["goals"]["home"] or 0
                away_goals = item["goals"]["away"] or 0

                total_goals = home_goals + away_goals
                score_display = f"{home_goals}-{away_goals}"

                status_display = "GREEN" if total_goals >= 2 else "RED"

            # VIP / FREE
            vip_leagues = [
                "Premier League",
                "La Liga",
                "Serie A",
                "Bundesliga",
                "Champions League",
                "Copa Libertadores"
            ]

            is_vip = league_name in vip_leagues

            # ==========================================
            # ICOM (INTELIGÊNCIA)
            # ==========================================
            icom = calcular_icom_over15(
                over15_casa=85,
                over15_fora=80,
                media_gols_casa=1.7,
                media_gols_fora=1.5,
                h2h_over15=75
            )

            classificacao = classificar_icom(icom)

            game = {
                "home_team": item["teams"]["home"]["name"],
                "away_team": item["teams"]["away"]["name"],
                "league": league_name,
                "time": match_time,
                "odds": "1.80",
                "market": "Over 1.5 Goals" if not is_vip else "Over 2.5 Goals",
                "graph_force": f"{icom}%",
                "icom_class": classificacao,
                "status": status_display,
                "score": score_display,
                "is_vip": is_vip,
                "next_day": False,
                "analysis": f"Análise ICOM automática: nível {classificacao}"
            }

            analyzed_games.append(game)

        return analyzed_games

    except Exception as e:
        print("Erro:", e)
        return []


# ==========================================
# GITHUB PUSH
# ==========================================
def push_to_github(content):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/jogos.json"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    res = requests.get(url, headers=headers)

    sha = None
    if res.status_code == 200:
        sha = res.json().get("sha")

    import base64
    data_bytes = json.dumps(content, ensure_ascii=False, indent=4).encode("utf-8")
    data_b64 = base64.b64encode(data_bytes).decode("utf-8")

    payload = {
        "message": "Atualização automática com ICOM",
        "content": data_b64
    }

    if sha:
        payload["sha"] = sha

    requests.put(url, headers=headers, json=payload)


# ==========================================
# EXECUÇÃO
# ==========================================
if __name__ == "__main__":

    games = fetch_and_filter_games()

    if games:
        output = {
            "last_update": datetime.utcnow().strftime("%d/%m/%Y %H:%M"),
            "accuracy": "0%",
            "greens": "0",
            "reds": "0",
            "analyzed_games": games
        }

        push_to_github(output)
        print("Bot executado com ICOM com sucesso!")

    else:
        print("Nenhum jogo encontrado ou erro na API")
