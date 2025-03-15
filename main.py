# %%
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# %%
coffe_sales_df = pd.read_csv("data/coffe_sales.csv")

# %%
coffe_sales_df["Date"] = pd.to_datetime(coffe_sales_df["Date"])
coffe_sales_df["Date"] = coffe_sales_df["Date"].dt.strftime("%d/%m/%Y")

# %%
coffe_sales_df[["Unit Price", "Sales Amount", "Discount_Amount", "Final Sales"]] = (
    coffe_sales_df[
        ["Unit Price", "Sales Amount", "Discount_Amount", "Final Sales"]
    ].astype(float)
)

# %%
novos_nomes = [
    "date",
    "customer_id",
    "city",
    "category",
    "product_name",
    "unit_price",
    "quantity",
    "sales_amount",
    "used_discount",
    "discount_amount",
    "final_sales",
]


# %%
coffe_sales_df.columns = novos_nomes
customers_df = coffe_sales_df[["customer_id", "city"]]

products_df = coffe_sales_df[["category", "product_name", "unit_price"]]

print(products_df)

# %%
# Criar a conexão com o banco de dados PostgreSQL
engine = create_engine("postgresql://postgres:1234@localhost:5432/coffe_sales_db")


# %%
try:
    # Usar uma única conexão para toda a operação
    with engine.connect() as connection:
        # Iniciar transação explícita
        trans = connection.begin()

        temp_table_name = "temp_customers"

        # 1. Criar tabela temporária usando DDL explícito (somente 'city')
        create_temp_table = text(
            f"""
            CREATE TEMPORARY TABLE {temp_table_name} (
                city VARCHAR(20)
            )
        """
        )
        connection.execute(create_temp_table)

        # 2. Inserir dados do DataFrame
        if not customers_df.empty:
            # Converter para lista de dicionários
            data = customers_df[["city"]].to_dict(orient="records")

            # Inserção em lote
            connection.execute(
                text(
                    f"""
                    INSERT INTO {temp_table_name} (city)
                    VALUES (:city)
                """
                ),
                data,
            )

        # 3. Fazer upsert na tabela principal (somente 'city')
        upsert_query = text(
            f"""
            INSERT INTO customers (city)
            SELECT city FROM {temp_table_name}
        """
        )
        connection.execute(upsert_query)

        # Commit final
        trans.commit()
        print("Operação concluída com sucesso!")

except SQLAlchemyError as e:
    print(f"Erro na operação: {e}")
    # O rollback é automático com o context manager 'with'

finally:
    engine.dispose()

# %%
try:
    # Usar uma única conexão para toda a operação
    with engine.connect() as connection:
        # Iniciar transação explícita
        trans = connection.begin()

        temp_table_name = "temp_products"

        # 1. Criar tabela temporária usando (somente 'category', 'product_name', 'unit_price')
        create_temp_table = text(
            f"""
            CREATE TEMPORARY TABLE {temp_table_name} (
                category VARCHAR(25),
                product_name VARCHAR(25),
                unit_price NUMERIC(10,2)
            )
        """
        )
        connection.execute(create_temp_table)

        # 2. Inserir dados do DataFrame
        if not products_df.empty:
            # Converter para lista de dicionários
            data = products_df[["category", "product_name", "unit_price"]].to_dict(
                orient="records"
            )

            # Inserção em lote
            connection.execute(
                text(
                    f"""
                    INSERT INTO {temp_table_name} (category, product_name, unit_price)
                    VALUES (:category, :product_name, :unit_price)
                """
                ),
                data,
            )

        # 3. Fazer upsert na tabela principal (somente 'category', 'product_name', 'unit_price')
        upsert_query = text(
            f"""
            INSERT INTO products (category, product_name, unit_price)
            SELECT category, product_name, unit_price FROM {temp_table_name}
        """
        )
        connection.execute(upsert_query)

        # Commit final
        trans.commit()
        print("Operação concluída com sucesso para a tabela 'products'!")

except SQLAlchemyError as e:
    print(f"Erro na operação: {e}")
    # O rollback é automático com o context manager 'with'

finally:
    engine.dispose()
