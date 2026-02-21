import streamlit as st
import pandas as pd
import base64
import requests
from io import BytesIO
from docx import Document
from docx.shared import Inches

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Arquiteto de Dados: Gerador de Stack", layout="wide")
st.title("🏗️ Arquiteto Virtual: Ecossistema e Ferramentas")
st.markdown("Gere a arquitetura de referência ideal, explore a tabela de ferramentas e baixe o relatório executivo completo (.docx).")

# --- 2. BASE DE CONHECIMENTO (As 17 Ferramentas) ---
dados = [
    {"nome": "OpenMetadata", "categoria": "Catálogo / Governança", "tipo": "Open Source", "link": "https://open-metadata.org/", "resumo": "Catálogo API-first, focado em colaboração e linhagem.", "facilidade_instalacao": 5, "suporte": 4, "flexibilidade": 5},
    {"nome": "DataHub", "categoria": "Catálogo / Governança", "tipo": "Open Source", "link": "https://datahubproject.io/", "resumo": "Plataforma robusta (LinkedIn), excelente para ecossistemas complexos.", "facilidade_instalacao": 3, "suporte": 4, "flexibilidade": 5},
    {"nome": "Apache Atlas", "categoria": "Catálogo / Governança", "tipo": "Open Source", "link": "https://atlas.apache.org/", "resumo": "Governança profunda e segurança, nativo do ecossistema Hadoop.", "facilidade_instalacao": 2, "suporte": 3, "flexibilidade": 4},
    {"nome": "Atlan", "categoria": "Catálogo / Governança", "tipo": "Comercial / Pago", "link": "https://atlan.com/", "resumo": "Plataforma SaaS super intuitiva, ideal para times de negócios.", "facilidade_instalacao": 5, "suporte": 5, "flexibilidade": 3},
    {"nome": "Cube", "categoria": "Camada Semântica", "tipo": "Open Source", "link": "https://cube.dev/", "resumo": "Camada semântica ('headless BI') que centraliza métricas via API.", "facilidade_instalacao": 4, "suporte": 4, "flexibilidade": 5},
    {"nome": "dbt Semantic Layer", "categoria": "Camada Semântica", "tipo": "Comercial / Pago", "link": "https://www.getdbt.com/product/semantic-layer", "resumo": "Define métricas diretamente nos modelos de transformação dbt.", "facilidade_instalacao": 4, "suporte": 5, "flexibilidade": 4},
    {"nome": "Looker", "categoria": "Camada Semântica", "tipo": "Comercial / Pago", "link": "https://cloud.google.com/looker", "resumo": "Plataforma do Google com linguagem LookML para modelagem forte.", "facilidade_instalacao": 5, "suporte": 5, "flexibilidade": 4},
    {"nome": "Apache Iceberg", "categoria": "Formato de Tabela", "tipo": "Open Source", "link": "https://iceberg.apache.org/", "resumo": "Formato aberto que traz transações seguras para Data Lakes.", "facilidade_instalacao": 3, "suporte": 4, "flexibilidade": 5},
    {"nome": "Delta Lake", "categoria": "Formato de Tabela", "tipo": "Open Source", "link": "https://delta.io/", "resumo": "Traz confiabilidade e performance ACID ao Lakehouse.", "facilidade_instalacao": 4, "suporte": 5, "flexibilidade": 4},
    {"nome": "Apache Hudi", "categoria": "Formato de Tabela", "tipo": "Open Source", "link": "https://hudi.apache.org/", "resumo": "Otimizado para atualizações constantes (upserts) em tempo real.", "facilidade_instalacao": 3, "suporte": 4, "flexibilidade": 4},
    {"nome": "Parquet", "categoria": "Formato de Arquivo", "tipo": "Open Source", "link": "https://parquet.apache.org/", "resumo": "Armazenamento colunar, hiper-comprimido, padrão para análises.", "facilidade_instalacao": 5, "suporte": 5, "flexibilidade": 3},
    {"nome": "Apache Spark", "categoria": "Processamento / Big Data", "tipo": "Open Source", "link": "https://spark.apache.org/", "resumo": "Motor líder para processar clusters massivos de dados.", "facilidade_instalacao": 2, "suporte": 5, "flexibilidade": 5},
    {"nome": "Trino", "categoria": "Motor de Consulta", "tipo": "Open Source", "link": "https://trino.io/", "resumo": "Motor SQL super rápido. Consulta dados onde eles estão.", "facilidade_instalacao": 2, "suporte": 5, "flexibilidade": 5},
    {"nome": "DuckDB", "categoria": "Motor de Consulta", "tipo": "Open Source", "link": "https://duckdb.org/", "resumo": "Banco analítico ultrarrápido que roda na própria máquina.", "facilidade_instalacao": 5, "suporte": 5, "flexibilidade": 5},
    {"nome": "Oracle", "categoria": "Banco de Dados", "tipo": "Comercial / Pago", "link": "https://www.oracle.com/database/", "resumo": "Banco relacional tradicional, altíssima resiliência e custo.", "facilidade_instalacao": 1, "suporte": 5, "flexibilidade": 2},
    {"nome": "Apache Kafka", "categoria": "Streaming de Dados", "tipo": "Open Source", "link": "https://kafka.apache.org/", "resumo": "Plataforma de streaming de eventos em tempo real.", "facilidade_instalacao": 2, "suporte": 5, "flexibilidade": 5},
    {"nome": "Schema Registry", "categoria": "Streaming de Dados", "tipo": "Open Source", "link": "https://docs.confluent.io/platform/current/schema-registry/index.html", "resumo": "Garante que eventos sigam um formato de contrato rígido.", "facilidade_instalacao": 3, "suporte": 5, "flexibilidade": 4}
]
df = pd.DataFrame(dados)

