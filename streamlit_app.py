import pandas as pd
import streamlit as st


# Configuração do Streamlit
st.set_page_config(page_title="LoL Draft Graph", layout="wide")

##--------------------------------------------------------------------------------------------------------------------------------
# Data
st.title("📊 Visualização da Tabela de Matchups")

file_path = "matchup_stats.xlsx" 

df = pd.read_excel(file_path)
##--------------------------------------------------------------------------------------------------------------------------------
# Funções

def apply_filters(df, league, playoffs, split, side, position):
    filtered = df.copy()
    if league != "Todos":
        filtered = filtered[filtered["league"] == league]
    if playoffs != "Todos":
        filtered = filtered[filtered["playoffs"] == playoffs]
    if split != "Todos":
        filtered = filtered[filtered["split"] == split]
    if side != "Todos":
        filtered = filtered[filtered["side"] == side]
    if position != "Todos":
        filtered = filtered[filtered["position"] == position]
    return filtered



##--------------------------------------------------------------------------------------------------------------------------------
# Cols

colA = st.columns(1)
colB = st.columns(1)

col1, col2, col3, col4, col5 = st.columns(5)
##--------------------------------------------------------------------------------------------------------------------------------
# Page Layout

with colA[0]:
    st.title("📊 Visualização da Tabela de Matchups")

with colB[0]:
    st.dataframe(df)

with col1:
    league_filter = st.selectbox("League", options=["Todos"] + sorted(df['league'].dropna().unique().tolist()))
with col2:
    playoffs_filter = st.selectbox("Playoffs", options=["Todos"] + sorted(df['playoffs'].dropna().unique().tolist()))
with col3:
    split_filter = st.selectbox("Split", options=["Todos"] + sorted(df['split'].dropna().unique().tolist()))
with col4:
    side_filter = st.selectbox("Side", options=["Todos"] + sorted(df['side'].dropna().unique().tolist()))
with col5:
    position_filter = st.selectbox("Position", options=["Todos"] + sorted(df['position'].dropna().unique().tolist()))

##--------------------------------------------------------------------------------------------------------------------------------
# Filtros

filtered_df = apply_filters(
    df,
    league=league_filter,
    playoffs=playoffs_filter,
    split=split_filter,
    side=side_filter,
    position=position_filter
)

# Mostrar resultado
st.markdown(f"### Resultado com {len(filtered_df)} linhas")
st.dataframe(filtered_df)

try:
    import openpyxl
    st.success("✅ openpyxl instalado com sucesso!")
except ImportError:
    st.error("❌ openpyxl não está instalado.")