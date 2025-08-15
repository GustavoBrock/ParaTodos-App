# db.py - Banco de dados com Google Sheets

import streamlit as st
import pandas as pd
from gspread_pandas import Spread
import io
from datetime import datetime

# O ID da sua planilha, lido do secrets.toml
SHEET_ID = st.secrets.get("google_sheet.sheet_id", None)

# Variável de cache para evitar múltiplas conexões à planilha
@st.cache_resource(ttl=300) # O cache será atualizado a cada 5 minutos
def get_spreadsheets():
    """Conecta e retorna o objeto Spread para a planilha principal."""
    if not SHEET_ID:
        st.error("O ID da planilha não foi encontrado. Certifique-se de que ele está no seu arquivo secrets.toml.")
        return None
    try:
        # A planilha principal (usada para usuários e histórico)
        spread = Spread(SHEET_ID)
        return spread
    except Exception as e:
        st.error(f"Erro ao conectar com a planilha do Google Sheets. Verifique o ID e as permissões. Erro: {e}")
        return None

def get_users_df():
    """Lê a aba 'users' da planilha e retorna como DataFrame."""
    spread = get_spreadsheets()
    if spread:
        return spread.sheet_to_df(index=False, sheet='users')
    return pd.DataFrame(columns=['username', 'password', 'profile'])

def update_users_sheet(df):
    """Escreve o DataFrame de volta na aba 'users'."""
    spread = get_spreadsheets()
    if spread:
        spread.df_to_sheet(df, index=False, start='A1', replace=True, sheet='users')

def get_history_df():
    """Lê a aba 'historico' da planilha e retorna como DataFrame."""
    spread = get_spreadsheets()
    if spread:
        return spread.sheet_to_df(index=False, sheet='historico')
    return pd.DataFrame(columns=['usuario', 'motorista', 'necessidades', 'status', 'data'])

def update_history_sheet(df):
    """Escreve o DataFrame de volta na aba 'historico'."""
    spread = get_spreadsheets()
    if spread:
        spread.df_to_sheet(df, index=False, start='A1', replace=True, sheet='historico')


def add_user(username, password, profile):
    """Adiciona um novo usuário na aba 'users' da planilha."""
    import bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    df = get_users_df()
    if username in df['username'].values:
        st.error("Este nome de usuário já existe.")
        return False
    
    new_user = pd.DataFrame([{
        'username': username,
        'password': hashed,
        'profile': profile
    }])
    updated_df = pd.concat([df, new_user], ignore_index=True)
    update_users_sheet(updated_df)
    return True

def get_user(username):
    """Retorna os dados de um usuário da aba 'users'."""
    df = get_users_df()
    user_row = df[df['username'] == username]
    if not user_row.empty:
        return user_row.iloc[0]
    return None

def user_exists(username):
    """Verifica se um usuário já existe na aba 'users'."""
    df = get_users_df()
    return username in df['username'].values

def salvar_corrida(usuario, motorista, necessidades, status):
    """Salva uma corrida na aba 'historico'."""
    df = get_history_df()
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    new_corrida = pd.DataFrame([{
        'usuario': usuario,
        'motorista': motorista,
        'necessidades': ', '.join(necessidades),
        'status': status,
        'data': data
    }])
    updated_df = pd.concat([df, new_corrida], ignore_index=True)
    update_history_sheet(updated_df)

def carregar_historico(usuario):
    """Carrega o histórico do usuário da aba 'historico'."""
    df = get_history_df()
    historico_usuario = df[df['usuario'] == usuario].sort_values(by='data', ascending=False)
    # Retorna o DataFrame para ser usado nas funções de exibição
    return historico_usuario

def mostrar_historico():
    st.subheader("Histórico de Corridas")
    historico = carregar_historico(st.session_state.username)
    if not historico.empty:
        st.dataframe(historico, use_container_width=True)
    else:
        st.info("Nenhuma corrida registrada ainda.")

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
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        tabela_precos.to_excel(writer, index=False)
    st.download_button("Baixar Excel", output.getvalue(), file_name="precos.xlsx")