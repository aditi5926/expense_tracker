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
    choice = st.radio("Choose Action", ["Login", "Register"], key="auth_choice")
    username = st.text_input("Username", key="auth_username")
    password = st.text_input("Password", type="password", key="auth_password")
    if choice == "Register" and st.button("Register", key="auth_register"):
        register(username, password)
    elif choice == "Login" and st.button("Login", key="auth_login"):
        login(username, password)
    st.stop()

# ---------- DASHBOARD ----------
st.title("💰 Expense Tracker")
st.caption(f"Logged in as **{st.session_state['user'][1]}**")

# ---------- ADD NEW EXPENSE ----------
with st.expander("➕ Add New Expense", expanded=False):
    desc = st.text_input("Description", key="add_desc")
    cat = st.selectbox("Category", ["Food", "Travel", "Supplies", "Other"], key="add_category")
    reimb = st.checkbox("Reimbursable?", key="add_reimb")
    qty = st.number_input("Quantity", min_value=1.0, value=1.0, key="add_qty")
    price = st.number_input("Unit Price", min_value=0.0, value=0.0, key="add_price")
    total = qty * price
    st.write(f"**Total:** {total:.2f}")

    if st.button("Add Expense", key="add_expense_btn"):
        if desc:
            conn.execute("""
                INSERT INTO expenses (user_id, description, category, reimbursable, quantity, unit_price, total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (st.session_state['user'][0], desc, cat, int(reimb), qty, price, total))
            conn.commit()
            st.success("Expense added!")
            st.session_state['reload'] = not st.session_state.get('reload', False)  # trigger rerun
        else:
            st.warning("Description required!")

# ---------- FILTER + PAGINATION ----------
st.header("📋 Your Expenses")
category_filter = st.selectbox("Filter by Category", ["All", "Food", "Travel", "Supplies", "Other"], key="filter_cat")
page_size = 5
page = st.number_input("Page number", min_value=1, value=1, key="page_num")

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
    del_id = st.selectbox("Select ID to delete", df['id'], key="del_id")
    if st.button("Delete Selected Expense", key="del_btn"):
        conn.execute("DELETE FROM expenses WHERE id=?", (del_id,))
        conn.commit()
        st.success("Deleted successfully!")
        st.session_state['reload'] = not st.session_state.get('reload', False)  # trigger rerun

# ---------- EDIT ----------
st.subheader("✏️ Edit an Expense")
if not df.empty:
    edit_id = st.selectbox("Select Expense ID to Edit", df["id"], key="edit_id")
    
    # Load expense into session_state
    if st.button("Load Expense", key=f"load_{edit_id}"):
        expense = conn.execute("SELECT * FROM expenses WHERE id=?", (edit_id,)).fetchone()
        if expense:
            st.session_state['edit_expense'] = {
                'desc': expense[2],
                'cat': expense[3],
                'reimb': bool(expense[4]),
                'qty': float(expense[5]),
                'price': float(expense[6])
            }

    if 'edit_expense' in st.session_state:
        new_desc = st.text_input("Description", value=st.session_state['edit_expense']['desc'], key=f"desc_{edit_id}")
        new_cat = st.selectbox(
            "Category", 
            ["Food", "Travel", "Supplies", "Other"], 
            index=["Food","Travel","Supplies","Other"].index(st.session_state['edit_expense']['cat']),
            key=f"cat_{edit_id}"
        )
        new_reimb = st.checkbox("Reimbursable?", value=st.session_state['edit_expense']['reimb'], key=f"reimb_{edit_id}")
        new_qty = st.number_input("Quantity", min_value=1.0, value=st.session_state['edit_expense']['qty'], key=f"qty_{edit_id}")
        new_price = st.number_input("Unit Price", min_value=0.0, value=st.session_state['edit_expense']['price'], key=f"price_{edit_id}")
        new_total = new_qty * new_price
        st.write(f"**Total:** {new_total:.2f}")

        if st.button("Save Changes", key=f"save_{edit_id}"):
            conn.execute("""
                UPDATE expenses
                SET description=?, category=?, reimbursable=?, quantity=?, unit_price=?, total=?
                WHERE id=?
            """, (new_desc, new_cat, int(new_reimb), new_qty, new_price, new_total, edit_id))
            conn.commit()
            st.success("Expense updated successfully!")
            del st.session_state['edit_expense']
            st.session_state['reload'] = not st.session_state.get('reload', False)  # trigger rerun

# ---------- SUMMARY + GRAPH ----------
if not df.empty:
    total_spent = df['total'].sum()
    st.metric("💵 Total Spent (This Page)", f"₹{total_spent:.2f}")

    import altair as alt
    chart = alt.Chart(df).mark_bar().encode(
        x='category',
        y='sum(total)',
        color='category'
    )
    st.altair_chart(chart, use_container_width=True)

# ---------- LOGOUT ----------
if st.button("🚪 Logout", key="logout_btn"):
    st.session_state['user'] = None
    st.session_state['reload'] = not st.session_state.get('reload', False)
