import os
from git import Repo, Commit
from multiprocessing import Process


class Origin:
    def __init__(self, repo_list, base_url, base_clone_path):
        self.repo_list = repo_list
        self.base_url = base_url
        self.base_clone_path = base_clone_path

    def clone_parallel(self, workers=8):
        size = len(self.repo_list) // workers + 1
        lists = [
            self.repo_list[i : i + size] for i in range(0, len(self.repo_list), size)
        ]
        procs = []
        for list in lists:
            proc = Process(target=self.clone, args=(list,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

    def clone(self, list):
        for repo in list:
            if not os.path.isdir(self.base_clone_path + f"/{repo}"):
                repo = Repo.clone_from(
                    self.base_url + repo, self.base_clone_path + f"/{repo}"
                )
                print(f"Clonou {repo}")
            else:
                print(f"{repo} Já estava clonado")
                pass

    def list_commits(self, list):
        repo_commits: dict[str, list[Commit]] = {}
        for repo_name in list:
            repository = Repo(self.base_clone_path + f"/{repo_name}")
            repo_commits[repo_name] = []
            try:
                commits = repository.iter_commits("master")
                for commit in commits:
                    repo_commits[repo_name].append(commit)
            except:
                pass
        return repo_commits


if __name__ == "__main__":
    origin = Origin(["exemplo_de_repositorio"], "git@bitbucket.org:baseurl/", "./repos")
    origin.clone()