# --- 3. INTERFACE DE PERGUNTAS (SIDEBAR) ---
st.sidebar.header("Filtros e Diretrizes")

categorias_disponiveis = ["Todas"] + sorted(list(df['categoria'].unique()))
filtro_categoria = st.sidebar.selectbox("0. Filtrar Tabela por Categoria?", categorias_disponiveis)

st.sidebar.markdown("---")
modelo_licenca = st.sidebar.radio("1. Preferência de licenciamento?", ("Mostrar Todos", "Apenas Open Source", "Apenas Comercial / Pago"))
cenario_dados = st.sidebar.radio("2. Comportamento dos dados?", ("Processamento em Lote (Lakehouse, Histórico)", "Streaming em Tempo Real (Eventos)"))
exige_semantica = st.sidebar.checkbox("3. Implementar Camada Semântica?", value=True)

st.sidebar.markdown("---")
nota_suporte = st.sidebar.slider("Suporte Mínimo (1 a 5)", 1, 5, 1)
nota_flexibilidade = st.sidebar.slider("Flexibilidade Mínima (1 a 5)", 1, 5, 1)

# --- 4. MOTOR DA ARQUITETURA ---
st.subheader("🗺️ Desenho da Arquitetura Recomendada")

camada_ingestao, camada_armazenamento, camada_processamento, camada_semantica_tool, camada_governanca, justificativa = "", "", "", "", "", ""

if modelo_licenca == "Apenas Comercial / Pago":
    if "Streaming" in cenario_dados:
        camada_ingestao, camada_armazenamento, camada_processamento, camada_governanca = "Confluent Cloud (Kafka)", "Oracle Cloud / Delta Lake", "Databricks (Spark)", "Atlan"
        justificativa = "Soluções gerenciadas focadas em streaming em tempo real com governança premium."
    else: 
        camada_ingestao, camada_armazenamento, camada_processamento, camada_governanca = "Fivetran / SaaS", "Delta Lake ou Oracle", "Motores Nativos de Nuvem", "Atlan"
        justificativa = "Arquitetura corporativa clássica para lotes históricos, priorizando suporte SLA."
    camada_semantica_tool = "Looker ou dbt Semantic Layer" if exige_semantica else "Não implementada"
else:
    if "Streaming" in cenario_dados:
        camada_ingestao, camada_armazenamento, camada_processamento, camada_governanca = "Apache Kafka + Schema Registry", "Apache Hudi (Data Lake)", "Apache Spark (Streaming)", "DataHub"
        justificativa = "Stack livre voltada para eventos. Kafka move os dados e o DataHub mapeia a alta complexidade."
    else: 
        camada_ingestao, camada_armazenamento, camada_processamento, camada_governanca = "Processos Batch (Python/Airflow)", "Apache Iceberg + Parquet", "DuckDB (Local) ou Trino", "OpenMetadata"
        justificativa = "Infraestrutura robusta de Lakehouse para análises locais e distribuídas de grandes bases."
    camada_semantica_tool = "Cube" if exige_semantica else "Não implementada"

