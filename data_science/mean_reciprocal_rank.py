import numpy as np
import math
from typing import List
"""
RANKING METRICS FOR SPRINT ASSIGNMENT EVALUATION

This module implements different metrics for evaluating how well a model ranks users
for sprint assignments. Two key metrics are implemented:

1. Mean Reciprocal Rank (MRR):
   - A ranking metric that focuses only on the position of the first relevant item
   - Formula: MRR = 1/rank, where rank is the position of the actual assigned user
   - Range: [0, 1] where 1 is perfect (actual user ranked first)
   - Interpretation: Directly indicates the reciprocal of the rank position
     * MRR = 1.0 → user ranked 1st
     * MRR = 0.5 → user ranked 2nd
     * MRR = 0.33 → user ranked 3rd
   - Advantages:
     * Simple to calculate and interpret
     * Focuses on a single correct answer, which matches sprint assignment
     * More intuitive representation of rank position

2. Normalized Discounted Cumulative Gain (NDCG):
   - A ranking metric that considers both position and relevance of items
   - In our implementation (where only one user is relevant):
     * DCG = 1/log2(rank+1)
     * IDCG = 1.0 (ideal DCG if user was ranked first)
     * NDCG = DCG/IDCG
   - Range: [0, 1] where 1 is perfect (actual user ranked first)
   - Interpretation: Penalizes lower rankings logarithmically
   - Advantages:
     * Industry-standard metric for ranking evaluation
     * Can be extended to handle multiple relevant items with graded relevance
     * Penalizes lower rankings less harshly than MRR

For sprint assignment evaluation where there is exactly one "correct" assignment,
MRR is often more appropriate as it directly measures the rank position of the
actually assigned user.
"""

def calculate_mrr(predicted_ranking: List[str], actual_assigned_user: str) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR) for a sprint assignment.
    
    This function evaluates how well the model ranked the actually assigned user
    using the reciprocal of the rank position.
    
    Args:
        predicted_ranking: List of users ranked by the model (from best fit to worst fit)
        actual_assigned_user: The user who was actually assigned to the sprint
        
    Returns:
        float: MRR score between 0 and 1, where higher is better
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
    
    # Calculate MRR (simply 1/rank)
    mrr = 1.0 / rank
    
    return mrr


# Example usage
def run(sprint_ranking:list, sprint_actual_user:str):
    '''
    Sample data:
    sprint1_ranking = ["user3", "user1", "user5", "user2", "user4"]
    sprint1_actual_user = "user1"  # This user was ranked 2nd by model
    '''
    print(f"  Model ranking: {sprint_ranking}")
    
    # Calculate MRR for Sprint assignment
    mrr_score = calculate_mrr(sprint_ranking, sprint_actual_user)
    
    # Find the rank position (1-indexed)
    try:
        rank = sprint_ranking.index(sprint_actual_user) + 1
    except ValueError:
        rank = len(sprint_ranking) + 1
    
    print(f"  Actual assigned user: {sprint_actual_user}")
    print(f"  Rank position: {rank}")
    print(f"  MRR score: {mrr_score:.4f}")
    return mrr_score


def sort(sprintDict:dict) -> dict:
    '''
    Sort the dictionary that is outputted from the model functions - use this before you run it
    '''
    sorted_results = {
        outer_k: dict(sorted(inner_d.items(), key=lambda item: item[1], reverse=True))
        for outer_k, inner_d in sprintDict.items()
    }

    return sorted_results
