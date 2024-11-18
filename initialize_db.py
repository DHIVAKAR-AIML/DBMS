import sqlite3

def initialize_db():
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()

        # Create Customers table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT UNIQUE,
            address TEXT
        )''')

        # Create Medicines table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Medicines (
            medicine_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manufacturer TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0
        )''')

        # Create Sales table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Sales (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            sale_date DATE NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (medicine_id) REFERENCES Medicines(medicine_id)
        )''')

        # Create Pharmacists table
        cursor.execute('''CREATE TABLE IF NOT EXISTS Pharmacists (
            pharmacist_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            shift TEXT NOT NULL
        )''')

        conn.commit()
        print("Database initialized successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_db()
