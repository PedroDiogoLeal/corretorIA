import streamlit as st
import re
import html as html_lib

def injetar_css_global():
    st.markdown("""
    <style>
    /* ── Stepper ── */
    .stepper { display: flex; align-items: center; gap: 0; margin-bottom: 2rem; background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 10px; padding: 4px; }
    .step-item { flex: 1; text-align: center; padding: 8px 4px; border-radius: 7px; font-size: 13px; font-weight: 500; color: #9ca3af; cursor: default; transition: background 0.2s; }
    .step-item.done   { color: #16a34a; background: #f0fdf4; }
    .step-item.active { color: #1d4ed8; background: #eff6ff; }
    .step-item .step-num { display: inline-block; width: 20px; height: 20px; border-radius: 50%; font-size: 11px; line-height: 20px; text-align: center; margin-right: 5px; background: currentColor; color: white; }
    .step-item.done .step-num    { background: #16a34a; }
    .step-item.active .step-num  { background: #1d4ed8; }
    .step-item.pending .step-num { background: #d1d5db; color: #6b7280; }

    /* ── Metric cards ── */
    .metric-card { flex: 1; background: #f8f9fa; border-radius: 10px; padding: 12px 16px; text-align: center; }
    .metric-card .val { font-size: 24px; font-weight: 600; }
    .metric-card .lbl { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: .05em; }
    .val-green  { color: #16a34a; }
    .val-yellow { color: #d97706; }
    .val-red    { color: #dc2626; }
    .val-blue   { color: #1d4ed8; }

    /* ── Resultado por critério ── */
    .criterio-item { display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f3f4f6; font-size: 13px; }
    .criterio-item:last-child { border-bottom: none; }
    .dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; margin-top: 3px; }
    .dot-green  { background: #16a34a; }
    .dot-yellow { background: #d97706; }
    .dot-red    { background: #dc2626; }

    /* ── Barra de peso ── */
    .peso-wrap { display: inline-flex; align-items: center; gap: 8px; }
    .peso-bar-bg { width: 80px; height: 6px; background: #e5e7eb; border-radius: 3px; overflow: hidden; display: inline-block; }
    .peso-bar-fill { height: 100%; background: #3b82f6; border-radius: 3px; }

    /* ── Progress list ── */
    .file-progress-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #6b7280; padding: 4px 0; }
    .file-progress-item.done    { color: #16a34a; }
    .file-progress-item.current { color: #1d4ed8; font-weight: 500; }

    /* ── Insight box ── */
    .insight-box { background: #eff6ff; border-left: 3px solid #3b82f6; border-radius: 0 8px 8px 0; padding: 12px 16px; font-size: 13px; color: #1e40af; line-height: 1.6; margin-top: 1rem; }

    /* ── Aluno row ── */
    .aluno-row { display: grid; grid-template-columns: 1fr 90px; gap: 8px; align-items: center; padding: 10px 0; border-bottom: 1px solid #f3f4f6; font-size: 13px; }
    .aluno-row:last-child { border-bottom: none; }
    .aluno-name { font-weight: 500; color: #111827; }
    .aluno-file { font-size: 11px; color: #9ca3af; }

    /* ── Nota badge ── */
    .nota-badge { text-align: center; font-weight: 600; font-size: 16px; padding: 4px 10px; border-radius: 8px; }

    /* ── Correção inline: texto anotado ── */
    .texto-anotado { font-size: 14px; line-height: 1.85; color: #1f2937; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.5rem 1.75rem; white-space: pre-wrap; word-break: break-word; font-family: Georgia, serif; max-height: 520px; overflow-y: auto; }
    .grifo { background: #fef08a; border-bottom: 2px solid #ca8a04; border-radius: 2px; cursor: help; position: relative; padding: 1px 2px; }
    .grifo .tooltip { visibility: hidden; opacity: 0; width: 280px; background: #1e293b; color: #f1f5f9; font-size: 12px; font-family: sans-serif; line-height: 1.5; padding: 8px 12px; border-radius: 8px; position: absolute; z-index: 999; bottom: calc(100% + 6px); left: 50%; transform: translateX(-50%); transition: opacity 0.15s; pointer-events: none; white-space: normal; box-shadow: 0 4px 16px rgba(0,0,0,0.25); }
    .grifo .tooltip::after { content: ""; position: absolute; top: 100%; left: 50%; transform: translateX(-50%); border: 6px solid transparent; border-top-color: #1e293b; }
    .grifo:hover .tooltip { visibility: visible; opacity: 1; }
    .legenda-inline { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #6b7280; margin-bottom: 8px; }
    .legenda-grifo { display: inline-block; background: #fef08a; border-bottom: 2px solid #ca8a04; padding: 1px 8px; border-radius: 2px; font-size: 12px; }

    /* ── Misc ── */
    .section-title { font-size: 18px; font-weight: 600; margin-bottom: 0.5rem; color: #111827; }
    .section-sub   { font-size: 13px; color: #6b7280; margin-bottom: 1.2rem; }
    .divider { border: none; border-top: 1px solid #f3f4f6; margin: 1.5rem 0; }
    </style>
    """, unsafe_allow_html=True)

