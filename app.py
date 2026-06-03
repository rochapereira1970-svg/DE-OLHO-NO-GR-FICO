import streamlit as st
import json

st.title("DE OLHO NOS MERCADOS")

if st.button("🔄 Atualizar dados"):
    st.warning("Agora o robô externo será responsável pelos dados.")

# Carrega jogos já prontos
try:
    with open("jogos.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    st.subheader("Jogos do dia")

    for jogo in data["analyzed_games"]:
        st.write(jogo)

except:
    st.error("Nenhum dado encontrado. Rode o bot primeiro.")
