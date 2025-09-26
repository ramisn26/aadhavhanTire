-- Create tables
DROP TABLE IF     created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),ISTS service CASCADE;
DROP TABLE IF EXISTS item CASCADE;
DROP TABLE IF EXISTS vehicle CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS role CASCADE;

CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) UNIQUE NOT NULL,
    permissions TEXT[] NOT NULL DEFAULT '{}'
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    role_id INTEGER REFERENCES role(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    address TEXT,
    gst_number VARCHAR(15),
    created_by_id INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE vehicle (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customer(id),
    registration_number VARCHAR(20) NOT NULL,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER,
    created_by_id INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE item (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    size VARCHAR(50),
    selling_price DECIMAL(10, 2) NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    stock_qty INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 0,
    gst_rate DECIMAL(5, 2) NOT NULL DEFAULT 0,
    created_by_id INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE service (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    gst_rate DECIMAL(5, 2) NOT NULL DEFAULT 0,
    created_by_id INTEGER REFERENCES "user"(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Insert initial roles
INSERT INTO role (id, name, permissions) VALUES 
(1, 'Admin', '{admin_access,create_invoice,create_purchase}'),
(2, 'Staff', '{create_invoice}');
SELECT setval('role_id_seq', 2, true);

-- Insert admin user with password 'admin123'
INSERT INTO users (id, name, email, password_hash, is_active, role_id)
VALUES (1, 'Admin', 'admin@example.com', 'pbkdf2:sha256:600000$8qXpzPaO9dMUDsO4$5e97903882a8e45bd291cd427dcd343cd907a023c67733e793130b0d192e2040', true, 1);
SELECT setval('user_id_seq', 1, true);

-- Insert test customers
INSERT INTO customer (id, name, mobile, email, address, gst_number, created_by_id)
VALUES 
(1, 'John Doe', '9876543210', 'john@example.com', '123 Main St', '33AABCT1234A1Z5', 1),
(2, 'Jane Smith', '9876543211', 'jane@example.com', '456 Oak St', NULL, 1);
SELECT setval('customer_id_seq', 2, true);

-- Insert vehicles
INSERT INTO vehicle (id, customer_id, registration_number, make, model, year, created_by_id)
VALUES 
(1, 1, 'TN01AB1234', 'Toyota', 'Innova', 2020, 1),
(2, 2, 'TN02CD5678', 'Honda', 'City', 2021, 1);
SELECT setval('vehicle_id_seq', 2, true);

-- Insert items
INSERT INTO item (id, name, description, size, selling_price, purchase_price, stock_qty, reorder_level, gst_rate, created_by_id)
VALUES 
(1, 'MRF ZVTS', '185/65 R15 88H Tubeless', '185/65 R15', 4500.00, 3800.00, 10, 5, 18.0, 1),
(2, 'Bridgestone B290', '195/55 R16 87V Tubeless', '195/55 R16', 5500.00, 4700.00, 8, 4, 18.0, 1);
SELECT setval('item_id_seq', 2, true);

-- Insert services
INSERT INTO service (id, name, description, price, gst_rate, created_by_id)
VALUES 
(1, 'Wheel Alignment', '4-wheel computerized alignment', 800.00, 18.0, 1),
(2, 'Wheel Balancing', 'Per wheel balancing with weights', 200.00, 18.0, 1),
(3, 'Tire Fitting', 'Per tire removal and fitting', 100.00, 18.0, 1);
SELECT setval('service_id_seq', 3, true);