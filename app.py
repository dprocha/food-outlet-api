import pyodbc
import os
from flask import Flask, jsonify


app = Flask(__name__)

# Environment variables
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "1433")
DATABASE_NAME = os.getenv("DATABASE_NAME", "FoodOutlet")
DATABASE_USER = os.getenv("DATABASE_USER", "sa")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "Datadog2024!")

print(f"Connecting to SQL Server at {DATABASE_HOST}:{DATABASE_PORT}...")
print(f"Database: {DATABASE_NAME}")
print(f"User: {DATABASE_USER}")
print(f"Password: {DATABASE_PASSWORD}")

# Connect to SQL Server
def get_db_connection():
    conn_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DATABASE_HOST},{DATABASE_PORT};"
        f"DATABASE={DATABASE_NAME};"
        f"UID={DATABASE_USER};"
        f"PWD={DATABASE_PASSWORD};"
    )
    return pyodbc.connect(conn_string)

@app.route('/restaurants/<int:restaurant_id>/sales', methods=['GET'])
def get_sales(restaurant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(OrderAmount) AS TotalSales 
        FROM Orders 
        WHERE RestaurantID = ?""", (restaurant_id,))
    result = cursor.fetchone()
    return jsonify({'restaurantID': restaurant_id, 'totalSales': result[0]})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)