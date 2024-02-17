import os
from list_repos import RepositoryListHelper
from origin import Origin
from destination import Destiny
from dotenv import load_dotenv


def sync():
    list_helper = RepositoryListHelper("bitbucket")
    repos = list_helper.list_repos(
        os.environ.get("BITBUCKET_WORKSPACE"), os.environ.get("BITBUCKET_PROJECT")
    )
    print(repos)
    print(len(repos))
    origin = Origin(repos, os.environ.get("ORIGIN_BASE_URL"), "./repos")
    origin.clone_parallel()
    commits = origin.list_commits(repos)

    destiny = Destiny("./bitbucket-activity-sync-mock")
    destiny.sync(commits)


if __name__ == "__main__":
    load_dotenv()
    sync()
