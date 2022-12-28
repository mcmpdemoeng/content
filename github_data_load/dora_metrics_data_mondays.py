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

    #TODO: we need to get the real epic link
    epicLink = f"https://github.com/{setup['repo']}/issues/{issueNumber}" 

    # Create Issue for the Epic
    titleName = f"User story {date} Epic: {epicLink}"
    storyIssueNumber = create_issue( repoConnection, labels=["User Story"], title=titleName, log_errors=True )
    if not storyIssueNumber:
        raise Exception("Unable to create issue")

    #Commit something to 'master'
    _, errorMessage = create_commit( repoConnection, "Autmatic commit", "master"  )
    if errorMessage:
        print(errorMessage)
        return Exception("Unable to commit changes")

    #create PR from 'master' to 'release-2023'
    bodyDescription = f"User Story: https://github.com/{setup['repo']}/issues/{storyIssueNumber}"
    create_pull_request( repoConnection, "master", "release-2023", body=bodyDescription )









if __name__ == "__main__":
    main()
    
   