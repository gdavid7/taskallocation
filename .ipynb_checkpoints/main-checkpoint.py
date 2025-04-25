import JSON_METHODS.create_issues_export
import JSON_METHODS.json_save
#from models.child_classes.codebert_model import Codebert
import models.parent_class
import models.child_classes.codebert_model
import JSON_METHODS.import_logic
import model_comparison.compare_task
import data_science.ndcg
import data_science.mean_reciprocal_rank
import JSON_METHODS.data_split
import data_science.formulas

print("PERFORMANCE BASED TAASK ALLOCATION WITH PAST SPRINT DATA")
if __name__ == '__main__':
    
    # LOAD THE MODELS
    model = models.child_classes.codebert_model.Codebert(name="codebert_similarity_model")
    print(model.name())

    
    # PHASE 1: Create the JSON File of Testing Data
    print("Phase 1: Grabbing users and issues from TAWOS Database:")
    user_issues = JSON_METHODS.create_issues_export.user_issues_dict() # Creating the dictionary object

    user_embeds = JSON_METHODS.create_issues_export.convertToEmbed(model, user_issues) # Convert each issue into an NLP embed
    JSON_METHODS.json_save.save_to_json_file(user_embeds) # Saving the data to data_exports/issues_export.json

    # SPLIT THE DATA
    JSON_METHODS.data_split.split_data()
    
    
    # Import the training data into an object (80%)
    trainingData = JSON_METHODS.import_logic.load_data("data_exports/train_data.json")

    # Import the testing data (20%) into an object
    testingData = JSON_METHODS.import_logic.load_data("data_exports/test_data.json")    

    ndcg_scores = {}
    mrr_scores = {}
    pri_scores = {}
    for user_id, tasks in testingData.items():
        for task in tasks:
            task_results = model_comparison.compare_task.compare_single_task(model, task, trainingData)
            sorted_results_list = sorted(task_results.keys(), key=lambda k: task_results[k], reverse=True)
            #algorithm_result_ndcg = data_science.ndcg.run(sorted_results_list, user_id)
            #algorithm_result_mrr = data_science.mean_reciprocal_rank.run(sorted_results_list, user_id)
            algorithm_result_pri = data_science.formulas.run(sorted_results_list, user_id)
            pri_scores[task['id']] = algorithm_result_pri
            #ndcg_scores[task['id']] = algorithm_result_ndcg
            #mrr_scores[task['id']] = algorithm_result_mrr
    #print("NDCG SCORES: ")
    #print(ndcg_scores)
    #print("MRR SCORES: ")
    #print(mrr_scores)
    print("PRI SCORES: ")
    print(pri_scores)
    #average_ndcg = sum(ndcg_scores.values()) / len(ndcg_scores)
    #average_mrr = sum(mrr_scores.values()) / len(mrr_scores)
    average_pri = sum(pri_scores.values()) / len(pri_scores)

    #print("Average:", average_ndcg)
    #print("Average: ", average_mrr)
    print("Average: " , average_pri)
    
