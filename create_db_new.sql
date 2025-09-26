-- Create tables
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS invoice_lines CASCADE;
DROP TABLE IF EXISTS invoices CASCADE;
DROP TABLE IF EXISTS purchase_lines CASCADE;
DROP TABLE IF EXISTS purchases CASCADE;
DROP TABLE IF EXISTS services CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) UNIQUE NOT NULL,
    permissions TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    role_id INTEGER REFERENCES roles(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    address TEXT,
    gst_number VARCHAR(15),
    created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Create vendors table
CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    gst_number VARCHAR(15),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    registration_number VARCHAR(20) NOT NULL,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER,
    created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    size VARCHAR(50),
    brand VARCHAR(50),
    pattern VARCHAR(50),
    selling_price DECIMAL(10, 2) NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    stock_qty INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 0,
    gst_rate DECIMAL(5, 2) NOT NULL DEFAULT 0,
    category VARCHAR(50),
    created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    gst_rate DECIMAL(5, 2) NOT NULL DEFAULT 0,
    duration INTEGER,
    category VARCHAR(50),
    created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Insert initial roles
INSERT INTO roles (id, name, permissions) VALUES 
(1, 'Admin', '{admin_access,create_invoice,create_purchase}'),
(2, 'Staff', '{create_invoice}');
SELECT setval('roles_id_seq', 2, true);

-- Insert admin user with password 'admin123'
INSERT INTO users (id, name, email, password_hash, is_active, role_id)
VALUES (1, 'Admin', 'admin@example.com', 'scrypt:32768:8:1$bFc3NgDNgOL76Qep$ce5468ae20654af99a1eb910b828c4cb4670cd012030d45c78bd48bf6ee07352ed626b113fe352da242cb3477a29d8db4a6b93fc2d398eabbb4fa6dd9d4aaea7', true, 1);
SELECT setval('users_id_seq', 1, true);

-- Insert test customers
INSERT INTO customers (id, name, mobile, email, address, gst_number, created_by_id)
VALUES 
(1, 'John Doe', '9876543210', 'john@example.com', '123 Main St', '33AABCT1234A1Z5', 1),
(2, 'Jane Smith', '9876543211', 'jane@example.com', '456 Oak St', NULL, 1);
SELECT setval('customers_id_seq', 2, true);

-- Insert vehicles
INSERT INTO vehicles (id, customer_id, registration_number, make, model, year, created_by_id)
VALUES 
(1, 1, 'TN01AB1234', 'Toyota', 'Innova', 2020, 1),
(2, 2, 'TN02CD5678', 'Honda', 'City', 2021, 1);
SELECT setval('vehicles_id_seq', 2, true);

-- Insert items
INSERT INTO items (id, code, name, description, size, brand, pattern, selling_price, purchase_price, stock_qty, reorder_level, gst_rate, category, created_by_id)
VALUES 
(1, 'MRF001', 'MRF ZVTS', '185/65 R15 88H Tubeless', '185/65 R15', 'MRF', 'ZVTS', 4500.00, 3800.00, 10, 5, 18.0, 'tyre', 1),
(2, 'BS001', 'Bridgestone B290', '195/55 R16 87V Tubeless', '195/55 R16', 'Bridgestone', 'B290', 5500.00, 4700.00, 8, 4, 18.0, 'tyre', 1);
SELECT setval('items_id_seq', 2, true);

-- Insert services
INSERT INTO services (id, code, name, description, price, gst_rate, duration, category, created_by_id)
VALUES 
(1, 'WA001', 'Wheel Alignment', '4-wheel computerized alignment', 800.00, 18.0, 45, 'alignment', 1),
(2, 'WB001', 'Wheel Balancing', 'Per wheel balancing with weights', 200.00, 18.0, 30, 'balancing', 1),
(3, 'TF001', 'Tire Fitting', 'Per tire removal and fitting', 100.00, 18.0, 15, 'fitting', 1);
SELECT setval('services_id_seq', 3, true);

-- Create invoices table
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INTEGER REFERENCES customers(id) NOT NULL,
    vehicle_id INTEGER REFERENCES vehicles(id),
    date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    subtotal DECIMAL(10, 2) DEFAULT 0,
    discount DECIMAL(10, 2) DEFAULT 0,
    total_tax DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) DEFAULT 0,
    round_off DECIMAL(2, 2) DEFAULT 0,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Create invoice_lines table
CREATE TABLE invoice_lines (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) NOT NULL,
    item_id INTEGER REFERENCES items(id),
    service_id INTEGER REFERENCES services(id),
    description VARCHAR(255),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0,
    tax_rate DECIMAL(4, 2),
    tax_amount DECIMAL(10, 2),
    subtotal DECIMAL(10, 2),
    total DECIMAL(10, 2),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Create payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER REFERENCES invoices(id) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL,
    payment_method VARCHAR(20),
    reference VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Create purchases table
CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    number VARCHAR(20) UNIQUE NOT NULL,
    vendor_id INTEGER REFERENCES vendors(id) NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    vendor_bill_number VARCHAR(50),
    vendor_bill_date DATE,
    subtotal DECIMAL(10, 2) DEFAULT 0,
    total_tax DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) DEFAULT 0,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    created_by_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Create purchase_lines table
CREATE TABLE purchase_lines (
    id SERIAL PRIMARY KEY,
    purchase_id INTEGER REFERENCES purchases(id) NOT NULL,
    item_id INTEGER REFERENCES items(id) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    tax_rate DECIMAL(4, 2),
    tax_amount DECIMAL(10, 2),
    subtotal DECIMAL(10, 2),
    total DECIMAL(10, 2),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Create stock_moves table
CREATE TABLE stock_moves (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES items(id) NOT NULL,
    quantity INTEGER NOT NULL,
    reference VARCHAR(50),
    reference_type VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);