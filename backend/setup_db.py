#!/usr/bin/env python3
"""
Database setup script for BookHub project
"""

import mysql.connector
from mysql.connector import Error

def create_database():
    """Create the library database if it doesn't exist"""
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS library")
            print("Database 'library' created successfully or already exists!")
            
            cursor.close()
            connection.close()
            print("MySQL connection closed.")
            
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database() 