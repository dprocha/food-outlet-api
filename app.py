import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Environment variables
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Configure logging
log_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
log_file = "app.log"

# File handler
#file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=10)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(log_formatter)

# Stream handler (console)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(log_formatter)

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info(f"Connecting to SQL Server at {DATABASE_HOST}:{DATABASE_PORT}...")

# SQLAlchemy connection setup
engine = create_engine(
    f"mssql+pyodbc://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
)
Session = sessionmaker(bind=engine)

@app.errorhandler(Exception)
def handle_exception(e):
    """Global error handler."""
    logger.error(f"An error occurred: {e}")
    return jsonify({"error": str(e)}), 500

@app.route('/restaurants/<int:restaurant_id>/sales', methods=['GET'])
def get_sales(restaurant_id):
    """Fetch total sales for a restaurant."""
    if restaurant_id <= 0:
        logger.warning(f"Invalid restaurant ID: {restaurant_id}")
        return jsonify({'error': 'Invalid restaurant ID'}), 400

    session = Session()
    try:
        query = text("""
            SELECT SUM(OrderAmount) AS TotalSales 
            FROM Orders 
            WHERE RestaurantID = :restaurant_id
        """)
        result = session.execute(query, {'restaurant_id': restaurant_id}).fetchone()
        total_sales = result[0] if result[0] is not None else 0
        logger.info(f"Total sales for restaurant {restaurant_id}: {total_sales}")
        return jsonify({'restaurantID': restaurant_id, 'totalSales': total_sales})
    except Exception as e:
        logger.error(f"Error fetching sales for restaurant {restaurant_id}: {e}")
        return jsonify({'error': 'Failed to retrieve sales data'}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
