import numpy as np
import math
from typing import List


def calculate_ndcg(predicted_ranking: List[str], actual_assigned_user: str) -> float:
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
    
    # Calculate DCG
    # Since only the actual user has relevance=1 and all others are 0,
    # DCG is simply 1/log2(rank+1)
    dcg = 1 / math.log2(rank + 1)
    
    # Ideal DCG would be if the actual user was ranked first
    # IDCG = 1/log2(1+1) = 1
    idcg = 1.0
    
    # nDCG = DCG/IDCG
    ndcg = dcg / idcg
    
    return ndcg


# Example usage
def run(sprint_ranking:list, sprint_actual_user:str):
    '''
    Sample data:
    sprint1_ranking = ["user3", "user1", "user5", "user2", "user4"]
    sprint1_actual_user = "user1"  # This user was ranked 2nd by model
    '''
    
    # Calculate nDCG for Sprint 1
    ndcg_score = calculate_ndcg(sprint_ranking, sprint_actual_user)
    
    # Find the rank position (1-indexed)
    rank = sprint_ranking.index(sprint_actual_user) + 1
    print(f"  Model ranking: {sprint_ranking}")
    print(f"  Actual assigned user: {sprint_actual_user}")
    print(f"  Rank position: {rank}")
    print(f"  nDCG score: {ndcg_score:.4f}")
    return ndcg_score




def sort(sprintDict:dict) -> dict:
    '''
    Sort the dictionary that is outputted from the model functions - use this before you run it
    '''

    sorted_results = {
        outer_k: dict(sorted(inner_d.items(), key=lambda item: item[1], reverse=True))
        for outer_k, inner_d in sprintDict.items()
    }

    return sorted_results
