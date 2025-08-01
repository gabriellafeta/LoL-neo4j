import streamlit as st
import pandas as pd
from neo4j import GraphDatabase
import os

# Configuração do Streamlit
st.set_page_config(page_title="LoL Draft Graph", layout="wide")







##--------------------------------------------------------------------------------------------------------------------------------
st.title("📊 Visualização da Tabela de Matchups")

# Caminho do arquivo
file_path = "matchup_stats.xlsx"  # ou "data/matchup_stats.xlsx" se estiver em subpasta

# Tenta carregar e exibir
try:
    df_matchups = pd.read_excel(file_path)
    st.success("Arquivo carregado com sucesso!")
    st.dataframe(df_matchups)
except FileNotFoundError:
    st.error(f"Arquivo `{file_path}` não encontrado.")
except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")