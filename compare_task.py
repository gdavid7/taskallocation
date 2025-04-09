# create a function that takes in 3 formal paraemeters:
    # (model, test_task, train_task)

# maybe we can use matplotlab to plot the progression?
import json
from typing import Dict, List, Callable, Any, Tuple

Embedding = Any
IssueID = str
UserID = str

#scoring logic and skips same embed
def compute_average_similarity(model, test_embed: Embedding, training_embeds: List[Embedding]) -> float:
    total_score = 0.0
    count = 0
    for train_embed in training_embeds:
        if test_embed == train_embed:
            continue
        score = model.compare(test_embed, train_embed)
        total_score += score
        count += 1
    return total_score / count if count > 0 else 0.0

#builds and sorts user score map
def rank_users_by_similarity(model, test_embed: Embedding, issues_embed: Dict[UserID, List[Embedding]]) -> List[Tuple[UserID, float]]:
    score_map: Dict[UserID, float] = {}
    for user_id, training_embeds in issues_embed.items():
        avg_score = compute_average_similarity(model, test_embed, training_embeds)
        if avg_score > 0:
            score_map[user_id] = avg_score
    sorted_users = sorted(score_map.items(), key=lambda x: x[1], reverse=True)
    return sorted_users

#computes absolute rank and normalized score
def get_user_ranking(actual_user: UserID, ranked_user_ids: List[UserID]) -> Tuple[int, float]:
    if actual_user in ranked_user_ids:
        rank = ranked_user_ids.index(actual_user) + 1
    else:
        rank = len(ranked_user_ids) + 1
    normalized_score = rank / len(ranked_user_ids)
    return rank, normalized_score

# compares the tasks
def compare_task(model, issues_test: Dict[IssueID, Embedding], issues_embed: Dict[UserID, List[Embedding]],getUserID: Callable[[IssueID], UserID]) -> Dict[IssueID, Dict[str, Any]]:
    results: Dict[IssueID, Dict[str, Any]] = {}

    for issue_id, test_embed in issues_test.items():
        sorted_users = rank_users_by_similarity(model, test_embed, issues_embed)
        ranked_user_ids = [user_id for user_id, _ in sorted_users]
        actual_user = getUserID(issue_id)
        rank, normalized_score = get_user_ranking(actual_user, ranked_user_ids)

        results[issue_id] = {
            "actual_user": actual_user,
            "rank": rank,
            "normalized_score": normalized_score,
            "sorted_users": ranked_user_ids
        }

    return results