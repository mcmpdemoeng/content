from github_utils import *
import time
import argparse

def parser( ) -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", help="<Optional> Github Token")
    parser.add_argument( '-r', "--repository",   help='<Required> repository name \Format: "mariobv/samplerepo"', required=True )
    values = parser.parse_args()
    return {
        "gitHubToken" : values.token,
        "repo" : values.repository
    }


def main():

    setup =  parser()
    repoConnection = Github( setup["gitHubToken"] ).get_repo( setup["repo"] )

    # Create Epic
    date = time.strftime("%d-%m-%Y %H:%M")
    titleName = f"Epic - {date}"
    issueNumber = create_issue( repoConnection, labels=[ "Epic" ], title=titleName, log_errors=True )
    if not issueNumber:
        raise Exception("Unable to create issue")

    
    epicLink = f"https://github.com/{setup['repo']}/issues/{issueNumber}" 

    # Create Issue for the Epic
    titleName = f"User story {date}"
    description = f"Epic: {epicLink}"
    storyIssueNumber = create_issue( repoConnection, labels=["User Story"], title=titleName, description=description,log_errors=True )
    if not storyIssueNumber:
        raise Exception("Unable to create issue")

    #Commit something to 'master'
    _, errorMessage = create_commit( repoConnection, "Autmatic commit from jenkins dora metrics", "release-2023", fileToLog="dora_metrics_log.log"  )
    if errorMessage:
        print(errorMessage)
        return Exception("Unable to commit changes")

    #create PR from 'release-2023' to 'master'
    bodyDescription = f"https://github.com/{setup['repo']}/issues/{storyIssueNumber}"
    create_pull_request( repoConnection, headBranch="master", baseBranch="release-2023", body=bodyDescription )









if __name__ == "__main__":
    main()
    
   
