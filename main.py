"""
Script para processamento e inserção de dados de vendas de café no banco de dados PostgreSQL.

Fluxo:
1. Carrega e processa os dados do arquivo CSV.
2. Conecta ao banco de dados.
3. Cria uma tabela temporária para armazenar os dados.
4. Insere os dados na tabela temporária.
5. Move os dados para a tabela final.
6. Fecha a conexão com o banco.
"""

from sqlalchemy.exc import SQLAlchemyError
from modules.data_processing import load_data
from modules.database import (
    insert_data,
    upsert_data,
    create_engine_connection,
    create_temp_table,
)


def main():
    """
    Função principal que executa o carregamento, processamento e inserção no banco.
    """

    # Caminho do arquivo de dados
    file_path = "data/coffe_sales.csv"

    # Nome da tabela temporária
    temp_table_name = "temp_coffee_beans_sales"

    # Carrega e processa os dados
    df = load_data(file_path)

    # Cria a conexão com o banco
    engine = create_engine_connection()

    try:
        with engine.connect() as connection:

            # Inicia a transação
            trans = connection.begin()

            # Cria a tabela temporária
            create_temp_table(connection, temp_table_name)

            # Insere os dados na tabela temporária
            insert_data(connection, df, temp_table_name)

            # Faz o upsert dos dados na tabela final
            upsert_data(connection, temp_table_name)

            # Confirma a transação
            trans.commit()

            print("Operação concluída com sucesso!")

    except SQLAlchemyError as e:

        # Exibe erro em caso de falha na operação
        print(f"Erro na operação: {e}")

    finally:
        # Fecha a conexão com o banco
        engine.dispose()

        # Exibe informações sobre o DataFrame processado
        print(df.info())


if __name__ == "__main__":

    # Executa a função principal
    main()
