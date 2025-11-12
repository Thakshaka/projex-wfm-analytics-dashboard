"""
Database connection utilities
"""
import mysql.connector
from mysql.connector import Error
from core.config import settings

def get_db_connection():
    """Get a MySQL database connection"""
    try:
        return mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            port=settings.DB_PORT
        )
    except Error as e:
        print(f"DB connection error: {e}")
        return None

def get_db_cursor(conn):
    """Get a dictionary cursor from connection"""
    if conn:
        return conn.cursor(dictionary=True)
    return None
