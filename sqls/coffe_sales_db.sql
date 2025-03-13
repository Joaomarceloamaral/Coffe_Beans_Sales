SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

-- Tabela de Clientes
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    city VARCHAR(255)
);

-- Tabela de Produtos
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    product VARCHAR(255),
    unit_price NUMERIC(10, 2)
);
