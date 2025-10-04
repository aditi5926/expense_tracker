# main.py
import streamlit as st
import pandas as pd
import sqlite3
from db import get_connection

st.set_page_config(page_title="Expense Tracker", layout="wide")

conn = get_connection()

if 'user' not in st.session_state:
    st.session_state['user'] = None

# ---------- AUTH ----------
def register(username, password):
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success("✅ Registered successfully! You can now log in.")
    except sqlite3.IntegrityError:
        st.error("❌ Username already exists!")

def login(username, password):
    cur = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    if user:
        st.session_state['user'] = user
        st.success(f"👋 Welcome {username}")
    else:
        st.error("Invalid credentials")

if not st.session_state['user']:
    st.title("🔐 Login / Register")

    choice = st.radio("Choose Action", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register" and st.button("Register"):
        register(username, password)
    elif choice == "Login" and st.button("Login"):
        login(username, password)
    st.stop()

# ---------- DASHBOARD ----------
st.title("💰 Expense Tracker")
st.caption(f"Logged in as **{st.session_state['user'][1]}**")

# ADD NEW EXPENSE
with st.expander("➕ Add New Expense", expanded=False):
    desc = st.text_input("Description")
    cat = st.selectbox("Category", ["Food", "Travel", "Supplies", "Other"])
    reimb = st.checkbox("Reimbursable?")
    qty = st.number_input("Quantity", min_value=1.0, value=1.0)
    price = st.number_input("Unit Price", min_value=0.0, value=0.0)
    total = qty * price
    st.write(f"**Total:** {total:.2f}")

    if st.button("Add Expense"):
        if desc:
            conn.execute("""
                INSERT INTO expenses (user_id, description, category, reimbursable, quantity, unit_price, total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (st.session_state['user'][0], desc, cat, int(reimb), qty, price, total))
            conn.commit()
            st.success("Expense added!")
        else:
            st.warning("Description required!")

# ---------- FILTER + PAGINATION ----------
st.header("📋 Your Expenses")

category_filter = st.selectbox("Filter by Category", ["All", "Food", "Travel", "Supplies", "Other"])
page_size = 5
page = st.number_input("Page number", min_value=1, value=1)

query = "SELECT * FROM expenses WHERE user_id=?"
params = [st.session_state['user'][0]]
if category_filter != "All":
    query += " AND category=?"
    params.append(category_filter)
query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
params += [page_size, (page - 1) * page_size]

df = pd.read_sql_query(query, conn, params=params)
if not df.empty:
    st.dataframe(df)
else:
    st.info("No expenses found.")

# ---------- DELETE ----------
if not df.empty:
    del_id = st.selectbox("Select ID to delete", df['id'])
    if st.button("Delete Selected Expense"):
        conn.execute("DELETE FROM expenses WHERE id=?", (del_id,))
        conn.commit()
        st.success("Deleted successfully!")
        st.experimental_rerun()

# ---------- SUMMARY ----------
if not df.empty:
    st.metric("💵 Total Spent (this page)", f"{df['total'].sum():.2f}")

# ---------- LOGOUT ----------
if st.button("🚪 Logout"):
    st.session_state['user'] = None
    st.experimental_rerun()
