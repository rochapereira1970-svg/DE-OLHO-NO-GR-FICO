import json
from datetime import datetime

def generate_fake_games():
    return [
        {
            "home_team": "Time A",
            "away_team": "Time B",
            "league": "Teste",
            "time": "18:00",
            "market": "Over 1.5",
            "graph_force": "88",
            "status": "TESTE",
            "score": "",
            "is_vip": False,
            "analysis": "Modo teste ativo para validar sistema"
        },
        {
            "home_team": "Time C",
            "away_team": "Time D",
            "league": "Teste VIP",
            "time": "20:00",
            "market": "Over 2.5",
            "graph_force": "91",
            "status": "TESTE",
            "score": "",
            "is_vip": True,
            "analysis": "Modo VIP teste ativo"
        }
    ]

def run():

    games = generate_fake_games()

    data = {
        "last_update": datetime.utcnow().strftime("%d/%m/%Y %H:%M"),
        "accuracy": "TESTE",
        "greens": "0",
        "reds": "0",
        "analyzed_games": games
    }

    with open("jogos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Sistema funcionando em modo teste!")

if __name__ == "__main__":
    run()
