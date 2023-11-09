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
    releaseNumber = time.strftime("%Y.%m.%d") 
    releaseBranchName = f"release-{releaseNumber}"
    create_branch( repoConnection=repoConnection, newBranchName=releaseBranchName )
    
    ## Release management data
    labelsForSev1 = [f"found_{releaseBranchName}", "sev1", "bug", ]
    create_issue(repoConnection=repoConnection, labels=labelsForSev1, title=f"Severity 1 issue - release {releaseBranchName}" )

    labelsForSev2 = [f"found_{releaseBranchName}", "sev2", "bug", "User Story" ]
    create_issue( repoConnection=repoConnection, labels=labelsForSev2, title=f"Severity 2 issue - release {releaseBranchName}" )
    ## /Release management data

    close_issues(repoConnection=repoConnection, Labelfilters=["User Story", "Epic"])
    close_issues(repoConnection=repoConnection, Labelfilters=labelsForSev1)
    close_issues(repoConnection=repoConnection, Labelfilters=labelsForSev2)


if __name__ == "__main__":
    main()