def cor_nota(nota):
    if nota is None: return "val-blue"
    if nota >= 8:    return "val-green"
    if nota >= 6:    return "val-yellow"
    return "val-red"

def cor_dot(nota):
    if nota is None: return "dot-yellow"
    if nota >= 7:    return "dot-green"
    if nota >= 5:    return "dot-yellow"
    return "dot-red"

def badge_cor(nota):
    if nota is None: return "background:#dbeafe;color:#1d4ed8"
    if nota >= 8:    return "background:#dcfce7;color:#16a34a"
    if nota >= 6:    return "background:#fef3c7;color:#d97706"
    return "background:#fee2e2;color:#dc2626"

def stepper(etapa_atual):
    etapas = ["🔑 Configuração", "📋 Rubricas", "📄 Correção", "📊 Resultados"]
    itens = "".join(
        f'<div class="step-item {"done" if i < etapa_atual else ("active" if i == etapa_atual else "pending")}">'
        f'<span class="step-num">{i+1}</span>{nome}</div>'
        for i, nome in enumerate(etapas)
    )
    st.markdown(f'<div class="stepper">{itens}</div>', unsafe_allow_html=True)

def extrair_texto(arquivo):
    arquivo.seek(0)
    if arquivo.type == "text/plain":
        return arquivo.read().decode("utf-8")
    elif arquivo.type == "application/pdf":
        try:
            from pdfminer.high_level import extract_text_to_fp
            from pdfminer.layout import LAParams
            import io
            arquivo.seek(0)
            out = io.StringIO()
            extract_text_to_fp(arquivo, out, laparams=LAParams(), output_type="text", codec="utf-8")
            texto = out.getvalue()
            if texto.strip(): return texto
        except Exception:
            pass
        try:
            import PyPDF2
            arquivo.seek(0)
            reader = PyPDF2.PdfReader(arquivo)
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except Exception:
            pass
        return "[Não foi possível extrair o texto do PDF. Instale pdfminer.six.]"
    return ""

def aplicar_grifos(texto_raw, anotacoes):
    texto_esc = html_lib.escape(texto_raw)
    anotacoes_ord = sorted(anotacoes, key=lambda a: len(a.get("trecho", "")), reverse=True)
    MARK = "\x00GRIFO\x00"

    for ann in anotacoes_ord:
        trecho = ann.get("trecho", "").strip()
        comentario = html_lib.escape(ann.get("comentario", ""))
        if not trecho or not comentario: continue

        trecho_esc = html_lib.escape(trecho)
        substituicao = f'{MARK}<span class="grifo">{trecho_esc}<span class="tooltip">💬 {comentario}</span></span>{MARK}'

        if trecho_esc in texto_esc:
            texto_esc = texto_esc.replace(trecho_esc, substituicao, 1)
            continue

        palavras = re.split(r'\s+', trecho_esc)
        if len(palavras) < 2: continue
        padrao = r'[\s\S]{0,4}'.join(re.escape(p) for p in palavras[:6])
        m = re.search(padrao, texto_esc)
        if m:
            matched = m.group(0)
            substituicao_fb = f'{MARK}<span class="grifo">{matched}<span class="tooltip">💬 {comentario}</span></span>{MARK}'
            texto_esc = texto_esc[:m.start()] + substituicao_fb + texto_esc[m.end():]

    return texto_esc.replace(MARK, "")
