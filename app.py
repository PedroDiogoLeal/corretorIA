import streamlit as st
from utils import injetar_css_global, stepper

# Importação dos módulos das páginas
from pages.gate import render_gate_page
from pages.rubricas import render_rubricas_page
from pages.correcao import render_correcao_page
from pages.resultados import render_resultados_page

# Configuração da página
st.set_page_config(page_title="Corretor IA", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")

# Inicialização do CSS global
injetar_css_global()

# Inicialização do Session State
defaults = {
    "api_key": "", "api_validada": False, "etapa": 0,
    "diretrizes": "", "arquivos_contexto": None, "rubricas": [],
    "historico": [], "insights": ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Header Persistente
if st.session_state["etapa"] > 0:
    col_logo, col_user = st.columns([6, 1])
    with col_logo:
        st.markdown("### 📋 Corretor IA")
    with col_user:
        if st.button("Trocar chave", help="Voltar à tela de configuração"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
    stepper(st.session_state["etapa"] - 1)

# Roteador de Etapas (A Orquestração do App)
if st.session_state["etapa"] == 0:
    render_gate_page()
elif st.session_state["etapa"] == 1:
    render_rubricas_page()
elif st.session_state["etapa"] == 2:
    render_correcao_page()
elif st.session_state["etapa"] == 3:
    render_resultados_page()

st.markdown("<p style='font-size:11px;color:#d1d5db;text-align:center;margin-top:2rem;'>MVP Corretor IA · Gemini 2.5 Flash</p>", unsafe_allow_html=True)
