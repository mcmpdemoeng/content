from github import Github
import time


def close_pull_requests( repoConnection, baseBranch='master' ):
    """
        Params:
            repoConnection ( Required Object ): Object from Github library with all required credentials
            baseBranch (optional string): Filter
    """
    pulls = repoConnection.get_pulls( state='open', sort='created', base=baseBranch )
    for pull in pulls:
        pull.edit(state='close')
        


def merge_pull_request( repoConnection, baseBranch='master', headBranch=None ):
    """
        Params:
            repoConnection ( Required Object ): Object from Github library with all required credentials
            baseBranch (optional string): Filter
    """
    pulls = repoConnection.get_pulls( state='open', sort='created', base=baseBranch )
    
    for pull in pulls:

        if headBranch and headBranch in pull.head.label:
            pull.merge("Automatic merge")

        elif not headBranch:
            pull.merge("Automatic merge")
        


def verify_branch_exists(repoConnection, branchToverify: str, logErrors=False):
    try:
            
        branches = repoConnection.get_branches()
        for branch  in branches:
            if branch.name == branchToverify:
                return True
        return False
    except BaseException as error:
        if logErrors:
            print(f"Error: {error} ")
        return False


def create_branch(repoConnection, newBranchName):
    try:
        source_branch = 'master'
        sb = repoConnection.get_branch(source_branch)
        repoConnection.create_git_ref(ref='refs/heads/' + newBranchName, sha=sb.commit.sha)
        return True

    except BaseException as error:

        return False


    
def verify_github_file_exists( filePath, repoConnection, branch='master' ):
    """
    Params:
        filePath (Required string): Path of the file in the repo
            Example: atomatic_commit_log.log
        
        repoConnection (Required Object): Object from Github library with all required credentials
    """
    try:

        content = repoConnection.get_contents( filePath, ref=branch )
        return True, {
            "sha": content.sha,
            "content": content.decoded_content.decode("UTF-8")
        }

    except BaseException as error:
        return False, {}


def create_commit( repoConnection, commitName="Automatic Commit", branch="master", fileToLog="atomatic_commit_log.log", logErrors=False ):
    """
        params:
            repoConnection ( Required Object ): Object from Github library with all required credentials

            commitName ( Optional string ): Default is 'Automatic Commit'

            Branch ( Optional string ): Default is set to 'master'

            fileToLog: (Optional string): filename to write the new content to commit
    """

    
    fileExists, fileData  =  verify_github_file_exists( filePath=fileToLog, repoConnection=repoConnection, branch=branch )
    
    try:
        newContent =  f"\nAutomatic commit {time.asctime()}"

        if fileExists:
            repoConnection.update_file( path=fileToLog, message=commitName, content=newContent, sha=fileData["sha"], branch=branch )

        else:
            
            repoConnection.create_file( path=fileToLog, message=commitName,  content=newContent, branch=branch )

        return True, ""
    
    except BaseException as error:
        if logErrors:
            print(error)
        return False, str(error)



def create_pull_request( repoConnection, headBranch, baseBranch='master', body="Body exmaple", logErrors=False ):
    """
        - MAKE SURE YOU ALREADY COMMITED SOMETHING IN THE BRANCH BEFORE EXECUTING A PR
        - make sure this branch exists and has no conflicts at the time of creating the PR
        Params:
            repoConnection ( Required Object ): Object from Github library with all required credentials
            headBranch ( Required string ): branch with the new changes
            baseBranch ( Optional string): branch to merge, default is set to 'master'
    """
  
    try:
        
        pullReqName = f"Automatic PR - {time.asctime()}"
        repoConnection.create_pull(title=pullReqName, body=body, head=headBranch, base=baseBranch )
        return True, ""
        
    except BaseException as error:
        if logErrors:
            print(error)
        return False, str(error)

def create_issue( repoConnection, labels=[], title="issue creted from python", log_errors=False, description="Default Description" ) -> str:
    """
        Params:
            repoConnection ( Required Object ): Object from Github library with all required credentials

            labels (optional): 
                Example: ['critical', 'Red Thread']

            log_errors (optional bool): Print errors on screen, default is False
    """

    try: 
        issueData = repoConnection.create_issue( title=title, labels=labels, body=description )
        return issueData.number
    except BaseException as error:

        if log_errors:
            print(error)

        return None


def update_issue(repoConnection, issueNumber):
    """
        Params:
            repoConnection ( Required Object ): Object from Github library with all required credentials
    """
    try:

        issue = repoConnection.get_issue( number=issueNumber )
        comment = f"Automated comment - {time.asctime()}"
        issue.create_comment( comment )
        return True, ""

    except BaseException as error:

        return False, str(error)



def create_close_issue(repoConnection, labels = []):
    """
        Params:
            repoConnection ( Required Object ): Object from Github library with all required credentials
    """
    try:

        issueNumber = create_issue( repoConnection=repoConnection, labels=labels )
        issue = repoConnection.get_issue( number=issueNumber )
        issue.edit( state='closed' )
        return True, ""

    except BaseException as error:

        return False, str(error)

def close_issues(repoConnection, Labelfilters=["documentation"] ):
    issues = repoConnection.get_issues()
    for issue in issues:
        for label in issue.labels:
            if label.name in Labelfilters :
                issue.edit( state='closed' )
