import pandas as pd
import streamlit as st
import networkx as nx
import plotly.graph_objects as go

# Configuração do Streamlit
st.set_page_config(page_title="LoL Draft Graph", layout="wide")

##--------------------------------------------------------------------------------------------------------------------------------
# Funções
# Filtros
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

# Gerar arestas
def generate_edges(df):
    edges = []
    for _, row in df.iterrows():
        source = row["champion"]
        target = row["champion_matchup"]

        # Exemplo com WinRateTag
        relation = row["WinRateTag"]  # ou "EarlyGameType", ou ambas

        edges.append({
            "source": source,
            "target": target,
            "relation": relation,
            "weight": row["WinRate"]  # ou outra métrica contínua
        })
    return edges


# Relações
def add_champion_traits(df):
    # Early game
    df["EarlyGameType"] = df.apply(
        lambda row: "Bad Early Game" if sum([
            row["golddiffat15"] < 0,
            row["xpdiffat15"] < 0,
            row["csdiffat15"] < 0
        ]) >= 2 else "Good Early Game",
        axis=1
    )

    # Late game (por enquanto igual, pode ser ajustado depois com outros critérios)
    df["LateGameType"] = df.apply(
        lambda row: "Bad Late Game" if sum([
            row["golddiffat15"] < 0,
            row["xpdiffat15"] < 0,
            row["csdiffat15"] < 0
        ]) >= 2 else "Good Late Game",
        axis=1
    )

    # Win rate e tag
    df["WinRate"] = df["wins"] / df["games_played"] * 100
    df["WinRateTag"] = df["WinRate"].apply(lambda x: "Historically bad" if x < 50 else "Historically good")

    return df
##--------------------------------------------------------------------------------------------------------------------------------

file_path = "matchup_stats.csv"
df = pd.read_csv(file_path)
df = add_champion_traits(df)

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
##--------------------------------------------------------------------------------------------------------------------------------
G = nx.DiGraph()
for edge in generate_edges(filtered_df):
    G.add_edge(edge['source'], edge['target'], relation=edge['relation'])

# Layout dos nós
pos = nx.spring_layout(G, seed=42)

# Coleta posições e labels
edge_x = []
edge_y = []
for src, tgt in G.edges():
    x0, y0 = pos[src]
    x1, y1 = pos[tgt]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

node_x = [pos[node][0] for node in G.nodes()]
node_y = [pos[node][1] for node in G.nodes()]
node_text = list(G.nodes)

# Plotly figure
fig = go.Figure()

# Arestas
fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='gray'),
    hoverinfo='none',
    mode='lines'))

# Nós
fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_text,
    textposition="top center",
    marker=dict(size=10, color='lightblue'),
    hoverinfo='text'))

fig.update_layout(
    title="Grafo de Campeões",
    showlegend=False,
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)