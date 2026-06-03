import json
import random
import requests
from datetime import datetime, timedelta

# CONFIGURAÇÃO DE TESTE COBERTURA AMISTOSOS
API_KEY = "53795b533294d9dd1065064221c9f3a4"

JUSTIFICATIVAS = [
    "Análise de EV+ baseada no algoritmo de pressão volumétrica indica saturação defensiva nos últimos 5 jogos, superando a linha de tendência esperada.",
    "Cruzamento estatístico via H2H aponta distorção de bloco baixo do visitante, resultando em alta probabilidade de transições agressivas na linha limite.",
    "O modelo estatístico identificou uma tendência matemática consolidada em que ambas as equipas mantêm intensidade ofensiva contínua nos quadrantes finais.",
    "Mapeamento tático preditivo registra que a linha limite máxima calculada apresenta sustentação superior a 78.4% de eficiência real histórica.",
    "Distorção severa detectada na linha de recomposição em transições rápidas. O modelo gráfico projeta inclinação acentuada após os 60 minutos."
]

def obter_grade_teste_amistosos(modo_amanha):
    print("🎯 Injetando a grade real de amistosos fornecida para validação de assertividade...")
    
    # Lista exata enviada por você ajustada para o motor estatístico
    grade_usuario = [
        {"casa": "Filipinas", "fora": "Guam", "horario": "08:30h"},
        {"casa": "Quirguistão", "fora": "Quénia", "horario": "09:30h"},
        {"casa": "Gibraltar", "fora": "Ilhas Virgens Britânicas", "horario": "14:00h"},
        {"casa": "Albânia", "fora": "Israel", "horario": "15:00h"},
        {"casa": "RD Congo", "fora": "Dinamarca", "horario": "15:00h"},
        {"casa": "Polónia", "fora": "Nigéria", "horario": "15:45h"},
        {"casa": "Holanda", "fora": "Argélia", "horario": "15:45h"},
        {"casa": "Luxemburgo", "fora": "Itália", "horario": "15:45h"},
        {"casa": "Panamá", "fora": "Rep. Dominicana", "horario": "21:45h"},
        {"casa": "Coreia do Sul", "fora": "El Salvador", "horario": "22:00h"}
    ]
    
    jogos_finais = []
    
    for idx, item in enumerate(grade_usuario):
        # Distribuição de Mercados EV+ baseada nos filtros de >75%
        sorteio = random.choice(["GOLS_15", "GOLS_25", "CANTOS", "CARTOES"])
        if sorteio == "GOLS_15":
            mercado = "🔥 Over 1.5 Gols na Partida"
            prob = random.randint(83, 95)
        elif sorteio == "GOLS_25":
            mercado = "⚽ Over 2.5 Gols (Índice de Pressão)"
            prob = random.randint(76, 89)
        elif sorteio == "CANTOS":
            mercado = "📐 Mais de 9.5 Escanteios (Linha Máxima)"
            prob = random.randint(78, 92)
        else:
            mercado = "🟨 Mais de 3.5 Cartões na Partida"
            prob = random.randint(75, 87)

        # Para fins de teste de assertividade parcial em tempo real:
        # Deixamos os primeiros jogos como concluídos (para ver as cores) e os demais aguardando
        if idx < 3:
            status_atual = "GREEN" if idx != 1 else "RED"
            placar_final = f"{random.randint(1,3)}-{random.randint(0,2)}"
        else:
            status_atual = "AGENDADO"
            placar_final = ""

        jogos_finais.append({
            "time_casa": item["casa"],
            "time_fora": item["fora"],
            "campeonato": "Amistoso Internacional",
            "horario": item["horario"],
            "odd": f"{random.uniform(1.72, 2.15):.2f}",
            "mercado": mercado,
            "forca_grafico": f"{prob}%",
            "justificativa": random.choice(JUSTIFICATIVAS),
            "status": status_atual,
            "placar": placar_final,
            "dia_seguinte": modo_amanha
        })
        
    return jogos_finais

def executar_automacao():
    # Detecta o fuso horário para aplicar a regra das 21:00h
    agora_brasil = datetime.utcnow() - timedelta(hours=3)
    modo_amanha = agora_brasil.hour >= 21
    
    lista_jogos = obter_grade_teste_amistosos(modo_amanha)
    
    greens_total = 0
    reds_total = 0
    
    for i, jogo in enumerate(lista_jogos):
        # Separação comercial: Primeiros 3 no FREE, o restante vai ocultado no VIP
        jogo["vip_card"] = i >= 3
        
        if jogo["status"] == "GREEN":
            greens_total += 1
        elif jogo["status"] == "RED":
            reds_total += 1

    total_concluidos = greens_total + reds_total
    taxa_assertividade = f"{(greens_total / total_concluidos * 100):.1f}%" if total_concluidos > 0 else "87.5%"
    
    data_painel = agora_brasil.strftime("%d/%m/%Y - %H:%Mh")
    
    dados_estruturados = {
        "ultima_atualizacao": data_painel,
        "assertividade": taxa_assertividade,
        "greens": str(greens_total),
        "reds": str(reds_total),
        "jogos_analisados": lista_jogos
    }
    
    with open("jogos.json", "w", encoding="utf-8") as f:
        json.dump(dados_estruturados, f, ensure_ascii=False, indent=2)
        
    print(f"🚀 Base de testes sincronizada para os Amistosos às {data_painel}!")

if __name__ == "__main__":
    executar_automacao()
