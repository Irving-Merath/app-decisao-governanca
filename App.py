import streamlit as st
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Arquiteto de Dados: Gerador de Stack", layout="wide")
st.title("🏗️ Arquiteto Virtual: Gerador de Ecossistema de Dados")
st.markdown("Responda às perguntas estratégicas abaixo para gerarmos a arquitetura completa da sua solução, conectando as ferramentas corretas.")

# --- 2. INTERFACE DE PERGUNTAS (SIDEBAR) ---
st.sidebar.header("Diretrizes da Arquitetura")

modelo_licenca = st.sidebar.radio(
    "1. Qual a sua preferência de licenciamento?",
    ("100% Open Source (Foco em custo zero de licença)", "Comercial / SaaS (Foco em suporte corporativo)")
)

cenario_dados = st.sidebar.radio(
    "2. Qual o comportamento principal dos dados?",
    ("Processamento em Lote (Bases históricas, pesquisa, Lakehouse)", "Streaming em Tempo Real (Eventos, alertas instantâneos)")
)

exige_semantica = st.sidebar.checkbox("3. Implementar Camada Semântica?", value=True, help="Centraliza regras de negócio e métricas para consumo padronizado.")

# --- 3. MOTOR DE REGRAS (Montagem da Arquitetura) ---
camada_ingestao = ""
camada_armazenamento = ""
camada_processamento = ""
camada_semantica_tool = ""
camada_governanca = ""
justificativa = ""

if modelo_licenca == "100% Open Source (Foco em custo zero de licença)":
    if cenario_dados == "Streaming em Tempo Real (Eventos, alertas instantâneos)":
        camada_ingestao = "Apache Kafka + Schema Registry"
        camada_armazenamento = "Apache Hudi (Data Lake)"
        camada_processamento = "Apache Spark (Streaming)"
        camada_governanca = "DataHub"
        justificativa = "O Kafka move os dados, o Schema Registry garante que o formato não quebre, o Hudi atualiza os registros rapidamente e o DataHub documenta ambientes complexos."
    else: 
        camada_ingestao = "Processos Batch (Python/Airflow)"
        camada_armazenamento = "Apache Iceberg + Parquet"
        camada_processamento = "DuckDB (Local) ou Trino (Distribuído)"
        camada_governanca = "OpenMetadata"
        justificativa = "O Iceberg organiza os arquivos Parquet. O DuckDB permite que pesquisadores consultem gigabytes de dados direto na própria máquina em segundos. O OpenMetadata documenta tudo com uma interface amigável."
    
    camada_semantica_tool = "Cube" if exige_semantica else "Não implementada"

else: 
    if cenario_dados == "Streaming em Tempo Real (Eventos, alertas instantâneos)":
        camada_ingestao = "Confluent Cloud (Kafka)"
        camada_armazenamento = "Oracle Cloud / Delta Lake"
        camada_processamento = "Databricks (Spark)"
        camada_governanca = "Atlan"
        justificativa = "Soluções totalmente gerenciadas. O Confluent cuida do streaming e o Databricks do processamento pesado, tudo catalogado pelo Atlan."
    else: 
        camada_ingestao = "Fivetran / Ferramentas SaaS"
        camada_armazenamento = "Delta Lake (Databricks) ou Oracle"
        camada_processamento = "Motores Nativos de Nuvem"
        camada_governanca = "Atlan"
        justificativa = "Arquitetura corporativa clássica de alta resiliência e suporte garantido. Ferramentas integradas nativamente."
    
    camada_semantica_tool = "Looker ou dbt Semantic Layer" if exige_semantica else "Não implementada"

# --- 4. EXIBIÇÃO DO RESULTADO ---
st.divider()

st.success("✅ Arquitetura de Referência Gerada com Sucesso!")
st.write(f"**Justificativa do Arquiteto:** {justificativa}")

st.subheader("🛠️ Componentes do seu Ecossistema")
st.markdown(f"""
* **1. Ingestão / Movimentação:** {camada_ingestao}
* **2. Armazenamento / Formato:** {camada_armazenamento}
* **3. Processamento / Consulta:** {camada_processamento}
* **4. Camada Semântica:** {camada_semantica_tool}
* **5. Governança, Catálogo e Linhagem:** {camada_governanca}
""")

# --- 5. ÁRVORE VISUAL (ABORDAGEM BLINDADA VIA IMAGEM API) ---
st.subheader("🗺️ Diagrama da Arquitetura")

mermaid_code = f"""graph LR
    subgraph Ingestao ["Camada de Dados Brutos e Ingestão"]
        A["{camada_ingestao}"]
    end
    
    subgraph Armazenamento ["Armazenamento e Processamento"]
        B["{camada_armazenamento}"]
        C["{camada_processamento}"]
    end
    
    subgraph Consumo ["Consumo e Negócios"]
        D["{camada_semantica_tool}"]
        E["Ferramentas de Pesquisa <br> R, Python, BI"]
    end
    
    subgraph Governanca ["Governança e Documentação"]
        F["{camada_governanca} <br> Catálogo e Linhagem"]
    end

    A -->|"Carrega Dados"| B
    B -->|"Consulta Rápida"| C
"""

if exige_semantica:
    mermaid_code += "    C -->|\"Padroniza Métricas\"| D\n"
    mermaid_code += "    D -->|\"Consome Dados\"| E\n"
else:
    mermaid_code += "    C -->|\"Consome Direto\"| E\n"

mermaid_code += """
    F -.- A
    F -.- B
    F -.- C
    F -.- D
    
    style F fill:#4a148c,stroke:#fff,color:#fff
    style D fill:#00695c,stroke:#fff,color:#fff
"""

# Transformando o texto do diagrama em uma imagem SVG em tempo real
graphbytes = mermaid_code.encode("utf8")
base64_bytes = base64.b64encode(graphbytes)
base64_string = base64_bytes.decode("ascii")

image_url = f"https://mermaid.ink/svg/{base64_string}"

# Mostrando a imagem no Streamlit de forma segura
st.image(image_url, use_container_width=True)

# Exportação do Código
st.markdown("### 🖨️ Exportar Diagrama para Projetos")
st.text_area("Código-fonte do Fluxograma (Mermaid):", mermaid_code, height=200)
st.markdown("Copie o código acima e cole no **[Mermaid Live](https://mermaid.live/)** para exportar em PNG ou SVG de alta qualidade.")