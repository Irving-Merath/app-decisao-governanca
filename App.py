import streamlit as st
import pandas as pd
import base64
import requests
from io import BytesIO
from docx import Document
from docx.shared import Inches

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Governança de Dados: Gerador de Stack", layout="wide")
st.title("Arquitetura de dados: Ecossistema e Ferramentas")
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
    {"nome": "Trino", "categoria": "Motor de Consulta", "tipo": "Open Source", "link": "https://trino.io/", "resumo": "Motor SQL para nuvem. Consulta dados pesados direto no Lake.", "facilidade_instalacao": 2, "suporte": 5, "flexibilidade": 5},
    {"nome": "DuckDB", "categoria": "Motor de Consulta", "tipo": "Open Source", "link": "https://duckdb.org/", "resumo": "Banco analítico ultrarrápido que roda localmente na máquina do analista.", "facilidade_instalacao": 5, "suporte": 5, "flexibilidade": 5},
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
        camada_ingestao, camada_armazenamento, camada_processamento, camada_governanca = "Processos Batch (Python/Airflow)", "Apache Iceberg + Parquet", "Trino (Nuvem) + DuckDB (Local)", "OpenMetadata"
        justificativa = "O Trino filtra Terabytes de dados massivos na nuvem, enquanto o DuckDB permite que o analista processe o resultado localmente no R/Python em altíssima velocidade."
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
    
    # Metodologia
    doc.add_heading('1. Metodologia de Avaliação das Ferramentas', level=1)
    doc.add_paragraph("As notas de Suporte e Flexibilidade apresentadas neste relatório foram estabelecidas com base nos seguintes critérios técnicos do mercado:")
    doc.add_paragraph("• Suporte (1 a 5): Avalia o tempo de maturidade da ferramenta, o tamanho e o engajamento da comunidade (para soluções Open Source) ou o nível de serviço corporativo (SLA). Uma nota 5 indica que a ferramenta possui anos no mercado, vasta documentação oficial clara e uma comunidade ativa capaz de solucionar eventuais problemas rapidamente.")
    doc.add_paragraph("• Flexibilidade (1 a 5): Avalia o grau em que a ferramenta pode ser customizada e integrada ao ecossistema moderno. Uma nota 5 indica que ela oferece APIs abertas, integra-se de forma nativa com as principais linguagens de análise (Python, R, Java, SQL) e utiliza padrões abertos que evitam o aprisionamento tecnológico (vendor lock-in).")

    # Arquitetura Macro
    doc.add_heading('2. Visão Macro da Arquitetura', level=1)
    
    # NOVO: Texto introdutório dinâmico
    resumo_macro = (
        f"A figura abaixo apresenta o diagrama da arquitetura recomendada, passando pelas camadas de Governança, "
        f"Ingestão de dados brutos, Armazenamento e processamento, e Consumo e negócios. Para este projeto, "
        f"foi selecionado {camada_governanca} para a Governança; {camada_ingestao} para a Ingestão; "
        f"{camada_armazenamento} e {camada_processamento} para o Armazenamento e processamento; e "
        f"{camada_semantica_tool} para a padronização e consumo."
    )
    doc.add_paragraph(resumo_macro)
    
    # Mantendo a justificativa detalhada logo abaixo do resumo
    doc.add_paragraph(f"Detalhe da topologia: {justificativa}")
    
    try:
        url_imagem = f"https://mermaid.ink/img/{b64_diagrama}?type=png"
        resposta = requests.get(url_imagem)
        if resposta.status_code == 200:
            doc.add_picture(BytesIO(resposta.content), width=Inches(6.0))
    except Exception:
        doc.add_paragraph("[Aviso: Imagem do diagrama indisponível offline.]")

    # Tabela com Links
    doc.add_heading('3. Tabela de Ferramentas Recomendadas', level=1)
    tabela = doc.add_table(rows=1, cols=4)
    tabela.style = 'Table Grid'
    hdr = tabela.rows[0].cells
    hdr[0].text = 'Ferramenta'
    hdr[1].text = 'Categoria'
    hdr[2].text = 'Resumo'
    hdr[3].text = 'Site / Link'
    
    for _, row in df_filtrado.iterrows():
        row_cells = tabela.add_row().cells
        row_cells[0].text = str(row['nome'])
        row_cells[1].text = str(row['categoria'])
        row_cells[2].text = str(row['resumo'])
        row_cells[3].text = str(row['link'])

    # Justificativas Dinâmicas das Ferramentas
    doc.add_heading('4. Justificativa Detalhada por Ferramenta', level=1)
    
    for _, row in df_filtrado.iterrows():
        doc.add_heading(f"{row['nome']} ({row['categoria']})", level=2)
        
        # Textos dinâmicos para suporte
        texto_sup = ""
        if row['suporte'] == 5: texto_sup = "é amplamente consolidada, com documentação farta, longo histórico de estabilidade no mercado e uma comunidade engajada (ou SLA corporativo premium) para resolução imediata de problemas."
        elif row['suporte'] == 4: texto_sup = "possui ótima documentação e canais ativos que resolvem a imensa maioria dos casos de uso de pesquisa."
        elif row['suporte'] <= 3: texto_sup = "oferece o suporte básico necessário, porém pode exigir maior conhecimento técnico da equipe interna para configurações avançadas."
        
        # Textos dinâmicos para flexibilidade
        texto_flex = ""
        if row['flexibilidade'] == 5: texto_flex = "é altamente customizável, integra-se com facilidade a múltiplas ferramentas analíticas, aceita linguagens variadas (Python, R, SQL, etc.) e foca em padrões abertos."
        elif row['flexibilidade'] == 4: texto_flex = "oferece excelentes conexões nativas com o ecossistema moderno de dados e atende à maioria dos padrões de engenharia."
        elif row['flexibilidade'] <= 3: texto_flex = "possui um ecossistema mais contido, operando de forma muito eficiente dentro do seu propósito específico, com menos opções de customização extrema."

        paragrafo = f"Foi escolhida a ferramenta {row['nome']} para a categoria de {row['categoria']} porque ela atende perfeitamente aos requisitos do projeto ({row['resumo']}). "
        paragrafo += f"Sua nota {row['suporte']} para suporte indica que ela {texto_sup} "
        paragrafo += f"Além disso, sua nota {row['flexibilidade']} para flexibilidade indica que ela {texto_flex}"
        
        doc.add_paragraph(paragrafo)

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
        recomendacoes[['nome', 'categoria', 'tipo', 'resumo', 'suporte', 'flexibilidade', 'link']],
        column_config={
            "nome": "Ferramenta", "categoria": "Categoria", "tipo": "Licença", "resumo": "O que faz?",
            "suporte": "Suporte (1-5)", "flexibilidade": "Customização (1-5)",
            "link": st.column_config.LinkColumn("Site Oficial")
        },
        hide_index=True, use_container_width=True
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        csv_data = recomendacoes.to_csv(index=False, sep=';', encoding='utf-8-sig')
        st.download_button("📥 Baixar Tabela em CSV", data=csv_data, file_name="ferramentas.csv", mime="text/csv")
    with col2:
        relatorio_docx = gerar_relatorio_word(recomendacoes, base64_string)
        st.download_button("📄 Baixar Relatório Completo (.docx)", data=relatorio_docx, file_name="Relatorio_Arquitetura.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")