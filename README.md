# AI-Powered Shop Manager

A desktop shop management system for inventory, sales, customers, billing, receipt generation, and basic sales prediction.

## Tech Stack

- Python
- Tkinter / CustomTkinter
- MySQL (via `mysql-connector-python`)
- Pandas
- Matplotlib
- scikit-learn

## Getting Started

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

## Configuration (Important)

- Database credentials should **not** be committed to GitHub.
- This repo reads the MySQL password from the environment variable `SHOPMANAGER_DB_PASSWORD` (see `database.py`).

Example (PowerShell):

```powershell
$env:SHOPMANAGER_DB_PASSWORD = "your_password_here"
python run.py
```

## GitHub Notes

Do not commit real customer data, credentials, API keys, private keys, receipts, database dumps, or other generated output.