st.write(f"**Visão Geral:** {justificativa}")

mermaid_code = f"""graph LR
    subgraph Ingestao ["Ingestão e Dados Brutos"]
        A["{camada_ingestao}"]
    end
    subgraph Armazenamento ["Armazenamento e Processamento"]
        B["{camada_armazenamento}"]
        C["{camada_processamento}"]
    end
    subgraph Consumo ["Consumo e Negócios"]
        D["{camada_semantica_tool}"]
        E["Aplicações (BI, Python, R)"]
    end
    subgraph Governanca ["Governança"]
        F["{camada_governanca}"]
    end
    A -->|"Carrega Dados"| B
    B -->|"Consulta"| C
"""
if exige_semantica:
    mermaid_code += "    C -->|\"Padroniza Métricas\"| D\n    D -->|\"Consome\"| E\n"
else:
    mermaid_code += "    C -->|\"Consome Direto\"| E\n"
mermaid_code += "    F -.- A\n    F -.- B\n    F -.- C\n    F -.- D\n    style F fill:#4a148c,stroke:#fff,color:#fff\n    style D fill:#00695c,stroke:#fff,color:#fff"

# Renderiza Diagrama na Tela
graphbytes = mermaid_code.encode("utf8")
base64_bytes = base64.b64encode(graphbytes)
base64_string = base64_bytes.decode('ascii')
st.image(f"https://mermaid.ink/svg/{base64_string}", use_container_width=True)

# --- 5. LÓGICA DE GERAÇÃO DO DOCUMENTO WORD (.DOCX) ---
def gerar_relatorio_word(df_filtrado, b64_diagrama):
    doc = Document()
    doc.add_heading('Relatório de Arquitetura de Dados', 0)
    
    # Seção 1: Justificativas Detalhadas
    doc.add_heading('1. Descrição e Justificativa da Stack', level=1)
    
    doc.add_heading('Governança e Catálogo:', level=2)
    if camada_governanca == "OpenMetadata":
        doc.add_paragraph("Foi escolhida a ferramenta OpenMetadata porque ela é open source, apropriada para catálogo, é altamente customizável e focada em colaboração. Seu principal forte é a linhagem de dados nativa, ou seja, é possível ver visualmente de onde o dado saiu, pra onde foi e quais scripts o alteraram no caminho.")
    elif camada_governanca == "DataHub":
        doc.add_paragraph("Foi escolhida a ferramenta DataHub porque é uma plataforma open source desenvolvida para suportar ecossistemas altamente complexos que envolvem streaming (como Kafka). Ela garante que todo o fluxo em tempo real fique mapeado e auditável.")
    else:
        doc.add_paragraph("Foi escolhida a ferramenta Atlan por ser uma solução comercial focada em facilidade de uso para times de negócio. Ela não exige manutenção técnica e oferece integrações nativas prontas para uso.")

    doc.add_heading('Ingestão de Dados Brutos:', level=2)
    if "Python/Airflow" in camada_ingestao:
        doc.add_paragraph("Foi escolhido Python/Airflow (Processos Batch) porque o fluxo analítico depende de bases históricas ou atualizações agendadas em lotes. O Airflow orquestra esses scripts de forma programática e altamente customizável sem custos de licença.")
    else:
        doc.add_paragraph(f"Foi escolhido o uso de {camada_ingestao} para garantir confiabilidade no transporte dos dados, suportando grandes volumes de eventos de negócios sem perda de pacotes.")

    doc.add_heading('Armazenamento e Formatos:', level=2)
    if "Iceberg" in camada_armazenamento:
        doc.add_paragraph("Foi sugerida a combinação de Apache Iceberg e Parquet. O formato Parquet comprime as informações colunarmente (ideal para pesquisas pesadas), enquanto o Iceberg cria uma camada de controle, permitindo que os pesquisadores consultem o Data Lake com comandos SQL rápidos e transacionais, como se fosse um banco de dados tradicional.")
    else:
        doc.add_paragraph(f"A arquitetura utilizará {camada_armazenamento} para garantir que os dados fiquem unificados, seguros e prontos para alimentar a camada de processamento com alta performance.")

    doc.add_heading('Processamento / Consultas:', level=2)
    if "DuckDB" in camada_processamento:
        doc.add_paragraph("Foi escolhido o DuckDB e Trino pela revolução que trazem na etapa de pesquisa. O DuckDB roda diretamente na máquina do analista (junto com scripts Python ou R), devorando arquivos em velocidade recorde, sem precisar de infraestrutura pesada.")
    else:
        doc.add_paragraph(f"O {camada_processamento} foi o motor escolhido por ser o padrão de mercado para distribuir processamento massivo, capaz de lidar com transformações complexas ou streaming de dados em escala.")

    doc.add_heading('Camada Semântica:', level=2)
    if exige_semantica:
        doc.add_paragraph(f"Foi implementada a solução {camada_semantica_tool} para centralizar as regras de pesquisa. Isso significa que variáveis como 'taxa de infecção' não ficarão perdidas em scripts individuais; elas são definidas de forma única na camada semântica e consumidas por qualquer painel ou linguagem, garantindo a veracidade das métricas.")
    else:
        doc.add_paragraph("Camada semântica não implementada nesta topologia. As regras de negócio e cálculos de pesquisa serão aplicados diretamente nos painéis ou rotinas de análise de cada usuário.")

    # Seção 2: Imagem do Diagrama
    doc.add_heading('2. Fluxograma da Arquitetura', level=1)
    try:
        url_imagem = f"https://mermaid.ink/img/{b64_diagrama}?type=png"
        resposta = requests.get(url_imagem)
        if resposta.status_code == 200:
            imagem_io = BytesIO(resposta.content)
            doc.add_picture(imagem_io, width=Inches(6.0))
        else:
            doc.add_paragraph("[Erro ao baixar o diagrama online para inclusão no documento.]")
    except Exception as e:
        doc.add_paragraph(f"[Aviso: A geração da imagem exige conexão com a internet. Erro: {str(e)}]")

    # Seção 3: Tabela
    doc.add_heading('3. Lista de Ferramentas Avaliadas', level=1)
    tabela = doc.add_table(rows=1, cols=3)
    tabela.style = 'Table Grid'
    hdr_cells = tabela.rows[0].cells
    hdr_cells[0].text = 'Ferramenta'
    hdr_cells[1].text = 'Categoria'
    hdr_cells[2].text = 'Resumo'
    
    for _, row in df_filtrado.iterrows():
        row_cells = tabela.add_row().cells
        row_cells[0].text = str(row['nome'])
        row_cells[1].text = str(row['categoria'])
        row_cells[2].text = str(row['resumo'])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 6. TABELA DETALHADA E BOTÕES DE EXPORTAÇÃO ---
