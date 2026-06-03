import streamlit as st
import json

# ==========================================
# CARREGAR DADOS
# ==========================================
def load_data():
    try:
        with open("jogos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"analyzed_games": []}


data = load_data()
games = data.get("analyzed_games", [])

# ==========================================
# CONVERSÃO DE ICOM
# ==========================================
def get_icom(game):
    try:
        return float(game.get("graph_force", "0").replace("%", ""))
    except:
        return 0


# ==========================================
# FILTROS
# ==========================================
free_games = [g for g in games if not g.get("is_vip")]
vip_games = [g for g in games if g.get("is_vip")]


# ordenar por ICOM
free_games = sorted(free_games, key=get_icom, reverse=True)
vip_games = sorted(vip_games, key=get_icom, reverse=True)


top_free = free_games[:3]
top_vip = vip_games[:10]


# ==========================================
# UI
# ==========================================
st.set_page_config(page_title="DE OLHO NO GRÁFICO", layout="wide")

st.title("📊 DE OLHO NO GRÁFICO - PAINEL DE SINAIS")

st.markdown("---")

# ==========================================
# RESUMO
# ==========================================
st.subheader("📈 Resumo do Dia")

col1, col2, col3 = st.columns(3)

col1.metric("Total Jogos", len(games))
col2.metric("FREE", len(free_games))
col3.metric("VIP", len(vip_games))

st.markdown("---")


# ==========================================
# TOP FREE
# ==========================================
st.subheader("🟢 TOP 3 FREE (Melhores oportunidades do dia)")

if top_free:
    for g in top_free:
        st.markdown(f"""
        ### {g['home_team']} x {g['away_team']}
        - 🕒 {g['time']}
        - 📊 ICOM: **{g['graph_force']}**
        - 🎯 Mercado: {g['market']}
        - 🏆 Status: {g['status']}
        - 🧠 Análise: {g['analysis']}
        """)
        st.markdown("---")
else:
    st.info("Sem jogos FREE disponíveis")


# ==========================================
# TOP VIP
# ==========================================
st.subheader("🔥 TOP 10 VIP (Alta precisão + mercados avançados)")

if top_vip:
    for g in top_vip:
        st.markdown(f"""
        ### {g['home_team']} x {g['away_team']}
        - 🕒 {g['time']}
        - 📊 ICOM: **{g['graph_force']}**
        - 🎯 Mercado: {g['market']}
        - 🏆 Status: {g['status']}
        - 🧠 Análise: {g['analysis']}
        """)
        st.markdown("---")
else:
    st.info("Sem jogos VIP disponíveis")


# ==========================================
# LISTA COMPLETA (OPCIONAL)
# ==========================================
with st.expander("📋 Ver todos os jogos"):
    for g in games:
        st.write(
            f"{g['home_team']} x {g['away_team']} | "
            f"ICOM {g.get('graph_force')} | "
            f"{g['market']} | {g['status']}"
        )
