import os
import git_status_in_repos as gsir
from subprocess import call
from pathlib import Path


class TestGitStatusInRepos:
    def setup_test_tree(self, tmp_path):
        """ Create the following directory tree:
            tmp_path
            |- repo_clean
            |   |- .git
            |- subdir
            |   |- repo_modified
            |   |   |- .git
            |   |   |- README.md
            |- not_a_repo
        """
        os.chdir(tmp_path)
        os.mkdir("repo_clean")
        call("git init", shell=True, cwd="repo_clean")

        repo_modified = Path("subdir") / "repo_modified"
        os.makedirs(repo_modified)
        call("git init", shell=True, cwd=repo_modified)
        with open(repo_modified / "README.md", "w") as readme_file:
            readme_file.write("some content")
        call("git add README.md", shell=True, cwd=repo_modified)

        os.mkdir("not_a_repo")

    def test_search_no_repos(self, tmp_path):
        git_repos = gsir.search_for_git_repos_in_dir(tmp_path)
        assert len(git_repos) == 0

    def test_search_nominal(self, tmp_path):
        self.setup_test_tree(tmp_path)
        git_repos = gsir.search_for_git_repos_in_dir(tmp_path)
        assert len(git_repos) == 2

    def test_status_empty(self, tmp_path):
        self.setup_test_tree(tmp_path)
        status = gsir.git_status_in_dir(tmp_path / "repo_clean")
        assert status == ""

    def test_status_file_added(self, tmp_path):
        self.setup_test_tree(tmp_path)
        status = gsir.git_status_in_dir(tmp_path / "subdir" / "repo_modified")
        assert status == "A  README.md"
