import streamlit as st
from services.gemini_service import gerar_rubricas_ia

def render_rubricas_page():
    st.markdown('<p class="section-title">Contexto & Rubricas</p>', unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        diretrizes = st.text_area("Diretrizes do trabalho (opcional)", value=st.session_state["diretrizes"], height=180)
        uploaded_ctx = st.file_uploader("Arquivos de contexto (PDF ou TXT)", accept_multiple_files=True, type=["pdf", "txt"])

    with col_r:
        st.markdown("**Rubricas geradas pela IA**")
        if st.button("✨ Gerar Rubricas", type="primary", use_container_width=True):
            with st.spinner("Gerando critérios de avaliação…"):
                try:
                    rubricas = gerar_rubricas_ia(st.session_state["api_key"], diretrizes, uploaded_ctx)
                    st.session_state["rubricas"] = rubricas
                    st.session_state["diretrizes"] = diretrizes
                    st.session_state["arquivos_contexto"] = uploaded_ctx
                except Exception as e:
                    st.error(f"Erro ao gerar rubricas: {e}")

        if st.session_state["rubricas"]:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            rubricas = st.session_state["rubricas"]
            for i, r in enumerate(rubricas):
                with st.expander(f"**{r['criterio']}** — {r['peso']}%", expanded=False):
                    novo_nome = st.text_input("Nome", value=r["criterio"], key=f"nome_{i}")
                    nova_desc = st.text_input("Descrição", value=r.get("descricao", ""), key=f"desc_{i}")
                    novo_peso = st.slider("Peso (%)", 0, 100, r["peso"], 5, key=f"peso_{i}")
                    if st.button("🗑 Remover", key=f"del_{i}"):
                        st.session_state["rubricas"].pop(i)
                        st.rerun()
                    rubricas[i] = {"criterio": novo_nome, "peso": novo_peso, "descricao": nova_desc}

            st.session_state["rubricas"] = rubricas
            total_peso = sum(r["peso"] for r in rubricas)

            if total_peso != 100:
                st.warning(f"⚠️ Soma dos pesos: {total_peso}% (deve ser exatamente 100%)")
            else:
                st.success("✓ Soma dos pesos: 100%")
                if st.button("Prosseguir para Correção →", type="primary", use_container_width=True):
                    st.session_state["etapa"] = 2
                    st.rerun()
