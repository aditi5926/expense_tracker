# 💰 Expense Tracker with AI-Powered Category Suggestions

A **Streamlit-based expense tracker** that allows users to manage personal or work-related expenses with **AI-assisted category suggestions** using Google Gemini. Users can add, edit, delete, filter, and visualize expenses through a simple and intuitive interface.


---

## 🚀 Features

| Feature | Description |
|----------|--------------|
| 🤖 **AI Category Suggestion** | Uses **Google Gemini API** to automatically predict the category of an expense based on its description. |
| 🧾 **CRUD Operations** | Add, view, edit, and delete expenses easily using an interactive Streamlit UI. |
| 📊 **Expense Summary & Visualization** | View total expenditure and bar charts showing spending by category. |
| 🔍 **Category Filtering** | Quickly filter expenses by category such as Food, Travel, Supplies, or Others. |
| 📑 **Pagination Support** | Expenses are neatly paginated for easy navigation and faster loading. |
| 🔐 **User Authentication** *(optional)* | Securely log in or sign up to manage your personal expense data. |
| 💬 **AI Fallback Mode** | If the Gemini API fails, a local placeholder AI suggests categories based on keywords. |
| 💾 **SQLite Database** | Stores all expenses locally in a lightweight SQLite database. |
| 🧠 **Modular Code Design** | Clear separation of app logic (`main.py`), database (`db.py`), and AI (`ai_utils.py`). |
| ☁️ **Deployable on Streamlit Cloud** | Easily host your app directly via GitHub using Streamlit Community Cloud. |

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



