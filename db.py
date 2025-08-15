# db.py - Banco de dados e funções auxiliares (SQLite)

import sqlite3
import pandas as pd
import io
import streamlit as st
from datetime import datetime
import bcrypt

DATABASE_PATH = "usuarios.db"

def get_db_connection():
    """Retorna uma nova conexão com o banco de dados.
    Usar a instrução 'with' garante que a conexão é fechada automaticamente.
    """
    return sqlite3.connect(DATABASE_PATH, check_same_thread=False)

def init_db():
    """Cria as tabelas de usuários e histórico se elas não existirem."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password BLOB NOT NULL,
            profile TEXT NOT NULL)""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            motorista TEXT NOT NULL,
            necessidades TEXT NOT NULL,
            status TEXT NOT NULL,
            data TEXT NOT NULL)""")
        conn.commit()

def add_user(username, password, profile):
    """Adiciona um novo usuário ao banco de dados."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, profile) VALUES (?, ?, ?)', (username, hashed, profile))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            st.error("Este nome de usuário já existe.")
            return False

def get_user(username):
    """Busca os dados de um usuário pelo nome de usuário."""
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, profile FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None

def user_exists(username):
    """Verifica se um nome de usuário já existe."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
        return cursor.fetchone() is not None

def salvar_corrida(usuario, motorista, necessidades, status):
    """Salva uma corrida no histórico."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        cursor.execute("INSERT INTO historico (usuario, motorista, necessidades, status, data) VALUES (?, ?, ?, ?, ?)",
                       (usuario, motorista, ', '.join(necessidades), status, data))
        conn.commit()

def carregar_historico(usuario):
    """Carrega o histórico de corridas de um usuário."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT motorista, necessidades, status, data FROM historico WHERE usuario = ? ORDER BY id DESC", (usuario,))
        return cursor.fetchall()

def mostrar_historico():
    st.subheader("Histórico de Corridas")
    if 'username' in st.session_state:
        historico = carregar_historico(st.session_state.username)
        if historico:
            df = pd.DataFrame(historico, columns=["Motorista", "Necessidades", "Status", "Data"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma corrida registrada ainda.")
    else:
        st.warning("Faça login para ver seu histórico.")

def mostrar_precos():
    st.subheader("Tabela de Preços")
    tabela_precos = pd.DataFrame({
        "Tipo de Veículo": [
            "Carro Padrão", "Carro Compacto Econômico", "Veículo Adaptado com Rampa",
            "Veículo com Elevador", "Carro com Motorista Treinado (Sensorial)",
            "Carro com Acompanhante", "Veículo Compartilhado (Sustentável)",
            "Van Acessível (Grupo ou Família)", "Carro Elétrico Sustentável"
        ],
        "Indicado para": [
            "Pessoas sem deficiência", "Qualquer pessoa", "Cadeirantes",
            "Pessoas com mobilidade muito reduzida", "Pessoas com deficiência visual ou auditiva",
            "Pessoas com deficiência intelectual ou idosas", "Todos os públicos",
            "Grupos com PCDs e acompanhantes", "Todos os públicos"
        ],
        "Adaptações Especiais": [
            "Nenhuma", "Nenhuma", "Rampa, espaço interno ampliado",
            "Elevador hidráulico, cintos especiais", "Comunicação adaptada (gestual, áudio)",
            "Espaço para cuidador/a", "Pode ter adaptação",
            "Rampa, elevador, até 4 cadeirantes", "Nenhuma (ou leve adaptação)"
        ],
        "Benefícios Principais": [
            "Rápido, econômico", "Menor preço, ideal para trajetos curtos",
            "Acesso com cadeira de rodas, segurança", "Conforto e autonomia no embarque",
            "Mais atenção e cuidado", "Maior segurança emocional",
            "Mais barato, menos poluição", "Ideal para clínicas, eventos, passeios",
            "Redução de impacto ambiental, silencioso"
        ],
        "Preço Estimado": [
            "A partir de R$ 8,00", "A partir de R$ 6,00", "A partir de R$ 12,00",
            "A partir de R$ 15,00", "A partir de R$ 10,00", "A partir de R$ 13,00",
            "A partir de R$ 6,00", "A partir de R$ 18,00", "A partir de R$ 9,00"
        ]
    })
    st.dataframe(tabela_precos, use_container_width=True)

    output = io.BytesIO()
    # Verifique se 'xlsxwriter' está no seu requirements.txt
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        tabela_precos.to_excel(writer, index=False)
    st.download_button("Baixar Excel", output.getvalue(), file_name="precos.xlsx")