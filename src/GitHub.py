from github import Github
import re


class GithubClient:
    def __init__(self, accessToken):
        self.accessToken = accessToken
        self.client = Github(accessToken)

    def getDictGitPR(self, repoName, prRegex):
        repo = self.client.get_repo(repoName)
        allPulls = repo.get_pulls()
        pullsDictionare = {}
        for pull in allPulls:
            if(re.search(prRegex, pull.title) != None):
                pullsDictionare[pull.user.login] = pull
        return pullsDictionare

    def getPRById(self, repoName, prId):
        repo = self.client.get_repo(repoName)
        pr = repo.get_pull(prId)
        return pr
