import json
import numpy as np

def load_data(file):
    # Load the JSON file
    with open(file, 'r') as f:
        data = json.load(f)
    
    # Convert lists back to numpy arrays for each user
    for key, value in data.items():
        for e in value:
            e['embed'] = np.array(e['embed'])
    return data
