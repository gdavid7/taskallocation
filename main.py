import json
from split_issues import split_issues_80_20
from models.codebert_model import compare_tasks_cb
import os

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
                similarity = compare_tasks_cb(test_task, train_task)  # codebert comparison
                num_comparisons += 1
                total_score += similarity
                # tell us the individual score
                print(f"User {user} - similarity between tasks {test_task['issue_key']} & {train_task['issue_key']}: {similarity:.4f}") 

# now we know the OVERALL score
overall = total_score / num_comparisons
print(f"Overall Score = {overall:.4f}")

# Create the string to dump the result into the file
dumping_string = "Overall Score of the codebert model was: "
dumping_string += str(overall)  # Correct conversion of float to string

# Ensure the 'models' directory exists
os.makedirs("models", exist_ok=True)

# Write the overall score to a text file inside the 'models' folder
with open("models/results.txt", "w", encoding="utf-8") as f:
    f.write(dumping_string)

print("Overall score has been saved to 'models/results.txt'.")
