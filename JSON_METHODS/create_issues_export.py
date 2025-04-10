import JSON_METHODS.database_connect as database_connect

def user_issues_dict():
    # issues_export.json
    return database_connect.connect_to_db()



def convertToEmbed(model, issuesDict:dict) -> dict:
    '''
    Convert each issue in the user:issues dictionary to it's embed form, and return a dictionary containing as such
    '''
    newDict = {}
    for user, issues in issuesDict.items():
        issuesEmbeds = []
        if(len(issues) > 0):
            for issue in issues:
                issuesEmbeds.append(model.convert(issue)) # This syntax is wrong so it needs to be changed
        newDict[user] = issuesEmbeds
    return newDict
            
        
        
        

