import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",         # Or your DB host
        user="Library_admin",     # Replace with your MySQL username
        password="Password123", # Replace with your password
        database="library_db"
    )
