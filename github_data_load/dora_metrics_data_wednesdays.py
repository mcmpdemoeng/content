from github_utils import *
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




def main( ):
    setup = parser()
    repoConnection = Github( setup["gitHubToken"] ).get_repo( setup["repo"] )

    releaseNumber = time.strftime("%w") #Using number of the week as release counter
    releaseBranchName = f"release-2023-{releaseNumber}"
    merge_pull_request( repoConnection=repoConnection, baseBranch=releaseBranchName, headBranch='automation-branch' )
    create_pull_request( repoConnection, headBranch=releaseBranchName, baseBranch="master", body="Release merge", logErrors=True )
    

if __name__ == "__main__":

    main()