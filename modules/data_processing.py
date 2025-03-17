"""
Módulo de processamento e transformação de dados.

Responsável por:
- Carregar os dados do arquivo CSV
- Tratar e formatar os dados
- Garantir a integridade dos tipos de dados
"""

import pandas as pd


def load_data(file_path):
    """
    Carrega os dados de um CSV, faz a formatação de datas, converte tipos e renomeia colunas.
    """
    dataframe = pd.read_csv(file_path)  # Lê o arquivo CSV

    # Converte a coluna de data para o formato dd/mm/yyyy
    dataframe["Date"] = pd.to_datetime(dataframe["Date"]).dt.strftime("%d/%m/%Y")

    # Converte colunas numéricas para tipo float
    dataframe[["Unit Price", "Sales Amount", "Discount_Amount", "Final Sales"]] = (
        dataframe[
            ["Unit Price", "Sales Amount", "Discount_Amount", "Final Sales"]
        ].astype(float)
    )

    # Renomeia as colunas para um padrão consistente
    dataframe.columns = [
        "date",
        "customer_id",
        "city",
        "category",
        "product",
        "unit_price",
        "quantity",
        "sales_amount",
        "used_discount",
        "discount_amount",
        "final_sales",
    ]

    # Garante que a coluna de desconto seja do tipo booleano
    dataframe["used_discount"] = dataframe["used_discount"].astype(bool)

    return dataframe
