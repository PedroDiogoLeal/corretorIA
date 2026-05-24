import streamlit as st
import pandas as pd
from utils import cor_nota, cor_dot, badge_cor, aplicar_grifos
from services.gemini_service import gerar_insights_ia

def render_resultados_page():
    historico = st.session_state["historico"]
    rubricas  = st.session_state["rubricas"]
    st.markdown('<p class="section-title">Resultados da turma</p>', unsafe_allow_html=True)

    if historico:
        notas_globais = [h["nota_global"] for h in historico if h.get("nota_global") is not None]
        media_geral = round(sum(notas_globais)/len(notas_globais), 1) if notas_globais else None
        
        cols = st.columns(5)
        with cols[0]:
            st.markdown(f'<div class="metric-card"><div class="val {cor_nota(media_geral)}">{media_geral or "—"}</div><div class="lbl">Média geral</div></div>', unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown("**Lista de alunos**")
        for h in historico:
            nota = h.get("nota_global")
            st.markdown(f'<div class="aluno-row"><div><div class="aluno-name">{h["nome"]}</div><div class="aluno-file">{h["arquivo"]}</div></div><div class="nota-badge" style="{badge_cor(nota)}">{nota}</div></div>', unsafe_allow_html=True)

    with col_r:
        st.markdown("**Detalhe por aluno**")
        if historico:
            aluno_idx = st.selectbox("Selecione o aluno", options=range(len(historico)), format_func=lambda i: historico[i]["nome"])
            h = historico[aluno_idx]
            
            for c in h.get("criterios", []):
                st.markdown(f'<div class="criterio-item"><div class="dot {cor_dot(c.get("nota"))}"></div><div><span style="font-weight:500;">{c["criterio"]}</span> — {c.get("nota")}<br><span style="color:#6b7280;font-size:12px;">{c.get("justificativa","")}</span></div></div>', unsafe_allow_html=True)

    # Bloco Inline Text
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("**Correção inline do trabalho**")
    aluno_inline_idx = st.selectbox("Trabalho a visualizar", options=range(len(historico)), format_func=lambda i: historico[i]["nome"], key="sel_inline")
    h_inline = historico[aluno_inline_idx]
    
    html_anotado = aplicar_grifos(h_inline.get("texto", ""), h_inline.get("anotacoes", []))
    st.markdown(f'<div class="texto-anotado">{html_anotado}</div>', unsafe_allow_html=True)

    # Bloco Insights
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    if st.button("✨ Gerar síntese com IA", type="primary"):
        st.session_state["insights"] = gerar_insights_ia(st.session_state["api_key"], historico, rubricas, st.session_state["diretrizes"], st.session_state["arquivos_contexto"])
    
    if st.session_state["insights"]:
        st.markdown(f'<div class="insight-box">💡 {st.session_state["insights"]}</div>', unsafe_allow_html=True)
