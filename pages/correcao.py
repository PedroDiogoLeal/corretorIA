import streamlit as st
import time
from utils import extrair_texto
from services.gemini_service import corrigir_trabalho_ia

def render_correcao_page():
    st.markdown('<p class="section-title">Correção em lote</p>', unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        uploaded_works = st.file_uploader(
            "Trabalhos dos alunos (PDF ou TXT)", 
            accept_multiple_files=True, 
            type=["pdf", "txt"],
            key="trabalhos_uploader"
        )
        nomes_alunos = {}
        if uploaded_works:
            st.markdown("**Nome de cada aluno**")
            for f in uploaded_works:
                nome_default = f.name.replace(".pdf","").replace(".txt","").replace("_"," ").title()
                nomes_alunos[f.name] = st.text_input(f.name, value=nome_default, key=f"aluno_{f.name}")

    with col_r:
        if uploaded_works:
            st.info(f"📋 {len(uploaded_works)} arquivo(s) carregado(s) e pronto(s) para processamento.")
            
            if st.button("▶ Iniciar Correção em Lote", type="primary", use_container_width=True):
                novos = []
                
                # Elementos visuais de carregamento dinâmico
                status_placeholder = st.empty()
                progresso_barra = st.progress(0.0)
                
                total_arquivos = len(uploaded_works)

                for idx, arquivo in enumerate(uploaded_works):
                    nome = nomes_alunos.get(arquivo.name, arquivo.name)
                    
                    # Mensagem dinâmica de espera (Problema 2 resolvido aqui)
                    status_placeholder.markdown(
                        f"""
                        <div style='padding: 10px; background-color: #eff6ff; border-left: 4px solid #1d4ed8; border-radius: 4px; margin-bottom: 10px;'>
                            ⏳ <b>Processando ({idx+1}/{total_arquivos}):</b> Analisando o relatório de <i>{nome}</i> via IA...
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Atualiza a barra de progresso proporcionalmente
                    progresso_barra.progress(idx / total_arquivos)
                    
                    # Extração e chamada de IA
                    texto = extrair_texto(arquivo)
                    try:
                        resultado = corrigir_trabalho_ia(
                            st.session_state["api_key"], arquivo,
                            st.session_state["rubricas"], st.session_state["diretrizes"],
                            st.session_state["arquivos_contexto"]
                        )
                        resultado.update({"nome": nome, "arquivo": arquivo.name, "texto": texto})
                        novos.append(resultado)
                    except Exception as e:
                        st.error(f"Erro ao corrigir o trabalho de {nome}: {e}")

                # Conclusão do progresso visual
                progresso_barra.progress(1.0)
                status_placeholder.success("🎉 Todas as correções foram processadas com sucesso!")
                time.sleep(1) # Pequena pausa para o usuário ver o sucesso antes da transição

                # Sincronização estrita de estados (Problema 1 resolvido aqui)
                st.session_state["historico"].extend(novos)
                st.session_state["etapa"] = 3
                
                # Força o recarregamento imediato já na etapa correta
                st.rerun()
        else:
            st.write("Aguardando o upload de relatórios na coluna da esquerda para habilitar o motor de IA.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Voltar para Rubricas"):
            st.session_state["etapa"] = 1
            st.rerun()
