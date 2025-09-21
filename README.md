# 🛍️ AI-Powered Shop Manager

A desktop-based **Shop Management System** built with **Tkinter/CustomTkinter** for GUI, **MySQL** for database storage, and **Machine Learning** for intelligent sales and product insights.  

This project empowers shop owners to manage inventory, billing, and customer records while leveraging **AI for sales forecasting and product categorization**.

---

## 🚀 Features
- 🖥️ **Desktop App Interface** – clean GUI with CustomTkinter.  
- 📦 **Inventory Management** – add, update, and delete products.  
- 💳 **Billing System** – generate and record sales bills.  
- 👥 **Customer Records** – maintain buyer details for future reference.  
- 📊 **Sales Forecasting** – Random Forest Regressor predicts future sales trends.  
- 🏷️ **Product Categorization** – Random Forest Classifier auto-suggests categories for new products.  
- 🗄️ **Database Integration** – robust storage powered by MySQL.
- 🗄️ **Output** – Generate Receipts.  

---

## 🛠️ Tech Stack
**GUI Framework:** Tkinter, CustomTkinter  
**Database:** MySQL  
**Machine Learning:** scikit-learn (Random Forest Regressor & Classifier)  
**Language:** Python 3  

---

## ⚡ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Stranger-S8/AI-Powered-Shop-Manager.git
   cd AI-Shop-Manager
2. **Create and activate virtual environment**
    python -m venv venv
    venv\Scripts\activate     # On Windows
    source venv/bin/activate  # On Mac/Linux
3.  **Install dependencies**
    pip install -r requirements.txt
    Setup MySQL Database

4.  **Create a new MySQL database (e.g., shop_manager)**.

    Import the provided SQL schema from database/schema.sql.
    Update your MySQL credentials in database/config.py.

5. **Run the application**

    python main.py

