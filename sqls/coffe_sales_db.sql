SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

-- Tabela de Clientes
CREATE TABLE customers (
	id SERIAL PRIMARY KEY,
    customer_id INT,
    city VARCHAR(255)
);

-- Tabela de Produtos
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    product VARCHAR(255),
    unit_price NUMERIC(10, 2)
);

DROP TABLE customers;

SELECT * FROM customers;

-- ON CONFLICT (customer_id) 
--             DO UPDATE SET
--                 city = EXCLUDED.city