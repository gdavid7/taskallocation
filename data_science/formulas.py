import numpy as np
import math
from typing import List
"""
RANKING METRICS FOR SPRINT ASSIGNMENT EVALUATION
"""

def calculate_pri(predicted_ranking: List[str], actual_assigned_user: str) -> float:
    print(predicted_ranking)
    """
    Calculate Normalized Discounted Cumulative Gain (nDCG) for a sprint assignment.
    
    This function evaluates how well the model ranked the actually assigned user.
    
    Args:
        predicted_ranking: List of users ranked by the model (from best fit to worst fit)
        actual_assigned_user: The user who was actually assigned to the sprint
        
    Returns:
        float: nDCG score between 0 and 1, where higher is better
              1.0 = perfect (model ranked the assigned user first)
              Lower scores indicate the assigned user appeared lower in the ranking
    """
    try:
        # Find the position of the actual user (0-indexed)
        position = predicted_ranking.index(actual_assigned_user)
    except ValueError:
        # If the user isn't in the predicted ranking, consider them at the end
        position = len(predicted_ranking)
    
    # Convert to 1-indexed rank for the formula
    rank = position + 1
    
    # Total number of items in the ranking
    n = len(predicted_ranking)
    
    # Calculate PRI
    # Formula: PRI = ((N - rank) / (N - 1)) * 100
    # This gives 100 for rank 1, and 0 for rank N
    if n > 1:  # Avoid division by zero
        pri = ((n - rank) / (n - 1)) * 100
    else:
        # If there's only one item, PRI is either 100 (if correct) or 0 (if incorrect)
        pri = 100.0 if rank == 1 else 0.0
    
    return pri


# Example usage
def run(sprint_ranking:list, sprint_actual_user:str):
    '''
    Sample data:
    sprint1_ranking = ["user3", "user1", "user5", "user2", "user4"]
    sprint1_actual_user = "user1"  # This user was ranked 2nd by model
    '''
    
    # Calculate nDCG for Sprint 1
    pri_score = calculate_pri(sprint_ranking, sprint_actual_user)
    
    # Find the rank position (1-indexed)
    rank = sprint_ranking.index(sprint_actual_user) + 1
    print(f"  Model ranking: {sprint_ranking}")
    print(f"  Actual assigned user: {sprint_actual_user}")
    print(f"  Rank position: {rank}")
    print(f"  nDCG score: {pri_score:.4f}")
    return pri_score




def sort(sprintDict:dict) -> dict:
    '''
    Sort the dictionary that is outputted from the model functions - use this before you run it
    '''

    sorted_results = {
        outer_k: dict(sorted(inner_d.items(), key=lambda item: item[1], reverse=True))
        for outer_k, inner_d in sprintDict.items()
    }

    return sorted_results
