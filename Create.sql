CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id VARCHAR(6) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    pos_id VARCHAR(100),
    active BIT DEFAULT 1
);

CREATE TABLE sales (
    sale_id INT IDENTITY(1,1) PRIMARY KEY,
    distributor VARCHAR(25),
    product_category VARCHAR(10),
    amount DECIMAL(10,2),
    credit_month INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    part_number VARCHAR(255),
    qty INT,
    credit_year INT NOT NULL,
    acct_num VARCHAR(9),
    pay_structure VARCHAR(25) NOT NULL,
    customer_name VARCHAR(255)

    FOREIGN KEY (distributor) REFERENCES distributors(distributor),
    FOREIGN KEY (id) REFERENCES users(full_name),
);

CREATE TABLE distributors(
    id INT IDENTITY (1,1) PRIMARY KEY,
    distributor VARCHAR(50),
    group_name VARCHAR(100)
    )
;

