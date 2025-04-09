# create a function that takes in 3 formal paraemeters:
    # (model, test_task, train_task)

# maybe we can use matplotlab to plot the progression?
import json

# scoring logic and skips same embed
def compute_average_similarity(model, test_embed, training_embeds:list) -> float:
    # Iterates through embeds for one user
    if len(training_embeds == 0):
        return 0
    total_score = 0
    count = 0
    for train_embed in training_embeds:
        if test_embed == train_embed:
            continue
        score = model.compare(test_embed, train_embed)
        total_score += score
        count += 1
    return total_score / count

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


# compares a SINGLE task against each user to find average scores for each one
def compare_single_task(model, testing_embed, database_embeds:dict) -> dict:
    # ex: comparing test task 1 against everything. issues_test is an embed
    results = {}
        # Now we have our embed that we want to compare against all the other ones
        # Comparing against all users in the database:
    for user_ID, user_embeds in database_embeds.items():
        user_avg_similarity = compute_average_similarity(model, testing_embed, user_embeds)
        # store the similarity score for the user
        results[user_ID] = user_avg_similarity
    return results

# O(n^2)
def compare_all_task(model, testing_embeds, database_embeds:dict) -> dict:
    results = {}
    # go through all the other testing since we only did it once
    for task_id, testing_embed in testing_embeds.items():
        task_results = compare_single_task(model, testing_embed, database_embeds)
        results[task_id] = task_results

    return results