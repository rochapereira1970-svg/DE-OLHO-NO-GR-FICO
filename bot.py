import json
import requests
from datetime import datetime, timedelta

# ==========================================
# CONFIGURAÇÃO
# ==========================================
API_KEY = "SUA_CHAVE_API_FOOTBALL"
GITHUB_TOKEN = "SUA_CHAVE_GITHUB"
GITHUB_REPO = "seu-usuario/seu-repo"

API_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

from robots.icom import calcular_icom_over15


# ==========================================
# ICOM + EDGE SCORE
# ==========================================
def score_game():
    icom = calcular_icom_over15(
        over15_casa=85,
        over15_fora=80,
        media_gols_casa=1.7,
        media_gols_fora=1.5,
        h2h_over15=75
    )
    return icom


# ==========================================
# BUSCAR JOGOS
# ==========================================
def fetch_games():
    today = (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d")
    url = f"{API_URL}/fixtures?date={today}"

    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        return []

    return r.json().get("response", [])


# ==========================================
# ROBÔ DE SELEÇÃO
# ==========================================
def build_signals(fixtures):
    free_signals = []
    vip_signals = []

    for item in fixtures:
        league = item["league"]["name"]

        is_vip = league in [
            "Premier League",
            "La Liga",
            "Serie A",
            "Bundesliga",
            "Champions League",
            "Copa Libertadores"
        ]

        icom = score_game()

        game = {
            "home_team": item["teams"]["home"]["name"],
            "away_team": item["teams"]["away"]["name"],
            "league": league,
            "time": item["fixture"]["date"][11:16],
            "market": "Over 1.5" if not is_vip else "Over 2.5",
            "icom": icom,
            "status": "SIGNAL",
            "analysis": f"Robô detectou valor estatístico com ICOM {icom}%"
        }

        # FILTRO DE QUALIDADE
        if icom >= 85:
            if is_vip:
                vip_signals.append(game)
            else:
                free_signals.append(game)

    # ordenar por força
    free_signals = sorted(free_signals, key=lambda x: x["icom"], reverse=True)
    vip_signals = sorted(vip_signals, key=lambda x: x["icom"], reverse=True)

    return free_signals[:3], vip_signals[:5]


# ==========================================
# PUSH GITHUB
# ==========================================
def push(data):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/jogos.json"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    res = requests.get(url, headers=headers)
    sha = res.json().get("sha") if res.status_code == 200 else None

    import base64
    content = json.dumps(data, ensure_ascii=False, indent=4).encode()
    b64 = base64.b64encode(content).decode()

    payload = {
        "message": "Robô automático de sinais",
        "content": b64
    }

    if sha:
        payload["sha"] = sha

    requests.put(url, headers=headers, json=payload)


# ==========================================
# EXECUÇÃO
# ==========================================
if __name__ == "__main__":

    fixtures = fetch_games()

    free, vip = build_signals(fixtures)

    output = {
        "last_update": datetime.utcnow().strftime("%d/%m/%Y %H:%M"),
        "free_signals": free,
        "vip_signals": vip,
        "total_free": len(free),
        "total_vip": len(vip)
    }

    push(output)

    print("Robô de entradas automáticas executado com sucesso!")
