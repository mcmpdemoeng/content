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
    print(f"Creating sev1 for {releaseBranchName}")
    labelsForSev1 = [f"found_{releaseBranchName}", "sev1", "bug", ]
    sev1_issueNumber = create_issue(repoConnection=repoConnection, labels=labelsForSev1, title=f"Severity 1 issue - release {releaseBranchName}" )
    print(f"issue number -> {sev1_issueNumber}")
    
    print(f"Creating sev2 for {releaseBranchName}")
    labelsForSev2 = [f"found_{releaseBranchName}", "sev2", "bug", "User Story" ]
    sev2_issueNumber = create_issue( repoConnection=repoConnection, labels=labelsForSev2, title=f"Severity 2 issue - release {releaseBranchName}" )
    print(f"issue number -> {sev2_issueNumber}")

    ## /Release management data

    close_issues(repoConnection=repoConnection, Labelfilters=["User Story", "Epic"])
    # Not closing the sev issues
    # close_issues(repoConnection=repoConnection, Labelfilters=labelsForSev1)
    # close_issues(repoConnection=repoConnection, Labelfilters=labelsForSev2)


if __name__ == "__main__":
    main()