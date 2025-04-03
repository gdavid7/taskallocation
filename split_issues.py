#create the 80 20 rules here
import json
import os
from typing import Dict, List, Any
import random

# splits the data randomly according to the 80 20 rule
# therefore we have two json files 1. testing 2. training
def split_issues_80_20(input_file: str = "data_exports/issues_export.json",
                        train_file: str = "data_exports/issues_train.json",
                        test_file: str = "data_exports/issues_test.json"):
    """
    Splits the issues dataset into 80% training and 20% testing, maintaining per-user distribution.

    Args:
        input_file: Path to the JSON file containing issues grouped by users.
        train_file: Path to save the training dataset.
        test_file: Path to save the testing dataset.
    
    Returns:
        Tuple of training and testing data dictionaries.
    """
    # Load the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        issues_by_user = json.load(f)

    train_data = {}
    test_data = {}

    for user_id, issues in issues_by_user.items():
        random.shuffle(issues)  # Shuffle issues to ensure randomness
        split_idx = int(len(issues) * 0.8)  # Determine 80% split point

        train_data[user_id] = issues[:split_idx]  # First 80% for training
        test_data[user_id] = issues[split_idx:]   # Last 20% for testing

    # Save training and testing data separately
    os.makedirs("data_exports", exist_ok=True)
    
    with open(train_file, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)
    
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)

    print(f"Training data saved to {train_file} ({len(train_data)} users)")
    print(f"Testing data saved to {test_file} ({len(test_data)} users)")

    return train_data, test_data

# Run the function
# split_issues_80_20()