# auth.py - Gerencia login, cadastro e sessão de usuário

import streamlit as st
import bcrypt
from db import get_user, add_user, user_exists
import os

logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

def load_session():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.profile = ""

def login_page():
    # Logo grande no topo da sidebar
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image(logo_path, width=200)
        

    # Conteúdo central
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>ParaTodos - Match PCD</h2>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Login</h4>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Usuário:")
            password = st.text_input("Senha:", type="password")
            submit = st.form_submit_button("Entrar")
            if submit:
                if not username or not password:
                    st.warning("Por favor, preencha todos os campos.")
                else:
                    user = get_user(username)
                    if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.profile = user[2]
                        st.rerun()
                    else:
                        st.error("Usuário ou senha inválidos.")

def register_page():
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image(logo_path, width=160)
        st.markdown("<h3 style='text-align: center; margin-top: 10px;'>ParaTodos</h3>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>Cadastro</h2>", unsafe_allow_html=True)
        with st.form("register_form"):
            username = st.text_input("Novo usuário:")
            password = st.text_input("Nova senha:", type="password")
            profile = st.selectbox("Perfil:", [
                "Deficiência Motora", 
                "Deficiência Visual", 
                "Deficiência Auditiva", 
                "Deficiência Intelectual",
                "Transtorno do Espectro Autista (TAE)"
                ])
            
            submit = st.form_submit_button("Cadastrar")
            if submit:
                if not username or not password:
                    st.warning("Preencha todos os campos para cadastrar.")
                elif user_exists(username):
                    st.error("Usuário já existe!")
                else:
                    add_user(username, password, profile)
                    st.success("Cadastro realizado. Faça login.")
