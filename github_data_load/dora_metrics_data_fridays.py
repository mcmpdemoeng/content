from github_utils import *
import argparse
import time

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
    releaseNumber = time.strftime("%Y.%m.%d") #Using number of the week as release counter
    releaseBranchName = f"release-{releaseNumber}"
    create_branch( repoConnection=repoConnection, newBranchName=releaseBranchName )
    close_issues(repoConnection=repoConnection, Labelfilters=["User Story", "Epic"])


if __name__ == "__main__":    
    main()