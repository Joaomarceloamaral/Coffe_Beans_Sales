SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

CREATE TABLE customers 
( 
    customer_id SERIAL PRIMARY KEY,  
    city VARCHAR(20) NOT NULL
);

CREATE TABLE products 
( 
    product_id SERIAL PRIMARY KEY,
    category VARCHAR(25) NOT NULL,  
    product_name VARCHAR(25) NOT NULL,    
    unit_price NUMERIC(10,2) NOT NULL  
); 

CREATE TABLE sales 
( 
    sale_id SERIAL PRIMARY KEY,  
    date DATE NOT NULL,  
    quantity INT NOT NULL,  
    sales_amount NUMERIC(10,2) NOT NULL,  
    used_discount BOOLEAN NOT NULL,  
    discount_amount NUMERIC(10,2) NOT NULL,  
    final_sales NUMERIC(10,2) NOT NULL,  
    customer_id INT NOT NULL,  
    product_id INT NOT NULL  
);

ALTER TABLE sales ADD FOREIGN KEY(customer_id) REFERENCES customers (customer_id);
ALTER TABLE sales ADD FOREIGN KEY(product_id) REFERENCES products (product_id);


DROP TABLE customers;

DROP TABLE products;

DROP TABLE sales;

SELECT * FROM customers;

SELECT * FROM products;

-- ON CONFLICT (customer_id) 
--             DO UPDATE SET
--                 city = EXCLUDED.city