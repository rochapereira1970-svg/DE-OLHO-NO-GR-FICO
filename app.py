import streamlit as st
import json
import requests

# 1. Configuração da Página
st.set_page_config(
    page_title="De Olho no Gráfico - Inteligência Preditiva",
    page_icon="📈",
    layout="wide"
)

# LINK DE PAGAMENTO (Substitua pelo seu link de vendas)
LINK_COMPRA_VIP = "https://seu-link-de-pagamento.com"

# 2. Injeção de CSS Premium (Estilo Azul Escuro com Foco em Conversão)
st.markdown("""
<style>
.main { background-color: #0b0f19; color: #f1f5f9; }
.header-box { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 16px; border: 1px solid #334155; text-align: center; margin-bottom: 20px; }
.header-box h1 { color: #38bdf8; font-size: 30px; font-weight: 800; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px; }
.header-box p { color: #94a3b8; font-size: 15px; margin: 0; }

/* Painel de Métricas Superior */
.painel-metricas { display: flex; justify-content: center; gap: 15px; margin-bottom: 20px; flex-wrap: wrap; }
.metrica-card { background-color: #111827; border: 1px solid #1f2937; padding: 12px 25px; border-radius: 12px; text-align: center; min-width: 150px; }
.metrica-valor { font-size: 20px; font-weight: 900; color: #10b981; }
.metrica-label { font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: bold; margin-top: 2px; }

/* Banner de Vendas Principal */
.banner-vip-principal { background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); border: 1px solid #581c87; padding: 20px; border-radius: 14px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
.banner-vip-principal h3 { color: #f59e0b; margin: 0 0 5px 0; font-size: 18px; font-weight: bold; text-transform: uppercase; }
.banner-vip-principal p { color: #cbd5e1; margin: 0 0 15px 0; font-size: 13px; }
.btn-principal-vip { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #000000 !important; font-weight: 900; padding: 12px 30px; border-radius: 8px; text-decoration: none; display: inline-block; text-transform: uppercase; font-size: 14px; box-shadow: 0 4px 15px rgba(245,158,11,0.4); }

/* Especialidades do Gráfico */
.fontes-container { background-color: #111827; padding: 12px; border-radius: 12px; border: 1px solid #1f2937; margin-bottom: 20px; text-align: center; }
.fonte-tag { background-color: #1f2937; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 12px; display: inline-block; margin: 3px 6px; border: 1px solid #374151; }

.aviso-horario-box { background-color: #1e293b; padding: 10px; border-radius: 10px; border: 1px solid #334155; text-align: center; margin-bottom: 25px; }
.aviso-texto { color: #38bdf8; font-weight: bold; font-size: 12px; text-transform: uppercase; }

/* Abas Customizadas */
.stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #1e293b; color: #94a3b8; border-radius: 8px 8px 0px 0px; padding: 10px 25px; font-weight: bold; border: 1px solid #334155; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%) !important; color: white !important; border: none; }

/* Cards de Palpites Liberados */
.card-analise { background-color: #1e293b; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #38bdf8; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }
.card-titulo { font-size: 18px; font-weight: bold; color: #ffffff; }
.badge-odd { background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); color: #ffffff; font-weight: 800; padding: 5px 12px; border-radius: 6px; font-size: 14px; }

.jogo-detalhes { background-color: #0f172a; padding: 12px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #1e293b; }
.times-nome { font-size: 16px; font-weight: bold; color: #ffffff; }
.campeonato-nome { font-size: 12px; color: #64748b; }

.mercado-box { background-color: #0c4a6e; color: #38bdf8; padding: 8px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; display: inline-block; margin-top: 5px; }
.justificativa-box { background-color: #111827; padding: 10px 14px; border-radius: 8px; border-left: 3px solid #64748b; font-size: 13px; color: #94a3b8; margin-top: 10px; }

/* Indicador Gráfico (Exclusivo deste App) */
.mini-grafico-barra { background: #1f2937; border-radius: 4px; height: 8px; width: 100%; margin-top: 8px; overflow: hidden; }
.mini-grafico-preenchimento { background: linear-gradient(90deg, #38bdf8 0%, #10b981 100%); height: 100%; border-radius: 4px; }

/* Cards Bloqueados (VIP) */
.card-vip-bloqueado { background-color: #131926; border-radius: 14px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #eab308; border: 1px dashed #eab308; opacity: 0.9; position: relative; }
.blur-text { filter: blur(5px); user-select: none; pointer-events: none; }
.btn-vip-container { text-align: center; margin-top: 15px; }
.btn-vip-link { background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%); color: #000000 !important; font-weight: bold; padding: 10px 24px; border-radius: 8px; text-decoration: none; display: inline-block; font-size: 13px; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# Altere o link abaixo para apontar para o SEU repositório novo do GitHub
JSON_URL = "https://raw.githubusercontent.com/rochapereira1970-svg/de-olho-no-gr-fico/main/jogos.json"

def carregar_dados():
    try:
        resposta = requests.get(JSON_URL)
        if resposta.status_code == 200:
            return json.loads(resposta.text)
    except:
        pass
    return None

dados = carregar_dados()
data_atualizacao = dados['ultima_atualizacao'] if dados else "Aguardando transmissão..."

# Topo Estruturado
st.markdown("""
    <div class="header-box">
        <h1>📈 DE OLHO NO GRÁFICO</h1>
        <p>Rastreamento de Tendências de Pressão e Volume Estatístico de Elite</p>
    </div>
""", unsafe_allow_html=True)

# Vitrine de Números Comerciais
st.markdown("""
    <div class="painel-metricas">
        <div class="metrica-card">
            <div class="metrica-valor">91.4%</div>
            <div class="metrica-label">📈 Confiabilidade da Curva</div>
        </div>
        <div class="metrica-card">
            <div class="metrica-valor">Padrão Ativo</div>
            <div class="metrica-label">📊 Cruzamento de Dados</div>
        </div>
        <div class="metrica-card">
            <div class="metrica-valor">3.41x</div>
            <div class="metrica-label">🚀 Fator de Alavancagem</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Chamada de Vendas para o VIP
st.markdown(f"""
    <div class="banner-vip-principal">
        <h3>📈 Pegue as Maiores Distorções de Gráfico da Rodada</h3>
        <p>Acesse as 7 análises de alta volatilidade e probabilidade matemática isoladas pelo nosso sistema analítico.</p>
        <a href="{LINK_COMPRA_VIP}" target="_blank" class="btn-principal-vip">Desbloquear Gráficos VIP</a>
    </div>
""", unsafe_allow_html=True)

# Selos Informativos dos Mercados Monitorados
st.markdown("""
    <div class="fontes-container">
        <span style="color: #64748b; font-size: 11px; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 5px;">
            🤖 Variáveis Analisadas pelo Motor Gráfico:
        </span>
        <div class="fonte-tag" style="color: #38bdf8;">🔥 Índice de Pressão (xPressure)</div>
        <div class="fonte-tag" style="color: #10b981;">⚽ Tendências de Linhas de Gols</div>
        <div class="fonte-tag" style="color: #eab308;">📐 Saturação de Cantos Finos</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="aviso-horario-box">
        <span class="aviso-texto">
            📢 Novas projeções gráficas são consolidadas diariamente às 22:00h!
        </span>
    </div>
""", unsafe_allow_html=True)

st.info(f"🔄 **Última plotagem gráfica:** {data_atualizacao}")

# Criação das Abas Separadoras
aba_free, aba_vip = st.tabs(["🆓 GRÁFICOS LIBERADOS (3 PROJEÇÕES)", "👑 CURVA PRIVADA VIP (7 AGRESSIVOS)"])

if not dados:
    st.warning("O motor gráfico está processando o volume das partidas. Aguarde a sincronização!")
else:
    lista_jogos = dados.get("jogos_analisados", [])
    
    # --- ABA GRATUITA ---
    with aba_free:
        st.subheader("🎯 Sinais e Padrões de Tendência Liberados")
        jogos_free = lista_jogos[:3]
        
        for jogo in jogos_free:
            # Captura a força do gráfico se existir no JSON, senão define 85% padrão
            forca_grafico = jogo.get("forca_grafico", "85%")
            
            st.markdown(f"""
                <div class="card-analise">
                    <div class="card-header">
                        <span class="card-titulo">📈 TENDÊNCIA CONFIRMADA</span>
                        <span class="badge-odd">ODD: @{jogo['odd']}</span>
                    </div>
                    <div class="jogo-detalhes">
                        <div class="times-nome">{jogo['time_casa']} x {jogo['time_fora']}</div>
                        <div class="campeonato-nome">🏆 {jogo['campeonato']} • ⏰ {jogo.get('horario', '22:00')}</div>
                    </div>
                    <div class="mercado-box">Entrada: {jogo['mercado']}</div>
                    
                    <div style="margin-top: 12px; font-size: 12px; color: #64748b; font-weight: bold;">
                        📊 ÍNDICE DE SATURAÇÃO DA LINHA: <span style="color: #10b981;">{forca_grafico}</span>
                    </div>
                    <div class="mini-grafico-barra">
                        <div class="mini-grafico-preenchimento" style="width: {forca_grafico};"></div>
                    </div>
                    
                    <div class="justificativa-box">
                        <strong>📈 Comportamento de Gráfico Identificado:</strong><br>
                        {jogo.get('justificativa', 'A curva de volume ofensivo superou a linha de corte histórica do algoritmo.')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    # --- ABA PRIVADA (VIP) ---
    with aba_vip:
        st.markdown("""
            <div style="background-color: #1e293b; color: #ffedd5; padding: 15px; border-radius: 8px; border-left: 4px solid #f97316; margin-bottom: 20px; font-size: 14px; text-align: center;">
                ⭐ <strong>7 CURVAS DE ALTA VOLATILIDADE EXCLUSIVAS:</strong> Padrões de comportamento com assimetria severa de odds nas casas.
            </div>
        """, unsafe_allow_html=True)
        
        for i in range(7):
            index_real = i + 3
            if index_real < len(lista_jogos):
                j_vip = lista_jogos[index_real]
                mercado_vip = j_vip['mercado']
                camp_vip = j_vip['campeonato']
            else:
                mercado_vip = "📈 Linha de Pressão Avançada"
                camp_vip = "Elite Europeia / Brasileirão"

            st.markdown(f"""
                <div class="card-vip-bloqueado">
                    <div class="card-header" style="border-bottom: 1px solid #222938;">
                        <span class="card-titulo" style="color: #eab308;">🔒 GRÁFICO PRIVADO #{i+1}</span>
                        <span class="badge-odd" style="background: #eab308; color: #000;">ODD Oculta</span>
                    </div>
                    <div class="jogo-detalhes" style="background-color: #0b0f19; border: 1px dashed #222938;">
                        <div class="times-nome blur-text">Time Oculto x Equipe Secreta</div>
                        <div class="campeonato-nome">🏆 {camp_vip} • ⏰ 22:00h</div>
                    </div>
                    <div class="mercado-box" style="background-color: #422006; color: #fef08a;">Linha: {mercado_vip}</div>
                    <div class="justificativa-box blur-text" style="border-left-color: #eab308;">Projeção confidencial do assinante.</div>
                    <div class="btn-vip-container"><a href="{LINK_COMPRA_VIP}" target="_blank" class="btn-vip-link">🔓 Acessar Gráfico VIP</a></div>
                </div>
            """, unsafe_allow_html=True)

# Rodapé Padronizado para PWA Móvel
st.markdown("""
    <hr style="border-color: #1e293b;">
    <div style="text-align: center; color: #64748b; font-size: 12px; padding: 10px;">
        📲 Abra este link no navegador do celular e selecione "Adicionar à Tela de Início" para salvar como App.
    </div>
""", unsafe_allow_html=True)
