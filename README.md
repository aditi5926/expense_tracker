# 💰 Expense Tracker with AI-Powered Category Suggestions

A **Streamlit-based expense tracker** that allows users to manage personal or work-related expenses with **AI-assisted category suggestions** using Google Gemini. Users can add, edit, delete, filter, and visualize expenses through a simple and intuitive interface.

---

## **Features**

### ✅ User Authentication
- Secure **login and registration** system
- Passwords stored in **SQLite database**

### ✅ Expense Management (CRUD)
- **Create, Read, Update, Delete** expenses
- Fields include:
  - Description (text)
  - Category (AI-suggested)
  - Reimbursable (boolean)
  - Quantity & Unit Price
  - Total (calculated)
  
### ✅ AI Integration
- Uses **Google Gemini API** to suggest categories automatically based on expense description.
- Fallback logic ensures a default category is always set.

### ✅ Data Filtering & Pagination
- Filter expenses by category
- Pagination support (5 items per page)
- Optional sorting and search

### ✅ Data Visualization
- Summarizes total expenses
- Graphs by category using **Altair**

### ✅ Additional Features
- Editable expenses
- Deletable expenses
- Logout functionality

---

## **Tech Stack**
- **Frontend & App**: Streamlit  
- **Database**: SQLite  
- **AI**: Google Gemini Generative API  
- **Data Visualization**: Altair  
- **Deployment**: Streamlit Community Cloud / Render / Vercel  

---

## **Installation (Local Development)**

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/expense_tracker.git
cd expense_tracker
```

2. **Create a virtual environment**

Windows (PowerShell)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
   
```bash
pip install -r requirements.txt
```

4. **Run the App**

```bash
streamlit run main.py
```


## Usage

### Register/Login
- Create a new account or login.

### Add Expenses
- Enter description, quantity, price, and reimbursable status.
- AI will suggest a category; you can accept or change it.

### View Expenses
- Filter by category.
- Navigate pages using pagination.

### Edit/Delete Expenses
- Select an expense and modify or delete it.

### View Summary & Graph
- See total spent and bar chart of expenses by category.


---

## AI Integration

- **File**: `ai_utils.py`
- Uses **Google Gemini API** to suggest a category based on the expense description.
- Includes **fallback placeholder AI** if the API fails.
- Example categories: `Food`, `Travel`, `Supplies`, `Other`.



