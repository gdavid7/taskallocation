import mysql.connector
import os
from dotenv import load_dotenv
import json
from typing import Dict, List, Any
from datetime import datetime
from query_db import get_issues_grouped_by_user, save_to_json_file

def connect_to_db(): 
    """Establish and return a database connection and cursor."""
    load_dotenv()
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            connect_timeout=10
        )
        cursor = conn.cursor(dictionary=True)  # Returns results as dictionaries
        print("Connected to DB successfully")
        # Here you would execute your queries
        # # Fetch and group issues
        issues_data = get_issues_grouped_by_user(cursor)
        
        # # Save to JSON file
        json_path = save_to_json_file(issues_data)          # creates out json path

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None
    finally:
        # Close connections when done
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
        print("Connection resources released")
    return


#test if connection works
connect_to_db()