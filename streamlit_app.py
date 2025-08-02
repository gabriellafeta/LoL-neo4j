import pandas as pd
import streamlit as st


# Configuração do Streamlit
st.set_page_config(page_title="LoL Draft Graph", layout="wide")

##--------------------------------------------------------------------------------------------------------------------------------
# Data

file_path = "matchup_stats.csv" 

df = pd.read_csv(file_path)
##--------------------------------------------------------------------------------------------------------------------------------
# Funções

def apply_filters(df, league, playoffs, split, side, position, champion, matchup):
    filtered = df.copy()
    if league != "All":
        filtered = filtered[filtered["league"] == league]
    if playoffs != "All":
        filtered = filtered[filtered["playoffs"] == playoffs]
    if split != "All":
        filtered = filtered[filtered["split"] == split]
    if side != "All":
        filtered = filtered[filtered["side"] == side]
    if position != "All":
        filtered = filtered[filtered["position"] == position]
    if champion != "All":
        filtered = filtered[filtered["champion"] == champion]
    if matchup != "All":
        filtered = filtered[filtered["champion_matchup"] == matchup]
    return filtered



##--------------------------------------------------------------------------------------------------------------------------------
# Cols

colA = st.columns(1)
colB = st.columns(1)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
##--------------------------------------------------------------------------------------------------------------------------------
# Page Layout

with colA[0]:
    st.title("📊 Visualização da Tabela de Matchups")

with col1:
    league_filter = st.selectbox("League", options=["All"] + sorted(df['league'].dropna().unique().tolist()))
with col2:
    playoffs_filter = st.selectbox("Playoffs", options=["All"] + sorted(df['playoffs'].dropna().unique().tolist()))
with col3:
    split_filter = st.selectbox("Split", options=["All"] + sorted(df['split'].dropna().unique().tolist()))
with col4:
    side_filter = st.selectbox("Side", options=["All"] + sorted(df['side'].dropna().unique().tolist()))
with col5:
    position_filter = st.selectbox("Position", options=["All"] + sorted(df['position'].dropna().unique().tolist()))
with col6:
    champion_filter = st.selectbox("Champion", options=["All"] + sorted(df['champion'].dropna().unique().tolist()))
with col7:
    matchup_filter = st.selectbox("Matchup", options=["All"] + sorted(df['champion_matchup'].dropna().unique().tolist()))

##--------------------------------------------------------------------------------------------------------------------------------
# Filtros

filtered_df = apply_filters(
    df,
    league=league_filter,
    playoffs=playoffs_filter,
    split=split_filter,
    side=side_filter,
    position=position_filter,
    champion=champion_filter,
    matchup=matchup_filter
)

# Mostrar resultado
st.markdown(f"### Resultado com {len(filtered_df)} linhas")
st.dataframe(filtered_df)
