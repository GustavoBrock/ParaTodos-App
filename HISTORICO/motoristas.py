# motoristas.py - Separação de tipo de veículo e adaptação (sem sugestões automáticas)

import streamlit as st
from db import salvar_corrida
from utils import speak
import folium
from streamlit_folium import st_folium
import time
import os
import math

motoristas = [
    {"name": "João", "capabilities": ["rampa", "cadeira de rodas"], "veiculo": "Comum"},
    {"name": "Maria", "capabilities": ["interprete libras"], "veiculo": "Híbrido"},
    {"name": "Carlos", "capabilities": ["rampa", "interprete libras", "cadeira de rodas"], "veiculo": "Comum"},
    {"name": "Ana", "capabilities": ["comunicação assistida"], "veiculo": "Elétrico"},
    {"name": "Pedro", "capabilities": ["rampa"], "veiculo": "Comum"},
    {"name": "Fernanda", "capabilities": ["interprete libras", "comunicação assistida"], "veiculo": "Híbrido"},
    {"name": "Lucas", "capabilities": ["rampa", "comunicação assistida"], "veiculo": "Elétrico"},
    {"name": "Patrícia", "capabilities": ["rampa", "cadeira de rodas", "elevador"], "veiculo": "Comum"},
    {"name": "Rafael", "capabilities": ["interprete libras"], "veiculo": "Híbrido"},
    {"name": "Juliana", "capabilities": ["rampa", "cadeira de rodas"], "veiculo": "Comum"},
    {"name": "Gustavo", "capabilities": ["rampa", "cadeira de rodas", "elevador"], "veiculo": "Elétrico"},
    {"name": "Luciana", "capabilities": ["comunicação assistida"], "veiculo": "Híbrido"},
    {"name": "Eduardo", "capabilities": ["interprete libras"], "veiculo": "Comum"},
    {"name": "Beatriz", "capabilities": ["rampa", "cadeira de rodas"], "veiculo": "Comum"},
    {"name": "Fábio", "capabilities": ["rampa", "comunicação assistida"], "veiculo": "Elétrico"},
    {"name": "Camila", "capabilities": ["interprete libras", "cadeira de rodas"], "veiculo": "Híbrido"},
    {"name": "Marcos", "capabilities": ["rampa"], "veiculo": "Comum"},
    {"name": "Vanessa", "capabilities": ["comunicação assistida"], "veiculo": "Elétrico"},
    {"name": "André", "capabilities": ["rampa", "interprete libras"], "veiculo": "Comum"},
    {"name": "Larissa", "capabilities": ["rampa", "elevador"], "veiculo": "Híbrido"},
]

precos_veiculo = {
    "Comum":     (4.00, 1.40, 0.25),
    "Híbrido":   (4.50, 1.30, 0.23),
    "Elétrico":  (5.00, 1.20, 0.20)
}

taxas_adaptacao = {
    "rampa": 2.00,
    "elevador": 3.50,
    "comunicação assistida": 1.50,
    "acompanhante": 2.50,
    "interprete libras": 1.00,
    "cadeira de rodas": 0.00
}

logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def estimar_duracao(dist_km):
    return round(dist_km / 0.5)

def mostrar_mapa_simulado():
    ponto_partida = [-26.9155, -49.0713]
    ponto_motorista = [-26.9108, -49.0703]
    mapa = folium.Map(location=[-26.913, -49.0708], zoom_start=14)
    folium.Marker(ponto_motorista, tooltip="Motorista", icon=folium.Icon(color="blue")).add_to(mapa)
    folium.Marker(ponto_partida, tooltip="Você", icon=folium.Icon(color="green")).add_to(mapa)
    folium.PolyLine([ponto_motorista, ponto_partida], color="blue").add_to(mapa)
    st_folium(mapa, width=700, height=500)