st.divider()
st.subheader("📊 Ecossistema e Exportação")

# Filtra o DataFrame dinamicamente
recomendacoes = df.copy()
if filtro_categoria != "Todas": recomendacoes = recomendacoes[recomendacoes['categoria'] == filtro_categoria]
if modelo_licenca == "Apenas Open Source": recomendacoes = recomendacoes[recomendacoes['tipo'] == "Open Source"]
elif modelo_licenca == "Apenas Comercial / Pago": recomendacoes = recomendacoes[recomendacoes['tipo'] == "Comercial / Pago"]
recomendacoes = recomendacoes[(recomendacoes['suporte'] >= nota_suporte) & (recomendacoes['flexibilidade'] >= nota_flexibilidade)]

if recomendacoes.empty:
    st.warning("Nenhuma ferramenta atende aos critérios selecionados.")
else:
    recomendacoes['Nota Final'] = recomendacoes['suporte'] + recomendacoes['flexibilidade'] + recomendacoes['facilidade_instalacao']
    recomendacoes = recomendacoes.sort_values(by='Nota Final', ascending=False)
    
    st.dataframe(
        recomendacoes[['nome', 'categoria', 'tipo', 'resumo', 'suporte', 'flexibilidade']],
        hide_index=True, use_container_width=True
    )
    
    # Criando colunas para os botões ficarem lado a lado
    col1, col2 = st.columns([1, 1])
    
    with col1:
        csv_data = recomendacoes.to_csv(index=False, sep=';', encoding='utf-8-sig')
        st.download_button(
            label="📥 Baixar Tabela em CSV",
            data=csv_data,
            file_name="ferramentas_arquitetura.csv",
            mime="text/csv"
        )
        
    with col2:
        relatorio_docx = gerar_relatorio_word(recomendacoes, base64_string)
        st.download_button(
            label="📄 Baixar Relatório Executivo (.docx)",
            data=relatorio_docx,
            file_name="Relatorio_Arquitetura_Dados.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )