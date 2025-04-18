import JSON_METHODS.create_issues_export
import JSON_METHODS.json_save
#from models.child_classes.codebert_model import Codebert
import models.parent_class
import models.child_classes.codebert_model
import data_exports.testingEmbeds
import JSON_METHODS.import_logic
import model_comparison.compare_task


print("PERFORMANCE BASED TAASK ALLOCATION WITH PAST SPRINT DATA")
if __name__ == '__main__':
    
    # LOAD THE MODELS
    model = models.child_classes.codebert_model.Codebert(name="codebert_similarity_model")
    print(model.name())
    '''
    # PHASE 1: Create the JSON File of Testing Data
    print("Phase 1: Grabbing users and issues from TAWOS Database:")
    user_issues = JSON_METHODS.create_issues_export.user_issues_dict() # Creating the dictionary object
    user_embeds = JSON_METHODS.create_issues_export.convertToEmbed(model, user_issues) # Convert each issue into an NLP embed
    JSON_METHODS.json_save.save_to_json_file(user_embeds) # Saving the data to data_exports/issues_export.json
    '''

    # Import the testing data into an object
    data = JSON_METHODS.import_logic.load_data()
    print("Testing Task: " + str(data["68"]))
    '''

    # Get an Embed as the testing data
    testing = {68:data_exports.testingEmbeds.testingEmbed()}
    
    # Get the rankings
    results = model_comparison.compare_task.compare_all_task(model, testing, data)
    print(results)
    '''
