SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

CREATE TABLE coffee_beans_sales 
( 
    id SERIAL PRIMARY KEY,  
	date DATE NOT NULL,
	customer_id INT NOT NULL,
    city VARCHAR(20) NOT NULL,
	category VARCHAR(25) NOT NULL,  
    product VARCHAR(25) NOT NULL,    
    unit_price NUMERIC(10,2) NOT NULL,
	quantity INT NOT NULL,
	sales_amount NUMERIC(10,2) NOT NULL,  
    used_discount BOOLEAN NOT NULL,  
    discount_amount NUMERIC(10,2) NOT NULL,  
    final_sales NUMERIC(10,2) NOT NULL
);

DROP TABLE coffee_beans_sales;

SELECT * FROM coffee_beans_sales;