import os
from dotenv import load_dotenv
import json
from typing import Dict, List, Any
from datetime import datetime
import numpy as np

# Add a custom encoder class for NumPy arrays
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert numpy arrays to lists
        return json.JSONEncoder.default(self, obj)


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
        json.dump(data, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
    
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
