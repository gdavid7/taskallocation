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

# Create or clear the results file at the start
try:
    os.makedirs("models", exist_ok=True)
    results_file_path = os.path.join("models", "results.txt")
    print(f"Attempting to create/clear file at: {os.path.abspath(results_file_path)}")
    
    with open(results_file_path, "w", encoding="utf-8") as f:
        f.write("Starting new results file\n")
        print("Successfully created/cleared results file")
except Exception as e:
    print(f"Error creating/clearing results file: {str(e)}")

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
                    # Print to terminal
                    print(f"Working on user {user}")
                    print(f"Time elapsed: {elapsed_time_str}")
                    print(f"current accuracy: {total_score/num_comparisons}")
                    # Write to file
                    try:
                        with open(results_file_path, "a", encoding="utf-8") as f:
                            f.write(f"Working on user {user}\n")
                            f.write(f"Time elapsed: {elapsed_time_str}\n")
                            f.write(f"current accuracy: {total_score/num_comparisons}\n")
                            print(f"Successfully wrote data for user {user} to file")
                    except Exception as e:
                        print(f"Error writing to file for user {user}: {str(e)}")
                similarity = compare_tasks_cb(test_task, train_task)  # codebert comparison
                num_comparisons += 1
                total_score += similarity

# now we know the OVERALL score
overall = total_score / num_comparisons
total_time = time.time() - start_time
total_time_str = str(timedelta(seconds=int(total_time)))
print(f"Overall Score = {overall:.4f}")
print(f"Total time taken: {total_time_str}")

# Write final results to file
try:
    with open(results_file_path, "a", encoding="utf-8") as f:
        f.write(f"\nOverall Score = {overall:.4f}\n")
        f.write(f"Total time taken: {total_time_str}\n")
    print("Successfully wrote final results to file")
except Exception as e:
    print(f"Error writing final results to file: {str(e)}")

print("Results have been saved to 'models/results.txt'.")
# ------------------------- END OF CODEBERT MODEL COMPARISON TEST  ------------------------- #