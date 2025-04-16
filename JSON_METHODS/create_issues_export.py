import JSON_METHODS.database_connect as database_connect

def user_issues_dict():
    # issues_export.json
    return database_connect.connect_to_db()



def convertToEmbed(model, issuesDict:dict) -> dict:
    '''
    Convert each issue in the user:issues dictionary to it's embed form, and return a dictionary containing as such
    '''
    totalProcessed = 0
    newDict = {}
    for user, issues in issuesDict.items():
        if totalProcessed % 500 == 0:
            print(f"Processed {totalProcessed} users so far")
        totalProcessed+=1
        issuesEmbeds = []

        if(len(issues) > 0):
            for issue in issues:
                #print("Issue being converted now")
                issuesEmbeds.append(model.convert(issue)) # This syntax is wrong so it needs to be changed

        newDict[user] = issuesEmbeds
        if totalProcessed >= 1000:
            break
    return newDict
            
        
        
        

