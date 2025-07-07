import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",         
        user="Library_admin",     
        password="Password123", 
        database="library_db"
    )
