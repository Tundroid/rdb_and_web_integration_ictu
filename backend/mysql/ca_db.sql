CREATE DATABASE ca_db;

USE ca_db;

CREATE TABLE CarModel (
    brand VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (brand, name)
);

CREATE TABLE Car (
    serial_number VARCHAR(50) NOT NULL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    color VARCHAR(50),
    tag_price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (brand, model_name) REFERENCES CarModel(brand, name) ON DELETE CASCADE
);

CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE Store (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE Seller (
    seller_id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    store_id INT NOT NULL,
    FOREIGN KEY (store_id) REFERENCES Store(store_id) ON DELETE CASCADE
);

CREATE TABLE Sale (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    serial_number VARCHAR(50) NOT NULL,
    customer_id INT NOT NULL,
    seller_id INT NOT NULL,
    store_id INT NOT NULL,
    purchase_price DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (serial_number) REFERENCES Car(serial_number) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (seller_id) REFERENCES Seller(seller_id) ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES Store(store_id) ON DELETE CASCADE
);

CREATE TABLE CarStorage (
    serial_number VARCHAR(50) NOT NULL,
    store_id INT NOT NULL,
    arrival_date DATE NOT NULL,
    departure_date DATE NOT NULL,
    PRIMARY KEY (serial_number, store_id, arrival_date),
    FOREIGN KEY (serial_number) REFERENCES Car(serial_number) ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES Store(store_id) ON DELETE CASCADE
);

CREATE TABLE Transfer (
    serial_number VARCHAR(50) NOT NULL,
    from_store INT NOT NULL,
    to_store INT NOT NULL,
    transfer_date DATE NOT NULL,
    PRIMARY KEY (serial_number, from_store, to_store, transfer_date),
    FOREIGN KEY (serial_number) REFERENCES Car(serial_number) ON DELETE CASCADE,
    FOREIGN KEY (from_store) REFERENCES Store(store_id) ON DELETE CASCADE,
    FOREIGN KEY (to_store) REFERENCES Store(store_id) ON DELETE CASCADE
);
