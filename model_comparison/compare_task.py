# create a function that takes in 3 formal paraemeters:
    # (model, test_task, train_task)

# maybe we can use matplotlab to plot the progression?
import json

# scoring logic and skips same embed
def compute_average_similarity(model, test_embed, training_embeds:list) -> float:
    # Iterates through embeds for one user
    if len(training_embeds) == 0:
        return 0
    total_score = 0
    count = 0
    for train_embed in training_embeds:
        
        if (test_embed == train_embed).all(): #comparing 2 numpy arrays
            continue
        score = model.compare(test_embed, train_embed)
        total_score += score
        count += 1
    return total_score / count

# compares a SINGLE task against each user to find average scores for each one
def compare_single_task(model, testing_embed, database_embeds:dict) -> dict:
    # ex: comparing test task 1 against everything. issues_test is an embed
    results = {}
        # Now we have our embed that we want to compare against all the other ones
        # Comparing against all users in the database:
    for user_ID, user_embeds in database_embeds.items():
        print(user_ID, user_embeds)
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
