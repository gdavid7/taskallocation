import JSON_METHODS.create_issues_export
import JSON_METHODS.json_save

print("PERFORMANCE BASED TAASK ALLOCATION WITH PAST SPRINT DATA")
if __name__ == '__main__':

    # LOAD THE MODELS
    model = None # fill this in


    # PHASE 1: Create the JSON File
    print("Phase 1: Grabbing users and issues from TAWOS Database:")
    user_issues = JSON_METHODS.create_issues_export.user_issues_dict() # Creating the dictionary object
    user_embeds = JSON_METHODS.create_issues_export.convertToEmbed(model, user_issues) # Convert each issue into an NLP embed
    JSON_METHODS.json_save.save_to_json_file(user_embeds) # Saving the data to data_exports/issues_export.json

    
    



