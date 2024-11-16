-- create database NammaKadai;
-- use NammaKadai;

create table CompanyDetails(
	num_id int auto_increment unique not null,
	company_id varchar(100) unique primary key not null,
    company_name varchar(50) not null,
    email_id varchar(100) not null unique,
    password_hash varchar(255) not null,
	access_code varchar(10) unique not null
);

select * from CompanyDetails;

-- drop table Item;

-- truncate table CompanyDetails;

create table Item(
	item_id int auto_increment not null primary key,
    item_name VARCHAR(100) NOT NULL unique,
    company_id VARCHAR(100) NOT NULL,
	remaining_quantity int not null,
    rate int not null,
    FOREIGN KEY (company_id) REFERENCES CompanyDetails(company_id)  
);

create table Purchase(
	purchase_id int auto_increment not null primary key,
    purchase_item_name varchar(100) not null,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity int not null,
    rate decimal(10, 2) not null,
    amount decimal(10, 2) as (quantity*rate),
    company_id varchar(100) not null,
    foreign key(company_id) REFERENCES CompanyDetails(company_id)
);

create table Sale(
	sale_id int auto_increment not null primary key,
    sale_item_name varchar(100) not null,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity int not null,
    rate decimal(10, 2) not null,
    amount decimal(10, 2) as (quantity*rate),
    company_id varchar(100) not null,
    foreign key(company_id) REFERENCES CompanyDetails(company_id)
);

create table Balance(
	balance decimal(10,2) not null,
	company_id VARCHAR(100) NOT NULL,
    transaction_type varchar(10) not null,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	foreign key(company_id) REFERENCES CompanyDetails(company_id)
);

select * from Balance;
select * from Sale;
select * from Purchase;
select * from Item;
select * from CompanyDetails;

use NammaKadai;

-- truncate table Balance;
-- truncate table Sale;
-- truncate table Purchase;
-- truncate table Item;
-- truncate table CompanyDetails;
ALTER TABLE Item ADD COLUMN is_active BOOLEAN DEFAULT 1;

select balance from Item where company_id="NK1595" and item_name="pen";