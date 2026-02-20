# 🏗️ Arquiteto Virtual: Gerador de Ecossistema de Dados

Um sistema especialista interativo desenhado para recomendar e visualizar arquiteturas de dados completas e modernas.

O foco desta ferramenta é facilitar a tomada de decisão técnica, construindo pilhas (stacks) robustas de Big Data que ajudam pesquisadores, cientistas e engenheiros a validarem hipóteses de pesquisa e construírem modelos estatísticos com eficiência. A aplicação garante que a arquitetura gerada respeite requisitos fundamentais de governança, rastreabilidade e padronização.

## ✨ Funcionalidades Principais

* **Motor de Recomendação Baseado em Regras:** Sugere automaticamente as melhores ferramentas de Ingestão, Armazenamento, Processamento e Governança com base no licenciamento e no comportamento dos dados.
* **Ênfase na Camada Semântica:** Permite isolar regras de negócio e métricas universais para um consumo padronizado e livre de ambiguidades.
* **Geração Visual em Tempo Real:** Cria diagramas da arquitetura sugerida utilizando a linguagem Mermaid.js renderizada via API.
* **Pronto para Documentação:** O código do fluxograma gerado pode ser copiado e colado diretamente em artigos acadêmicos, apresentações ou documentações em formato texto.

## 🚀 Como Executar Localmente

Certifique-se de ter o Python instalado em sua máquina.

1. Faça o clone deste repositório:
`git clone https://github.com/Irving-Merath/app-decisao-governanca.git`

2. Acesse a pasta do projeto e instale as ferramentas necessárias:
`pip install -r requirements.txt`

3. Inicie o servidor local da aplicação:
`streamlit run app.py`

## 🛠️ Stack Tecnológica

* **Linguagem Base:** Python
* **Interface Web:** Streamlit
* **Estruturação de Dados:** Pandas
* **Diagramação Visual:** Mermaid.js (via integração Base64/SVG)