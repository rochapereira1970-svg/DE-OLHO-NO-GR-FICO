import streamlit as st
import json
import os

st.set_page_config(page_title="DE OLHO NO GRÁFICO", layout="wide")

st.title("📊 DE OLHO NO GRÁFICO")

# DIAGNÓSTICO

st.write("Pasta atual:", os.getcwd())
st.write("Arquivos encontrados:", os.listdir())

try:
with open("jogos.json", "r", encoding="utf-8") as f:
data = json.load(f)

```
games = data.get("analyzed_games", [])

st.success(f"JSON carregado com sucesso! Jogos encontrados: {len(games)}")

for jogo in games:
    st.write(
        f"{jogo['home_team']} x {jogo['away_team']} | "
        f"{jogo['market']} | "
        f"{jogo['graph_force']}"
    )
```

except Exception as e:
st.error(f"Erro ao carregar jogos.json: {e}")
