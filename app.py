
import streamlit as st
import sqlite3

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL
                )''')
    conn.commit()
    conn.close()

# Add product
def add_product(name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()

# View all products
def view_products():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    data = c.fetchall()
    conn.close()
    return data

# Delete product by ID
def delete_product(product_id):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# Streamlit app UI
st.title("Inventory Tracker")

menu = ["Add Product", "View Inventory", "Delete Product"]
choice = st.sidebar.selectbox("Menu", menu)

init_db()

if choice == "Add Product":
    st.subheader("Add New Product")
    name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Price", min_value=0.0, step=0.1, format="%.2f")
    
    if st.button("Add"):
        if name:
            add_product(name, quantity, price)
            st.success(f"Added {name} to inventory.")
        else:
            st.error("Please enter a product name.")

elif choice == "View Inventory":
    st.subheader("Inventory List")
    products = view_products()
    if products:
        for p in products:
            st.write(f"ID: {p[0]} | Name: {p[1]} | Quantity: {p[2]} | Price: ₹{p[3]:.2f}")
    else:
        st.info("No products in inventory.")

elif choice == "Delete Product":
    st.subheader("Delete Product")
    products = view_products()
    product_ids = [str(p[0]) for p in products]
    if product_ids:
        selected_id = st.selectbox("Select Product ID to Delete", product_ids)
        if st.button("Delete"):
            delete_product(int(selected_id))
            st.success(f"Deleted product with ID {selected_id}.")
    else:
        st.info("No products to delete.")
