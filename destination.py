import os
import hashlib
from git import Repo, Commit
from dotenv import load_dotenv
import datetime
import pytz


class Destiny:
    def __init__(self, path):
        self.path = path
        try:
            self.repo = Repo(path)
        except:
            self.repo = Repo.init(path)
        print(self.repo.working_tree_dir)
        print(self.repo.index.write_tree())
        self.author_emails = os.getenv("AUTHOR_EMAILS").split(",")

    def sync(self, repo_commits: dict[Repo, list[Commit]]):
        desired_commits = []
        for repo, commits in repo_commits.items():
            repo_hash = hashlib.md5()
            repo_hash.update(repo.encode("utf-8"))
            repo_filename = str(int(repo_hash.hexdigest(), 16))[0:12]
            for commit in commits[::-1]:
                if commit.author.email in self.author_emails:
                    filename = self.path + f"/{repo_filename}"
                    file_for_repo = open(filename, "a+")
                    file_for_repo.seek(0)
                    already_synced_commits = file_for_repo.read().splitlines()

                    if str(commit) not in already_synced_commits:
                        file_for_repo.write(str(commit) + "\n")
                        file_for_repo.close()
                        self.repo.git.add("-A")
                        self.repo.index.commit(
                            message=str(commit),
                            author=commit.author,
                            committer=commit.committer,
                            commit_date=datetime.datetime.fromtimestamp(
                                commit.committed_date, pytz.UTC
                            ),
                            author_date=datetime.datetime.fromtimestamp(
                                commit.authored_date, pytz.UTC
                            ),
                        )
                    file_for_repo.close()


if __name__ == "__main__":

    load_dotenv()
    d = Destiny("./testenovo")
