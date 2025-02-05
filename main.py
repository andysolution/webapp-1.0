from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pyodbc
import os



# Initialize FastAPI app
app = FastAPI()

# Set up template rendering
templates = Jinja2Templates(directory="templates")

# Mount static files (JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Azure SQL Connection Details
SERVER = os.getenv("AZURE_SQL_SERVER", "andika-sql-server.database.windows.net")
DATABASE = os.getenv("AZURE_SQL_DATABASE", "andika-database")
USERNAME = os.getenv("AZURE_SQL_USERNAME", "andika-admin")
PASSWORD = os.getenv("AZURE_SQL_PASSWORD", "Mypassword73@")

# Connection String
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)

def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

@app.get("/")
def serve_homepage(request: Request):
    """Serve the homepage with input field."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/employee/{employee_number}")
def get_employee(employee_number: int):
    """Fetch employee details by employee_number."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor()
    query = """
        SELECT employee_number, name, department FROM employees WHERE employee_number = ?
    """
    cursor.execute(query, (employee_number,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"employee_number": row[0], "name": row[1], "department": row[2]}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")
    
@app.get("/employee/{employee_number}")
def get_employee(employee_number: int):
    """Fetch employee details by employee_number."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor()
    query = """
        SELECT employee_number, name, department, position, email, phone FROM employees WHERE employee_number = ?
    """
    cursor.execute(query, (employee_number,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "employee_number": row[0],
            "name": row[1],
            "department": row[2],
            "position": row[3] if row[3] else None,
            "email": row[4] if row[4] else None,
            "phone": row[5] if row[5] else None
        }
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

    


# Run the API with: uvicorn main:app --reload