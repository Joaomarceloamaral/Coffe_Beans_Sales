"""
Módulo de interação com o banco de dados PostgreSQL.

Responsável por:
- Criar conexão com o banco
- Criar tabelas temporárias
- Inserir e atualizar dados
"""

import psycopg2
from sqlalchemy import create_engine, text

CONN_PARAMS = {
    "dbname": "coffe_sales_db",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432",
}


def create_engine_connection():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL.
    """

    database_url = "postgresql://postgres:1234@localhost:5432/coffe_sales_db"

    return create_engine(database_url)


def create_psycopg_conn():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL usando psycopg2.

    Retorna:
        psycopg2.extensions.connection: Objeto de conexão se bem-sucedido.
        None: Se houver erro na conexão.
    """
    try:
        # Estabelece a conexão com o banco de dados
        conn = psycopg2.connect(**CONN_PARAMS)

        # Exibe informações básicas da conexão
        print(f"Database: {conn.info.dbname}")
        print(f"Status: {conn.status}")

        return conn
    except psycopg2.Error as e:
        # Captura e exibe erros de conexão
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def create_temp_table(connection, temp_table_name):
    """
    Cria uma tabela temporária no banco de dados para armazenar os dados antes do upsert.
    """
    create_query = text(
        f"""
        CREATE TEMPORARY TABLE {temp_table_name} (
            date DATE,
            customer_id INT,
            city VARCHAR(20),
            category VARCHAR(25),
            product VARCHAR(25),    
            unit_price NUMERIC(10,2),
            quantity INT,
            sales_amount NUMERIC(10,2),  
            used_discount BOOLEAN,  
            discount_amount NUMERIC(10,2),  
            final_sales NUMERIC(10,2)
        )
        """
    )

    # Executa a criação da tabela temporária
    connection.execute(create_query)


def insert_data(connection, df, temp_table_name):
    """
    Insere os dados processados na tabela temporária do banco de dados.
    """
    if not df.empty:
        data = df.to_dict(
            orient="records"
        )  # Converte o DataFrame para uma lista de dicionários
        insert_query = text(
            f"""
            INSERT INTO {temp_table_name} (date, customer_id, city, category, product, unit_price, quantity, sales_amount, used_discount, discount_amount, final_sales)
            VALUES (:date, :customer_id, :city, :category, :product, :unit_price, :quantity, :sales_amount, :used_discount, :discount_amount, :final_sales)
            """
        )

        # Insere os dados na tabela temporária
        connection.execute(insert_query, data)


def upsert_data(connection, temp_table_name):
    """
    Move os dados da tabela temporária para a tabela final no banco de dados.
    """
    upsert_query = text(
        f"""
        INSERT INTO coffee_beans_sales (date, customer_id, city, category, product, unit_price, quantity, sales_amount, used_discount, discount_amount, final_sales)
        SELECT date, customer_id, city, category, product, unit_price, quantity, sales_amount, used_discount, discount_amount, final_sales FROM {temp_table_name}
        """
    )

    # Executa a inserção dos dados na tabela final
    connection.execute(upsert_query)
