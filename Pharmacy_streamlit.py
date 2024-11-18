import sqlite3
from datetime import date
import streamlit as st

# Database Operations
def initialize_db():
    """Initialize the database and tables."""
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT UNIQUE,
            address TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Medicines (
            medicine_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            manufacturer TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Sales (
            sale_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER,
            sale_date DATE,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (medicine_id) REFERENCES Medicines(medicine_id)
        )''')

        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database initialization failed: {e}")
    finally:
        conn.close()

def add_customer(name, phone, address):
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Customers (name, phone, address) VALUES (?, ?, ?)', 
                       (name, phone, address))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error adding customer: {e}")
    finally:
        conn.close()

def add_medicine(name, manufacturer, price, stock):
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Medicines (name, manufacturer, price, stock) VALUES (?, ?, ?, ?)', 
                       (name, manufacturer, price, stock))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error adding medicine: {e}")
    finally:
        conn.close()

def make_sale(customer_id, medicine_id, quantity):
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        
        # Check stock availability
        cursor.execute('SELECT stock FROM Medicines WHERE medicine_id = ?', (medicine_id,))
        stock = cursor.fetchone()
        if stock is None or stock[0] < quantity:
            st.error("Insufficient stock!")
            return
        
        # Record the sale
        sale_date = date.today().strftime('%Y-%m-%d')
        cursor.execute('INSERT INTO Sales (customer_id, medicine_id, quantity, sale_date) VALUES (?, ?, ?, ?)', 
                       (customer_id, medicine_id, quantity, sale_date))
        cursor.execute('UPDATE Medicines SET stock = stock - ? WHERE medicine_id = ?', 
                       (quantity, medicine_id))
        conn.commit()
        st.success("Sale recorded successfully!")
    except sqlite3.Error as e:
        st.error(f"Error making sale: {e}")
    finally:
        conn.close()

def fetch_data(query):
    try:
        conn = sqlite3.connect('pharmacy.db')
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        st.error(f"Error fetching data: {e}")
        return []
    finally:
        conn.close()

# Initialize the database
initialize_db()

# Streamlit UI
st.title("Pharmacy Management System")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Add Customer", "Add Medicine", "Make Sale", "View Data"])

if page == "Add Customer":
    st.header("Add Customer")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    if st.button("Add Customer"):
        if name and phone and address:
            add_customer(name, phone, address)
        else:
            st.error("All fields are required.")

elif page == "Add Medicine":
    st.header("Add Medicine")
    name = st.text_input("Medicine Name")
    manufacturer = st.text_input("Manufacturer")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    stock = st.number_input("Stock", min_value=0, step=1)
    if st.button("Add Medicine"):
        if name and manufacturer and price and stock:
            add_medicine(name, manufacturer, price, stock)
        else:
            st.error("All fields are required.")

elif page == "Make Sale":
    st.header("Make Sale")
    customer_id = st.number_input("Customer ID", min_value=1, step=1)
    medicine_id = st.number_input("Medicine ID", min_value=1, step=1)
    quantity = st.number_input("Quantity", min_value=1, step=1)
    if st.button("Make Sale"):
        if customer_id and medicine_id and quantity:
            make_sale(customer_id, medicine_id, quantity)
        else:
            st.error("All fields are required.")

elif page == "View Data":
    st.header("View Data")
    data_type = st.selectbox("View", ["Customers", "Medicines", "Sales"])
    if data_type == "Customers":
        st.subheader("Customers")
        customers = fetch_data("SELECT * FROM Customers")
        for customer in customers:
            st.write(customer)
    elif data_type == "Medicines":
        st.subheader("Medicines")
        medicines = fetch_data("SELECT * FROM Medicines")
        for medicine in medicines:
            st.write(medicine)
    elif data_type == "Sales":
        st.subheader("Sales")
        sales = fetch_data("SELECT * FROM Sales")
        for sale in sales:
            st.write(sale)
