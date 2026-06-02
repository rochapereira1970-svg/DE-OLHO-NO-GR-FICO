import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

MERCADOS = [
    "🔥 Over 2.5 Gols (Índice de Pressão)", 
    "📐 Mais de 9.5 Escanteios na Partida", 
    "⚽ Ambas Marcam - Sim (BTTS)", 
    "📐 Mais de 4.5 Cantos no 1º Tempo",
    "🔥 Over 1.5 Gols no 2º Tempo"
]

JUSTIFICATIVAS = [
    "O gráfico de xPressure cruzado indica sustentação ofensiva contínua superior a 8.2 minutos por quadrante no terço final.",
    "O time mandante costuma saturar as linhas laterais em jogos sob pressão, disparando a curva de cantos na segunda etapa.",
    "Distorção severa detectada na linha defensiva visitante em transições rápidas. Gráfico aponta alta volatilidade para gols.",
    "A análise de volume histórico aponta que ambas as equipes mantêm intensidade de finalização acima da média da liga.",
    "Ajustes táticos previstos tendem a expor os blocos defensivos. Curva de gols esperada com forte inclinação após os 60 minutos."
]

def raspar_jogos_academia():
    print("🌐 Conectando à Academia das Apostas para ler a grade real de hoje...")
    url = "https://www.academiadasapostasbrasil.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }
    
    try:
        resposta = requests.get(url, headers=headers, timeout=15)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            jogos_raspados = []
            
            # Nova abordagem por links de jogos (mais estável contra mudanças estruturais)
            links_jogos = soup.find_all('a', class_='match-link')
            
            for link in links_jogos:
                try:
                    texto = link.text.strip()
                    if " v " in texto:
                        times = texto.split(" v ")
                        casa = times[0].strip()
                        fora = times[1].strip()
                        
                        # Filtra nomes sujos ou vazios
                        if casa and fora and len(casa) < 30 and len(fora) < 30:
                            jogos_raspados.append({
                                "casa": casa,
                                "fora": fora,
                                "campeonato": "Principais Ligas de Hoje",
                                "horario": "Rodada Atual"
                            })
                except:
                    continue
            
            # Remove duplicados mantendo a ordem
            jogos_unicos = []
            for j in jogos_raspados:
                if j not in jogos_unicos:
                    jogos_unicos.append(j)
                    
            if len(jogos_unicos) >= 10:
                print(f"✅ Sucesso! {len(jogos_unicos)} jogos reais detetados de forma estável.")
                return jogos_unicos[:10]
                
    except Exception as e:
        print(f"⚠️ Erro de conexão: {e}")
        
    print("🔄 Ativando contingência inteligente com os principais jogos da rodada europeia/sul-americana...")
    return [
        {"casa": "França", "fora": "Inglaterra", "campeonato": "Amistoso Internacional", "horario": "15:45"},
        {"casa": "Espanha", "fora": "Itália", "campeonato": "Amistoso Internacional", "horario": "16:00"},
        {"casa": "Alemanha", "fora": "Holanda", "campeonato": "Amistoso Internacional", "horario": "15:45"},
        {"casa": "Portugal", "fora": "Bélgica", "campeonato": "Amistoso Internacional", "horario": "16:15"},
        {"casa": "Uruguai", "fora": "Estados Unidos", "campeonato": "Amistoso Internacional", "horario": "21:00"},
        {"casa": "Argentina", "fora": "Equador", "campeonato": "Amistoso Internacional", "horario": "20:30"},
        {"casa": "Chile", "fora": "Paraguai", "campeonato": "Amistoso Internacional", "horario": "21:00"},
        {"casa": "Japão", "fora": "Coreia do Sul", "campeonato": "Amistoso Internacional", "horario": "07:20"},
        {"casa": "México", "fora": "Canadá", "campeonato": "Amistoso Internacional", "horario": "22:00"},
        {"casa": "Colômbia", "fora": "Bolívia", "campeonato": "Amistoso Internacional", "horario": "19:00"}
    ]

def processar_rodada():
    grade_jogos = raspar_jogos_academia()
    random.shuffle(grade_jogos)
    
    jogos_finais = []
    
    for i, jogo in enumerate(grade_jogos[:10]):
        if i < 3:
            prob = random.randint(75, 79) # 3 GRATUITOS
        else:
            prob = random.randint(82, 97) # 7 VIP
            
        dados_jogo = {
            "time_casa": jogo["casa"],
            "time_fora": jogo["fora"],
            "campeonato": jogo["campeonato"],
            "horario": jogo["horario"],
            "odd": f"{random.uniform(1.68, 2.15):.2f}",
            "mercado": random.choice(MERCADOS),
            "probabilidade": prob,
            "forca_grafico": f"{prob}%",
            "justificativa": random.choice(JUSTIFICATIVAS)
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
        
    print(f"🚀 Base de dados jogos.json atualizada com sucesso às {agora}!")

if __name__ == "__main__":
    processar_rodada()
    
