import sqlite3

DB_FILE = "customers.db"

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the customers table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            address TEXT,
            phone TEXT,
            length REAL,
            waist REAL,
            hip_height REAL,
            round_hip REAL,
            thigh REAL,
            ankle REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_customer(name, address, phone, length, waist, hip_height, round_hip, thigh, ankle):
    """Adds a new customer to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO customers (name, address, phone, length, waist, hip_height, round_hip, thigh, ankle)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, address, phone, length, waist, hip_height, round_hip, thigh, ankle))
        conn.commit()
        print(f"✅ Saved customer: {name}")
    except sqlite3.IntegrityError:
        print(f"Error: Customer with name '{name}' already exists.")
    finally:
        conn.close()

def get_all_customers():
    """Retrieves all customers from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_customer_by_name(name):
    """Retrieves a single customer by their name."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row
