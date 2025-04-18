import json
import numpy as np

def load_data():
    # Load the JSON file
    with open('data_exports/issues_export.json', 'r') as f:
        data = json.load(f)
    
    # Convert lists back to numpy arrays for each user
    for user_id in data:
        for i in range(len(data[user_id])):
            data[user_id][i] = np.array(data[user_id][i])
    
    return data
