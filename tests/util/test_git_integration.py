"""GitIntegration のユニットテスト

実際の git repo を ``tmp_path`` に作って subprocess を実行する形で検証する。
mock よりも本物の git を呼んだほうが ADR-0002 の想定 (subprocess 直呼び)
をそのまま検証できるため。CI に git が無い環境はスキップ扱い。
"""
import shutil
import subprocess

import pytest

from utils.exceptions import (
    KasuGitNotFoundError,
    KasuInvalidGitRefError,
    KasuNotAGitRepoError,
)
from utils.git import GitIntegration


_GIT_AVAILABLE = shutil.which("git") is not None
requires_git = pytest.mark.skipif(not _GIT_AVAILABLE, reason="git not in PATH")


@pytest.fixture
def git_repo(tmp_path):
    """init → commit 2 回で 2 つのリビジョンを持つ repo を作る"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _run(["git", "init", "-q", "-b", "main"], cwd=repo)
    _run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    _run(["git", "config", "user.name", "Tester"], cwd=repo)

    (repo / "a.txt").write_text("hello\n")
    _run(["git", "add", "a.txt"], cwd=repo)
    _run(["git", "commit", "-q", "-m", "first"], cwd=repo)

    (repo / "b.txt").write_text("world\n")
    (repo / "a.txt").write_text("hello changed\n")
    _run(["git", "add", "-A"], cwd=repo)
    _run(["git", "commit", "-q", "-m", "second"], cwd=repo)

    return repo


def _run(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


@requires_git
class TestGitIntegrationInit:
    def test_non_git_dir_raises(self, tmp_path):
        with pytest.raises(KasuNotAGitRepoError):
            GitIntegration(str(tmp_path))

    def test_nonexistent_dir_raises(self, tmp_path):
        with pytest.raises((KasuNotAGitRepoError, KasuGitNotFoundError)):
            GitIntegration(str(tmp_path / "nope"))


@requires_git
class TestGitIntegrationCommands:
    def test_list_changed_files_between_revisions(self, git_repo):
        git = GitIntegration(str(git_repo))
        changed = git.list_changed_files("HEAD~1")
        assert set(changed) == {"a.txt", "b.txt"}

    def test_get_diff_contains_changed_content(self, git_repo):
        git = GitIntegration(str(git_repo))
        diff = git.get_diff("HEAD~1")
        assert "a.txt" in diff
        assert "b.txt" in diff
        assert "hello changed" in diff

    def test_invalid_ref_raises(self, git_repo):
        git = GitIntegration(str(git_repo))
        with pytest.raises(KasuInvalidGitRefError):
            git.list_changed_files("does-not-exist-ref-xyz")
        with pytest.raises(KasuInvalidGitRefError):
            git.get_diff("does-not-exist-ref-xyz")

    def test_dash_prefixed_ref_is_rejected(self, git_repo):
        """argument injection 対策: ``-`` 始まりの ref は拒否する"""
        git = GitIntegration(str(git_repo))
        for ref in ["-upload-pack=evil", "--foo", "-"]:
            with pytest.raises(KasuInvalidGitRefError):
                git.list_changed_files(ref)
            with pytest.raises(KasuInvalidGitRefError):
                git.get_diff(ref)

    def test_empty_ref_is_rejected(self, git_repo):
        git = GitIntegration(str(git_repo))
        with pytest.raises(KasuInvalidGitRefError):
            git.list_changed_files("")
        with pytest.raises(KasuInvalidGitRefError):
            git.get_diff("")
