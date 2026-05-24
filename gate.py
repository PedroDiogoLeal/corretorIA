import streamlit as st
from services.gemini_service import validar_chave

def render_gate_page():
    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1rem;">
        <div style="font-size:2.5rem;">📋</div>
        <h1 style="font-size:1.6rem;font-weight:700;margin:.5rem 0 .25rem;">Corretor IA</h1>
        <p style="color:#6b7280;font-size:14px;">Correção de trabalhos acadêmicos com IA</p>
    </div>
    """, unsafe_allow_html=True)

    col_c, col_r = st.columns([1, 1])
    with col_c:
        st.markdown("#### Configure sua API Key para começar")
        api_input = st.text_input("Gemini API Key", type="password", placeholder="Cole sua chave aqui…")
        if st.button("Continuar →", type="primary", use_container_width=True):
            if not api_input.strip():
                st.error("Insira uma API Key válida.")
            else:
                with st.spinner("Validando chave..."):
                    try:
                        validar_chave(api_input.strip())
                        st.session_state["api_key"] = api_input.strip()
                        st.session_state["api_validada"] = True
                        st.session_state["etapa"] = 1
                        st.rerun()
                    except Exception as e:
                        st.error(f"Chave inválida ou erro de conexão: {e}")
    with col_r:
        st.markdown("#### Como funciona")
        st.markdown("<div style='font-size:13px;color:#374151;line-height:2;'><b>1. Contexto & Rubricas</b><br>Cole as diretrizes e a IA sugere os critérios.<br><br><b>2. Correção em lote</b><br>Envie os trabalhos. A IA corrige e adiciona comentários inline.<br><br><b>3. Painel de resultados</b><br>Gere estatísticas e veja os grifos no texto.</div>", unsafe_allow_html=True)
