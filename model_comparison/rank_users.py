from compare_task import compute_average_similarity

# builds and sorts user score map
def rank_users_by_similarity(model, test_embed, issues_embed) -> list:
    score_map = {}
    for user_id, training_embeds in issues_embed.items():
        avg_score = compute_average_similarity(model, test_embed, training_embeds)
        if avg_score > 0:
            score_map[user_id] = avg_score
    sorted_users = sorted(score_map.items(), key=lambda x: x[1], reverse=True)
    return sorted_users

# computes absolute rank and normalized score
def get_user_ranking(actual_user, ranked_user_ids: list) -> tuple:
    if actual_user in ranked_user_ids:
        rank = ranked_user_ids.index(actual_user) + 1
    else:
        rank = len(ranked_user_ids) + 1
    normalized_score = rank / len(ranked_user_ids)
    return rank, normalized_score