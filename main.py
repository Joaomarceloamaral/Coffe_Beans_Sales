# %%
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# %%
coffee_sales_df = pd.read_csv("data/coffe_sales.csv")
print(coffee_sales_df)

# %%
coffee_sales_df["Date"] = pd.to_datetime(coffee_sales_df["Date"])
coffee_sales_df["Date"] = coffee_sales_df["Date"].dt.strftime("%d/%m/%Y")

# %%
coffee_sales_df[["Unit Price", "Sales Amount", "Discount_Amount", "Final Sales"]] = (
    coffee_sales_df[
        ["Unit Price", "Sales Amount", "Discount_Amount", "Final Sales"]
    ].astype(float)
)

# %%
novos_nomes = [
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

# %%
coffee_sales_df.columns = novos_nomes


# %%
coffee_sales_df["used_discount"].astype(bool)

print(coffee_sales_df.info())

# %%
engine = create_engine("postgresql://postgres:1234@localhost:5432/coffe_sales_db")


# %%
try:
    with engine.connect() as connection:

        trans = connection.begin()

        TEMP_TABLE = "temp_coffee_beans_sales"

        CREATE_TEMP_TB = text(
            f"""
            CREATE TEMPORARY TABLE {TEMP_TABLE} (
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
        connection.execute(CREATE_TEMP_TB)

        if not coffee_sales_df.empty:

            data = coffee_sales_df[
                [
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
            ].to_dict(orient="records")

            connection.execute(
                text(
                    f"""
                    INSERT INTO {TEMP_TABLE} (date, customer_id, city, category, product, unit_price, quantity, sales_amount, used_discount, discount_amount, final_sales)
                    VALUES (:date, :customer_id, :city, :category, :product, :unit_price, :quantity, :sales_amount, :used_discount, :discount_amount, :final_sales)
                """
                ),
                data,
            )

        upsert_query = text(
            f"""
            INSERT INTO coffee_beans_sales (date, customer_id, city, category, product, unit_price, quantity, sales_amount, used_discount, discount_amount, final_sales)
            SELECT date, customer_id, city, category, product, unit_price, quantity, sales_amount, used_discount, discount_amount, final_sales FROM {TEMP_TABLE}
        """
        )
        connection.execute(upsert_query)

        trans.commit()
        print("Operação concluída com sucesso!")

except SQLAlchemyError as e:
    print(f"Erro na operação: {e}")

finally:
    engine.dispose()

# %%
print(coffee_sales_df)
