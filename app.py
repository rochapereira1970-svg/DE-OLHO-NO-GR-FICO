import streamlit as st
import json

st.set_page_config(
    page_title="DE OLHO NOS MERCADOS",
    layout="wide"
)

st.title("⚽ DE OLHO NOS MERCADOS")

with open("jogos.json", "r", encoding="utf-8") as f:
    data = json.load(f)

games = data["analyzed_games"]

free_games = [g for g in games if not g["is_vip"]]
vip_games = [g for g in games if g["is_vip"]]

st.header("🟢 FREE")

for jogo in free_games:
    st.write(
        f"**{jogo['home_team']} x {jogo['away_team']}** | "
        f"{jogo['market']} | "
        f"ICOM {jogo['graph_force']}"
    )

st.divider()

st.header("🔥 VIP")

for jogo in vip_games:
    st.write(
        f"**{jogo['home_team']} x {jogo['away_team']}** | "
        f"{jogo['market']} | "
        f"ICOM {jogo['graph_force']}"
    )
    
