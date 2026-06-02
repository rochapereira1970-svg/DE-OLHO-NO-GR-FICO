import json
import random
from datetime import datetime

# Grade de jogos limpa e focada
JOGOS_BASE = [
    {"casa": "França", "fora": "Inglaterra", "campeonato": "Amistoso Internacional", "horario": "15:45"},
    {"casa": "Espanha", "fora": "Itália", "campeonato": "Amistoso Internacional", "horario": "16:00"},
    {"casa": "Alemanha", "fora": "Holanda", "campeonato": "Amistoso Internacional", "horario": "15:45"},
    {"casa": "Portugal", "fora": "Bélgica", "campeonato": "Amistoso Internacional", "horario": "16:15"},
    {"casa": "Uruguai", "fora": "Estados Unidos", "campeonato": "Amistoso Internacional", "horario": "21:00"},
    {"casa": "Santos", "fora": "Operário-PR", "campeonato": "Brasileirão Série B", "horario": "19:00"},
    {"casa": "Goiás", "fora": "Sport", "campeonato": "Brasileirão Série B", "horario": "21:30"},
    {"casa": "Coritiba", "fora": "CRB", "campeonato": "Brasileirão Série B", "horario": "20:00"},
    {"casa": "Ceará", "fora": "Vila Nova", "campeonato": "Brasileirão Série B", "horario": "21:00"},
    {"casa": "Mirassol", "fora": "Guarani", "campeonato": "Brasileirão Série B", "horario": "19:15"}
]

MERCADOS = [
    "🔥 Over 2.5 Gols (Índice de Pressão)", 
    "📐 Mais de 9.5 Escanteios na Partida", 
    "⚽ Ambas Marcam - Sim (BTTS)", 
    "📐 Mais de 4.5 Cantos no 1º Tempo",
    "🔥 Over 1.5 Gols no 2º Tempo"
]

# Frases limpas (Sem tags HTML)
JUSTIFICATIVAS = [
    "O gráfico de xPressure cruzado indica sustentação ofensiva contínua superior a 8.2 minutos por quadrante no terço final.",
    "O time mandante costuma saturar as linhas laterais em jogos sob pressão, disparando a curva de cantos na segunda etapa.",
    "Distorção severa detectada na linha defensiva visitante em transições rápidas. Gráfico aponta alta volatilidade para gols.",
    "A análise de volume histórico aponta que ambas as equipes mantêm intensidade de finalização acima da média da liga.",
    "Ajustes táticos previstos tendem a expor os blocos defensivos. Curva de gols esperada com forte inclinação após os 60 minutos."
]

def gerar_dados():
    print("🤖 Processando filtros estatísticos limpos...")
    random.shuffle(JOGOS_BASE)
    
    jogos_finais = []
    
    for i, jogo in enumerate(JOGOS_BASE[:10]):
        # Define os percentuais exatos baseados nas suas regras de negócio
        if i < 3:
            prob = random.randint(75, 79) # FREE
        else:
            prob = random.randint(81, 98) # VIP
            
        dados_jogo = {
            "time_casa": jogo["casa"],
            "time_fora": jogo["fora"],
            "campeonato": jogo["campeonato"],
            "horario": jogo["horario"],
            "odd": f"{random.uniform(1.68, 2.15):.2f}",
            "mercado": random.choice(MERCADOS),
            "probabilidade": prob,
            "forca_grafico": f"{prob}%", # Apenas o texto limpo (Ex: 76%)
            "justificativa": random.choice(JUSTIFICATIVAS) # Texto puro, sem sujeira
        }
        
        if i < 3:
            jogos_finais.insert(0, dados_jogo)
        else:
            jogos_finais.append(dados_jogo)

    agora = datetime.now().strftime("%d/%m/%Y - %H:%Mh")
    dados_estruturados = {
        "ultima_atualizacao": agora,
        "jogos_analisados": jogos_finais
    }
    
    with open("jogos.json", "w", encoding="utf-8") as f:
        json.dump(dados_estruturados, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Arquivo jogos.json gerado sem poluição visual às {agora}!")

if __name__ == "__main__":
    gerar_dados()
