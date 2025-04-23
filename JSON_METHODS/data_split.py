#!/usr/bin/env python3
"""
Data Splitter for AI Project Management Tool

This script splits a JSON file containing user task data into training (80%)
and testing (20%) datasets, allowing tasks from the same user to appear in both sets.
"""

import json
import random
import os
from typing import Dict, List, Any


def split_data(
    input_file_path: str = "data_exports/issues_export.json",
    train_ratio: float = 0.8,
    train_output_path: str = "data_exports/train_data.json",
    test_output_path: str = "data_exports/test_data.json",
    random_seed: int = 42
):
    """
    Split JSON data into training and testing sets, allowing tasks from 
    the same user to appear in both sets.
    
    Args:
        input_file_path: Path to the input JSON file
        train_ratio: Proportion of data to use for training (default: 0.8)
        train_output_path: Path to save the training data
        test_output_path: Path to save the testing data
        random_seed: Random seed for reproducibility
    """
    # Set random seed for reproducibility
    random.seed(random_seed)
    
    # Load the data
    print(f"Loading data from {input_file_path}...")
    with open(input_file_path, 'r') as file:
        data = json.load(file)
    
    print(f"Loaded data with {len(data)} users")
    
    # Create a list of all user-task pairs
    all_pairs = []
    for user_id, tasks in data.items():
        for task in tasks:
            all_pairs.append((user_id, task))
    
    # Count total tasks
    total_tasks = len(all_pairs)
    print(f"Total tasks: {total_tasks}")
    
    # Shuffle the pairs
    print(f"Shuffling {len(all_pairs)} user-task pairs...")
    random.shuffle(all_pairs)
    
    # Split into training and testing sets
    split_idx = int(total_tasks * train_ratio)
    train_pairs = all_pairs[:split_idx]
    test_pairs = all_pairs[split_idx:]
    
    print(f"Training set: {len(train_pairs)} tasks ({len(train_pairs)/total_tasks:.1%})")
    print(f"Testing set: {len(test_pairs)} tasks ({len(test_pairs)/total_tasks:.1%})")
    
    # Reorganize into the original format
    train_data = {}
    test_data = {}
    
    for user_id, task in train_pairs:
        if user_id not in train_data:
            train_data[user_id] = []
        train_data[user_id].append(task)
    
    for user_id, task in test_pairs:
        if user_id not in test_data:
            test_data[user_id] = []
        test_data[user_id].append(task)
    
    # Save the training and testing data with nice formatting
    with open(train_output_path, 'w') as file:
        json.dump(train_data, file, indent=2, sort_keys=True)
    
    with open(test_output_path, 'w') as file:
        json.dump(test_data, file, indent=2, sort_keys=True)
    
    print(f"Training data saved to {train_output_path}")
    print(f"Testing data saved to {test_output_path}")
    
    # Calculate overlap statistics
    train_users = set(train_data.keys())
    test_users = set(test_data.keys())
    common_users = train_users & test_users
    
    print(f"\nSummary:")
    print(f"Users in training set: {len(train_users)}")
    print(f"Users in testing set: {len(test_users)}")
    print(f"Users in both sets: {len(common_users)} ({len(common_users)/len(data):.1%} of all users)")
    
    # Show task distribution for users who appear in both sets
    if len(common_users) > 0:
        print("\nTask distribution for users in both sets:")
        for user_id in sorted(common_users):
            train_count = len(train_data[user_id])
            test_count = len(test_data[user_id])
            total_count = train_count + test_count
            print(f"  User {user_id}: {train_count} tasks in training ({train_count/total_count:.1%}), " +
                  f"{test_count} tasks in testing ({test_count/total_count:.1%})")

'''
if __name__ == "__main__":
    # Example usage
    input_file = "data_exports/issues_export.json"  # Replace with your actual file path
    
    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
    else:
        split_data(input_file)
'''
