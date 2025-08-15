# Estrutura inicial para versão reorganizada do app ParaTodos

# Diretórios sugeridos:
# paratodos-app/
# ├── app.py                  <- fluxo principal
# ├── auth.py                 <- login, cadastro, sessão
# ├── db.py                   <- banco de dados SQLite
# ├── motoristas.py           <- base de motoristas e matching
# ├── mapa.py                 <- simulação de rota com folium
# ├── utils.py                <- voz, extras, temas
# ├── logo.png
# ├── requirements.txt
# ├── README.md

# Este é o novo app.py simplificado que chama os módulos

import streamlit as st
from auth import login_page, register_page, load_session
from db import init_db
from motoristas import pagina_home
from mapa import pagina_mapa
from utils import carregar_tema
import pandas as pd

st.set_page_config(page_title="ParaTodos - Match PCD", layout="wide")
carregar_tema()
init_db()
load_session()

menu_login = st.sidebar.selectbox("Acesso", ["Login", "Cadastro"])

if not st.session_state.logged_in:
    if menu_login == "Login":
        login_page()
    else:
        register_page()
else:
    menu = st.sidebar.selectbox("Menu", ["Home", "Histórico", "Preços", "Sobre", "Como usar"])

    if menu == "Home":
        pagina_home()
    elif menu == "Histórico":
        from db import mostrar_historico
        mostrar_historico()
    elif menu == "Preços":
        from db import mostrar_precos
        mostrar_precos()
    elif menu == "Sobre":
        from utils import mostrar_sobre
        mostrar_sobre()
    elif menu == "Como usar":
        from utils import mostrar_como_usar
        mostrar_como_usar()
