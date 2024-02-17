import os
from atlassian.bitbucket import Cloud
from github import Github
from github import Auth
from dotenv import load_dotenv


class RepositoryListHelper:
    def __init__(self, mode):
        self.mode = mode
        if mode == "github":
            auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
            self.github = Github(auth=auth)
        if mode == "bitbucket":
            self.bitbucket = Cloud(
                username=os.getenv("BITBUCKET_USERNAME"),
                password=os.getenv("BITBUCKET_PASSWORD"),
                cloud=True,
            )

    def list_repos(self, workspace=None, project=None):
        if self.mode == "github":
            repos = list(self.github.get_user().get_repos())
        elif self.mode == "bitbucket":
            repos = []
            workspace = self.bitbucket.workspaces.get(workspace)
            project = workspace.projects.get(project)
            repos = []
            for repo in project.repositories.each():
                repos.append(repo.slug)
        else:
            raise NotImplementedError(f"{self.mode} listing is not yet implemented.")

        return repos


if __name__ == "__main__":
    load_dotenv()
    repo_helper = RepositoryListHelper("bitbucket")
