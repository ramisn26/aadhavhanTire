import psycopg2
from psycopg2.extras import execute_values
from werkzeug.security import generate_password_hash

def seed_data():
    try:
        # Connect to the database
        conn = psycopg2.connect("dbname=aadhavhantire")
        cur = conn.cursor()

        print("Creating test customers...")
        cur.execute("""
            INSERT INTO customer (name, mobile, email, address, gst_number, created_by_id)
            VALUES 
            ('John Doe', '9876543210', 'john@example.com', '123 Main St', '33AABCT1234A1Z5', 1),
            ('Jane Smith', '9876543211', 'jane@example.com', '456 Oak St', NULL, 1)
            RETURNING id;
        """)
        customer_ids = [r[0] for r in cur.fetchall()]

        print("Creating vehicles...")
        vehicles_data = [
            (customer_ids[0], 'TN01AB1234', 'Toyota', 'Innova', 2020, 1),
            (customer_ids[1], 'TN02CD5678', 'Honda', 'City', 2021, 1)
        ]
        cur.execute("""
            INSERT INTO vehicle (customer_id, registration_number, make, model, year, created_by_id)
            VALUES %s
        """, vehicles_data)

        print("Creating items...")
        items_data = [
            ('MRF ZVTS', '185/65 R15 88H Tubeless', '185/65 R15', 4500.00, 3800.00, 10, 5, 18.0, 1),
            ('Bridgestone B290', '195/55 R16 87V Tubeless', '195/55 R16', 5500.00, 4700.00, 8, 4, 18.0, 1)
        ]
        cur.execute("""
            INSERT INTO item (name, description, size, selling_price, purchase_price, stock_qty, reorder_level, gst_rate, created_by_id)
            VALUES %s
        """, items_data)

        print("Creating services...")
        services_data = [
            ('Wheel Alignment', '4-wheel computerized alignment', 800.00, 18.0, 1),
            ('Wheel Balancing', 'Per wheel balancing with weights', 200.00, 18.0, 1),
            ('Tire Fitting', 'Per tire removal and fitting', 100.00, 18.0, 1)
        ]
        cur.execute("""
            INSERT INTO service (name, description, price, gst_rate, created_by_id)
            VALUES %s
        """, services_data)

        conn.commit()
        print("Test data has been seeded successfully!")
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error seeding data: {e}")
        conn.rollback()
        cur.close()
        conn.close()
        raise

if __name__ == '__main__':
    seed_data()

if __name__ == '__main__':
    seed_data()

if __name__ == '__main__':
    seed_data()