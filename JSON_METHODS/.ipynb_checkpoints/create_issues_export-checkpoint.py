import JSON_METHODS.database_connect as database_connect

def user_issues_dict():
    # issues_export.json
    return database_connect.connect_to_db()



def convertToEmbed(model, issuesDict:dict) -> dict:
    '''
    Convert each issue in the user:issues dictionary to it's embed form, and return a dictionary containing as such
    '''
    newDict = {}
    totalProcessed = 0
    for user, issues in issuesDict.items():
        print(f"Processed {totalProcessed} users so far")
        totalProcessed+=1
        newDict[user] = issues
        for issue in newDict[user]:
            # Adding the embed as a key in the dictionary
            issue["embed"] = model.convert(issue)
            #print("Issue being converted now")
            #issuesEmbeds.append(model.convert(issue)) # This syntax is wrong so it needs to be changed
        #if totalProcessed >= 20:
        #    break
    return newDict
            
        
        
        

