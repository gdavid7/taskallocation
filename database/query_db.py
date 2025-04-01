import mysql.connector
import os
from dotenv import load_dotenv
import json
from typing import Dict, List, Any
from datetime import datetime

import connect_to_db
# groups our issues by the user, which is a dictionary. this is important for our 80_20_rule.py 
# excules null users, therefore orgranized
def get_issues_grouped_by_user(cursor, batch_size=5000) -> Dict[str, List[Dict[str, Any]]]:
    """
    Fetch issues from database and group them by creator ID.
    
    Args:
        cursor: Database cursor object
        batch_size: Number of rows to fetch at once
        
    Returns:
        Dictionary with creator IDs as keys and lists of issue dictionaries as values
    """
    print("Starting query...")
    
    try:
        cursor.execute("""
            SELECT
                Creator_ID, ID, Issue_Key, Title, Description, Description_Code
            FROM Issue
            WHERE Issue_Key IS NOT NULL
            ORDER BY Creator_ID;
        """)
        
        print("Query executed, processing results...")

        issues_by_user = {}
        batch_count = 0
        total_rows = 0

        while True:
            # Process in reasonably sized batches
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break

            batch_count += 1
            total_rows += len(batch)
            
            if batch_count % 10 == 0:
                print(f"Processed {total_rows} rows...")

            for row in batch:
                creator_id = row['Creator_ID']
                if creator_id is None:
                    print("Creator ID is none")
                    continue
                else:
                    print("creator ID is not none: ")
                    print(creator_id)
            
                        
                issue = {
                    'id': row['ID'],
                    'issue_key': row['Issue_Key'],
                    'title': row['Title'],
                    'description': row['Description'],
                    'description_code': row['Description_Code']
                }
                # Use dict.setdefault for cleaner initialization
                issues_by_user.setdefault(creator_id, []).append(issue)

        print(f"Completed processing {total_rows} rows for {len(issues_by_user)} unique creators")
        return issues_by_user
    
    except Exception as e:
        print(f"Error in get_issues_grouped_by_user: {e}")
        # Consume any remaining results to avoid "Unread result found" error
        if cursor.with_rows:
            cursor.fetchall()
        raise

# function application:
# allows us to save all the data into a json file, this is our method of creating static information.
# without this, we would need to continuously run through the database and convert the data into dictionary form, which takes
# a long period of time which is NOT useful at all. Since we are always using the same data no matter what, it is smarter to save
# this data as a json file so we can use it instantly.
def save_to_json_file(data: Dict, filename: str = "issues_export.json", output_dir: str = "data_exports") -> str:
    """
    Save dictionary data to a JSON file, overwriting any existing file.
    Maintains a log of all exports.
    
    Args:
        data: Dictionary data to save
        filename: Output filename (default is issues_export.json)
        output_dir: Directory to save the file (will be created if it doesn't exist)
        
    Returns:
        Path to the saved JSON file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Ensure filename has .json extension
    if not filename.endswith('.json'):
        filename += '.json'
        
    # Create full file path
    file_path = os.path.join(output_dir, filename)
    
    # Get current timestamp for logging
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Write data to JSON file with pretty formatting, overwriting any existing file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Log this export
    log_file = os.path.join(output_dir, "export_log.txt")
    
    log_entry = f"[{timestamp}] Exported {len(data)} creator records to {filename}"
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
        log_entry += f" (file size: {file_size:.2f} MB)"
    
    # Total number of issues
    total_issues = sum(len(issues) for issues in data.values())
    log_entry += f" - Total issues: {total_issues}\n"
    
    # Append to log file
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"Data successfully saved to {file_path}")
    print(f"Export logged to {log_file}")
    
    return file_path





#Previous code that is now modified as seen above.
#Saving for future reference if necessary
'''
def return_unique_ids(cursor):
    """Fetch unique issue IDs where Issue_Key is not NULL."""
    cursor.execute("SELECT DISTINCT ID FROM Issue WHERE Issue_Key IS NOT NULL LIMIT 1000;")
    return [row["ID"] for row in cursor.fetchall()]

def row_based_on_id(cursor, user_id):
    """Fetch issue rows based on a given ID."""
    cursor.execute("SELECT * FROM Issue WHERE ID = %s", (user_id,))
    return cursor.fetchall()

def get_issues_dict():
    """Fetch all issues grouped by unique IDs."""
    conn, cursor = connect_to_db()
    if not conn or not cursor:
        print("Failed to connect to database.")
        return {}

    try:
        issues_dict = {}
        unique_ids = return_unique_ids(cursor)
        for user_id in unique_ids:
            issues_dict[user_id] = row_based_on_id(cursor, user_id)
        return issues_dict
    finally:
        cursor.close()
        conn.close()
        print("Connection closed.")

# Call get_issues_dict() to verify functionality
issues_dict = get_issues_dict()
print(issues_dict)
'''