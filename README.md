# Projeto de ETL e BI para Vendas de Café ☕📊

Este repositório contém um script em Python para tratamento de dados de um arquivo CSV, realizando o processo de ETL (Extract, Transform, Load) e alimentando um banco de dados, que serve como fonte para um sistema de Business Intelligence (BI).

## Descrição do Projeto
O objetivo deste projeto é automatizar o processo de importação, transformação e carregamento dos dados de vendas de café, fornecendo insights valiosos por meio de ferramentas de BI.

## Funcionalidades
- **Extração de Dados:** Carrega os dados de um arquivo CSV contendo informações de vendas de café.
- **Transformação de Dados:** Limpa e transforma os dados, incluindo:
  - Conversão de tipos de dados
  - Tratamento de valores nulos
  - Formatação de datas
- **Carregamento de Dados:** Insere os dados transformados em um banco de dados SQL.
- **Integração com BI:** Utiliza ferramentas de BI para criar relatórios e painéis interativos.

## Requisitos
- Python 3.x
- Pandas
- SQLAlchemy
- Ferramenta de BI (ex.: Power BI, Tableau)

## Como Usar
1. Clone este repositório.
2. Instale as dependências listadas em `requirements.txt`.
3. Configure a conexão com o banco de dados no arquivo `config.py`.
4. Execute o script `etl.py` para processar e carregar os dados.
5. Utilize a ferramenta de BI para criar visualizações e analisar os dados.
