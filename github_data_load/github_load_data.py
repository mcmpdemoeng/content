
from unittest import result
from github_utils import *
import json
import argparse

"""
IN CASE THE DEFAULT BRANCH IS NOT MASTER  THE PULL REQUEST WILL FAIL
WE NEED TO FIX THAT
"""

def parser( ) -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", help="<Optional> Github Token")
    parser.add_argument( '-r', "--repositories", nargs="+",  help='<Required> repository name \nExample: mariobv/samplerepo', required=True )
    values = parser.parse_args()
    return {
        "gitHubToken" : values.token,
        "repoList" : values.repositories
    }


def load_repo( repoName, gitToken="" )-> dict:
    """
        Params:
            repoName ( Required Object ): Object from Github library with all required credentials
            gitToken ( Optional string ): 

    """
    
    repoConnection = Github( gitToken ).get_repo( repoName )

    resultsList = []
    resultsList.append( close_pull_requests( repoConnection=repoConnection, baseBranch='ForDataAutomation' ) )

    resultsList.append( { "create_commit": create_commit( repoConnection=repoConnection, branch="master" ) })
    
    resultsList.append( { "create_pull_request" : create_pull_request( repoConnection=repoConnection, headBranch="master",  baseBranch="ForDataAutomation" ) })
  
    issueNumber = create_issue( repoConnection=repoConnection )
    resultsList.append( { "create_issue" : issueNumber } )

    #Pause for 2 min to avoid the api to restrict the access
    print("WAITING 2min to continue")
    time.sleep(120.0)

    if issueNumber:
        resultsList.append({ "update_issue" : update_issue( repoConnection=repoConnection, issueNumber=issueNumber ) }) 
    resultsList.append( { "create_close_issue" : create_close_issue( repoConnection=repoConnection ) })

    # #Create defect 
    defectNumber = create_issue( repoConnection=repoConnection, labels=["bug"] )
    resultsList.append( { "create_issue(defect)" : issueNumber } )
    if defectNumber:
        resultsList.append( { "update_issue(defect)" : update_issue( repoConnection=repoConnection, issueNumber=defectNumber  ) } ) 
    
    # #Create and close a defect
    resultsList.append( { "create_close_issue" : create_close_issue( repoConnection=repoConnection, labels=["bug"] ) } )

    return {
        "repository" : repoName,
        "results" : resultsList
    }



def validate_params( params ):
    """
    Verify that the repositories exists, an you have the necesary permissions to perfom the 
    require operations
    """
    pass



def showResults( repoResults ):
    for results in repoResults:
        title =f'!!!!!!!!!{results["repository"]}!!!!!!!!!!!!!!'
        print( title )
        
        print( results )



def main():

    params  =  parser( )
    validate_params( params )
    repoResults  =  []

    for repo in params["repoList"]:

       repoResults.append( load_repo(  repoName=repo , gitToken=params["gitHubToken"]  ) )
       print("WAITING 5min to continue")
       time.sleep(3600.0)

    showResults( repoResults )


if __name__ == "__main__":
    main()