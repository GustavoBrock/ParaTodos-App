# utils.py - Funções auxiliares e páginas de apoio

import streamlit as st

def speak(text):
    if st.session_state.get("voz_ativada", False):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voz_pt = None

            # Tenta encontrar uma voz em português
            for voz in voices:
                if "portuguese" in voz.name.lower() or "brazil" in voz.name.lower():
                    voz_pt = voz.id
                    break

            if voz_pt:
                engine.setProperty('voice', voz_pt)
            else:
                st.warning("Voz em português não encontrada. Usando voz padrão.")

            engine.setProperty('rate', 160)  # velocidade da fala
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            st.warning(f"Erro ao tentar falar: {e}")


def carregar_tema():
    st.markdown("""
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def mostrar_sobre():
    st.markdown("<h1>Sobre nós</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Nossa História</h3>", unsafe_allow_html=True)
    st.write("""
        Criamos este aplicativo porque vimos que muitas pessoas com deficiência têm dificuldade para se locomover. Os apps de transporte que existem não pensam em todo mundo. Por isso, decidimos fazer algo diferente: um app feito para ajudar todas as pessoas, com respeito e acessibilidade.

        A ideia surgiu ao perceber que a mobilidade ainda é um grande desafio para quem tem alguma limitação física, visual, auditiva ou intelectual. Muitas vezes, essas pessoas ficam dependentes de outras ou acabam evitando sair de casa por falta de transporte adequado. Isso não é justo.

        Queremos mudar essa realidade. Nosso objetivo é dar mais liberdade, conforto e segurança para quem precisa. Pensamos em cada detalhe com carinho: desde carros adaptados até motoristas treinados para oferecer um atendimento acolhedor.

        Esse app nasceu para ser mais do que um serviço. Ele nasceu como um projeto de inclusão, feito com escuta, empatia e compromisso com a diversidade.
    """)
    st.markdown("<h3>Nossa Missão</h3>", unsafe_allow_html=True)
    st.write("""
        Levar mais liberdade e segurança para pessoas com deficiência por meio de um transporte acessível e feito com carinho.
    """)
    st.markdown("<h3>Nossos Valores</h3>", unsafe_allow_html=True)
    st.markdown("""
        - Inclusão: Todos têm o direito de se locomover.  
        - Respeito: Tratamos todos com cuidado e atenção.  
        - Empatia: Nos colocamos no lugar do outro.  
        - Acessibilidade: Queremos que o app seja fácil para todos.  
        - Responsabilidade: Pensamos nas pessoas e no meio ambiente.  
    """)
    st.markdown("<h3>Nosso Diferencial</h3>", unsafe_allow_html=True)
    st.markdown("""
        - Carros adaptados  
        - Motoristas treinados  
        - App fácil de usar  
        - Atendimento com atenção e respeito
    """)
    st.markdown("<h4 style='margin-top:2em;'>Aqui, ninguém fica de fora. Pensamos em todos os detalhes para que você tenha um transporte justo e confortável.</h4>", unsafe_allow_html=True)

def mostrar_como_usar():
    st.markdown("<h1>Como usar</h1>", unsafe_allow_html=True)
    st.write("""
        🔹 **Deficiência Motora:** Escolha veículos com rampa ou elevador.

        🔹 **Deficiência Visual:** Motoristas treinados para conduzir com auxílio de cão-guia e comunicação assistiva.

        🔹 **Deficiência Auditiva:** Motoristas que utilizam Libras ou comunicação por texto.

        🔹 **Deficiência Intelectual:** Assistência personalizada durante toda a corrida.
    """)
