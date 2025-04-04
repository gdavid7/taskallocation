import json
from split_issues import split_issues_80_20
from models.codebert_model import compare_tasks_cb
import os
import time
from datetime import timedelta

# ------------------------- START OF CODEBERT MODEL COMPARISON TEST  ------------------------- #
# we need to split now
train_issues_by_user, test_issues_by_user = split_issues_80_20()

total_score = 0
num_comparisons = 1
unique_users = set()
start_time = time.time()  # Start the timer

# compare them
for user in test_issues_by_user:
    if user in train_issues_by_user:
        for test_task in test_issues_by_user[user]:
            for train_task in train_issues_by_user[user]:
                if user not in unique_users:
                    unique_users.add(user)
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))
                    print(f"Working on user {user}")
                    print(f"Time elapsed: {elapsed_time_str}")
                    print(f"current accuracy: {total_score/num_comparisons}") 
                similarity = compare_tasks_cb(test_task, train_task)  # codebert comparison
                num_comparisons += 1
                total_score += similarity
                # tell us the individual score
                #print(f"User {user} - similarity between tasks {test_task['issue_key']} & {train_task['issue_key']}: {similarity:.4f}") 

# now we know the OVERALL score
overall = total_score / num_comparisons
total_time = time.time() - start_time
total_time_str = str(timedelta(seconds=int(total_time)))
print(f"Overall Score = {overall:.4f}")
print(f"Total time taken: {total_time_str}")

# Create the string to dump the result into the file
dumping_string = f"Overall Score of the codebert model was: {overall}\n"
dumping_string += f"Total time taken: {total_time_str}"
os.makedirs("models", exist_ok=True) # Ensure the 'models' directory exists

# Write the overall score to a text file inside the 'models' folder
with open("models/results.txt", "w", encoding="utf-8") as f:
    f.write(dumping_string)

print("Overall score has been saved to 'models/results.txt'.")
# ------------------------- END OF CODEBERT MODEL COMPARISON TEST  ------------------------- #