def pagina_home():
    if 'aba_visitada' not in st.session_state or not st.session_state.aba_visitada:
        st.session_state.search_clicked = False
        st.session_state.matched_drivers = []
        st.session_state.selected_driver = ""
        st.session_state.aba_visitada = True

    col1, col2 = st.columns([1, 8])
    with col1:
        st.image(logo_path, width=200)
    with col2:
        st.markdown("<h1 style='color:#005DA8; margin-bottom:0;'>ParaTodos - Match PCD</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#fff; margin-top:0;'>Sistema de Match PCD x Motoristas</h4>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"<h3>Bem-vindo, {st.session_state.username}!</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Perfil:</strong> {st.session_state.profile}</p>", unsafe_allow_html=True)
        st.session_state.voz_ativada = st.checkbox("🔊 Ativar voz", value=st.session_state.get("voz_ativada", False))
        if st.session_state.voz_ativada:
            if st.button("🔈 Testar voz"):
                speak("O sistema de voz está funcionando corretamente.")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.aba_visitada = False
            st.rerun()

    st.info("Selecione todas as opções que correspondem às suas necessidades.")
    needs = st.multiselect("Selecione o que você precisa:", ["rampa", "cadeira de rodas", "interprete libras", "comunicação assistida", "elevador"])
    local_origem = st.text_input("Local atual (ex: Rua A, 123)")
    local_destino = st.text_input("Local de parada (ex: Av. B, 456)")

    if st.button("Buscar motoristas compatíveis"):
        st.session_state.matched_drivers = []
        st.session_state.selected_driver = ""
        st.session_state.search_clicked = True

        if not needs:
            st.warning("Por favor, selecione ao menos uma necessidade.")
            speak("Por favor, selecione ao menos uma necessidade.")
        elif not local_origem or not local_destino:
            st.warning("Preencha origem e destino para estimar a corrida.")
        else:
            st.session_state.matched_drivers = [
                d for d in motoristas if all(n in d["capabilities"] for n in needs)]

    if st.session_state.get("search_clicked") and st.session_state.get("matched_drivers"):
        st.success(f"{len(st.session_state.matched_drivers)} motorista(s) encontrado(s).")
        speak(f"{len(st.session_state.matched_drivers)} motoristas encontrados.")
        driver_names = [f"{d['name']} | Recursos: {', '.join(d['capabilities'])}" for d in st.session_state.matched_drivers]
        selected_driver = st.selectbox("Escolha um motorista disponível:", driver_names)

        distancia_km = 5.2
        duracao_min = estimar_duracao(distancia_km)

        driver_nome = selected_driver.split("|")[0].strip()
        driver_obj = next((d for d in motoristas if d["name"] == driver_nome), None)

        if driver_obj:
            veiculo = driver_obj["veiculo"]
            base, por_km, por_min = precos_veiculo.get(veiculo, (4.0, 1.4, 0.25))
            taxa_adapt = sum(taxas_adaptacao.get(n, 0) for n in needs)
            preco_estimado = round(base + distancia_km * por_km + duracao_min * por_min + taxa_adapt, 2)

            st.markdown(f"**Distância estimada:** {distancia_km} km")
            st.markdown(f"**Duração estimada:** {duracao_min} minutos")
            st.markdown(f"**Tipo de veículo:** {veiculo}")
            st.markdown(f"**Adaptações selecionadas:** {', '.join(needs)}")
            st.markdown(f"**Taxa de adaptação:** R$ {taxa_adapt:.2f}")
            st.markdown(f"**Preço estimado:** R$ {preco_estimado:.2f}")

            if st.button("🚗 Chamar motorista"):
                st.session_state.mostrar_mapa = True
                st.info("Motorista a caminho...")
                progress = st.progress(0)
                for i in range(1, 101):
                    time.sleep(0.01)
                    progress.progress(i)
                st.success("Motorista chegou! 🧍‍♂️🚗")
                speak("Motorista chegou.")
                salvar_corrida(st.session_state.username, selected_driver.split("|")[0].strip(), needs, "Finalizada")

            # Exibir mapa se o motorista já chegou
            if st.session_state.get("mostrar_mapa"):
                mostrar_mapa_simulado()


    elif st.session_state.get("search_clicked") and not st.session_state.get("matched_drivers"):
        st.error("Nenhum motorista compatível encontrado.")
        speak("Nenhum motorista compatível encontrado.")
