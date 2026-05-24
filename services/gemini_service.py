import google.generativeai as genai
import typing_extensions as Ext
import json

MODEL_NAME = "models/gemini-2.5-flash"

# --- Schemas de Validação Estrita ---
class ItemRubrica(Ext.TypedDict):
    criterio: str
    peso: int
    descricao: str

class CriterioAvaliado(Ext.TypedDict):
    criterio: str
    nota: float
    justificativa: str

class AnotacaoInline(Ext.TypedDict):
    trecho: str
    comentario: str

class SchemaCorrecao(Ext.TypedDict):
    nota_global: float
    criterios: list[CriterioAvaliado]
    anotacoes: list[AnotacaoInline]

# --- Helpers de Arquivo ---
def _upload_to_parts(uploaded_files):
    parts = []
    for f in (uploaded_files or []):
        f.seek(0)
        bytes_data = f.read()
        mime_type = f.type
        if f.name.endswith(".txt") or mime_type == "text/plain":
            mime_type = "text/plain"
        elif f.name.endswith(".pdf") or mime_type == "application/pdf":
            mime_type = "application/pdf"
        parts.append({"mime_type": mime_type, "data": bytes_data})
    return parts

# --- Chamadas de API ---
def validar_chave(api_key):
    genai.configure(api_key=api_key)
    genai.GenerativeModel(MODEL_NAME).generate_content("ok")

def gerar_rubricas_ia(api_key, diretrizes, arquivos_contexto):
    genai.configure(api_key=api_key)
    prompt = (
        "Gere critérios amplos de avaliação acadêmica (rubricas) com pesos em %, somando 100%.\n"
        "Os critérios devem ser específicos ao trabalho abordado nos arquivos de contexto, de modo que um trabalho sobre outro tema deve receber nota zero.\n"
        "Os critérios devem ser tão específicos quanto possível.\n"
        f"Diretrizes do professor:\n{diretrizes or '[sem diretrizes]'}"
    )
    content = [{"text": prompt}] + _upload_to_parts(arquivos_contexto)
    model = genai.GenerativeModel(MODEL_NAME)
    resp = model.generate_content(
        content,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=list[ItemRubrica]
        )
    )
    return json.loads(resp.text)

def corrigir_trabalho_ia(api_key, arquivo_trabalho, rubricas, diretrizes, arquivos_contexto):
    genai.configure(api_key=api_key)
    criterios_txt = "\n".join(f'- {r["criterio"]} ({r["peso"]}%): {r.get("descricao","")}' for r in rubricas)
    
    prompt = (
        "Avalie o trabalho acadêmico usando ESTRITAMENTE os critérios abaixo, padronizando a avaliação global de 0 a 100.\n"
        "Identifique de 4 a 8 trechos relevantes do texto (positivos ou negativos) e escreva uma anotação.\n"
        "Os trechos devem ser COPIADOS LITERALMENTE do texto — mínimo 6 palavras.\n\n"
        f"Critérios:\n{criterios_txt}\n\nDiretrizes:\n{diretrizes or '[sem]'}"
    )
    content = [{"text": prompt}] + _upload_to_parts(arquivos_contexto) + _upload_to_parts([arquivo_trabalho])
    model = genai.GenerativeModel(MODEL_NAME)
    resp = model.generate_content(
        content,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=SchemaCorrecao
        )
    )
    return json.loads(resp.text)

def gerar_insights_ia(api_key, historico, rubricas, diretrizes, arquivos_contexto):
    genai.configure(api_key=api_key)
    resumo = "\n".join(
        f"Aluno '{h['nome']}': nota {h['nota_global']} | " + " | ".join(f"{c['criterio']}={c['nota']}" for c in h.get("criterios", []))
        for h in historico
    )
    criterios_txt = "\n".join(f'- {r["criterio"]} ({r["peso"]}%)' for r in rubricas)
    prompt = (
        "Analise o conjunto de correções abaixo e escreva 3 a 5 frases descritivas dirigidas ao professor, destacando padrões, gargalos e pontos fortes.\n"
        f"Critérios:\n{criterios_txt}\n\nDiretrizes:\n{diretrizes or '[sem]'}\n\nCorreções:\n{resumo}"
    )
    content = [{"text": prompt}] + _upload_to_parts(arquivos_contexto)
    resp = genai.GenerativeModel(MODEL_NAME).generate_content(content)
    return resp.text.strip()
