# mapa.py - Página de rota simulada com folium

import streamlit as st
import folium
from streamlit_folium import st_folium

def pagina_mapa():
    if 'selected_driver' not in st.session_state:
        st.warning("Nenhum motorista foi selecionado ainda. Vá até a aba 'Home' para fazer uma busca.")
        return

    st.markdown("### 🗺️ Rota simulada entre motorista e passageiro")
    ponto_partida = [-26.9155, -49.0713]     # ponto do usuário
    ponto_motorista = [-26.9108, -49.0703]   # ponto do motorista

    mapa = folium.Map(location=[-26.913, -49.0708], zoom_start=14, tiles="OpenStreetMap")
    folium.Marker(ponto_motorista, tooltip="Motorista", icon=folium.Icon(color="blue")).add_to(mapa)
    folium.Marker(ponto_partida, tooltip="Você", icon=folium.Icon(color="green")).add_to(mapa)
    folium.PolyLine(locations=[ponto_motorista, ponto_partida], color="blue", weight=3).add_to(mapa)

    st_folium(mapa, width=700, height=500, returned_objects=[])
