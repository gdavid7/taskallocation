from dotenv import load_dotenv
from typing import Dict, List, Any
from datetime import datetime

def get_issues_grouped_by_user(cursor, batch_size=5000) -> Dict[str, List[Dict[str, Any]]]:
    """
    Fetch issues from TAWOS and group them by creator ID.
    
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
                Creator_ID, ID, Issue_Key, Title, Description, Description_Code, Project_ID
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
                    continue
                issue = {
                    'id': row['ID'],
                    'issue_key': row['Issue_Key'],
                    'title': row['Title'],
                    'description': row['Description'],
                    'description_code': row['Description_Code'],
                    'project_id':row['Project_ID']
                }

                # CONVERT THE ISSUE INTO AN NLP EMBED (NEW METHOD)
                # INSERT CODE FOR THIS HERE -> issue to embed. Sytax depends on whatever dustin wrote

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

