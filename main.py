import json
from split_issues import split_issues_80_20
from models.codebert_model import compare_tasks_cb


# CODEBERT MODEL COMPARISON TEST

# we need to split now
train_issues_by_user, test_issues_by_user = split_issues_80_20()

total_score = 0
num_comparisons = 0

# compare them
for user in test_issues_by_user:
    if user in train_issues_by_user:
        for test_task in test_issues_by_user[user]:
            for train_task in train_issues_by_user[user]:
                similarity = compare_tasks_cb(test_task, train_task) #codebert comparison
                num_comparisons += 1
                total_score += similarity
                # tell us the individual score
                print(f"User {user} - similarity between tasks{test_task['issue_key']} & {train_task['issue_key']}: {similarity:.4f}") 

# now we know the OVERALL score 
print(f"Overall Score = {total_score/num_comparisons:.4f}")