"""GitIntegration の境界値・エラーパス補強テスト

既存の tests/util/test_git_integration.py に触れずに追加する。
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


def _run(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


@pytest.fixture
def git_repo_with_tag(tmp_path):
    """init → commit → tag を持つ repo"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _run(["git", "init", "-q", "-b", "main"], cwd=repo)
    _run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    _run(["git", "config", "user.name", "Tester"], cwd=repo)

    (repo / "a.txt").write_text("hello\n")
    _run(["git", "add", "a.txt"], cwd=repo)
    _run(["git", "commit", "-q", "-m", "first"], cwd=repo)
    _run(["git", "tag", "v0.1.0"], cwd=repo)

    (repo / "b.txt").write_text("world\n")
    _run(["git", "add", "b.txt"], cwd=repo)
    _run(["git", "commit", "-q", "-m", "second"], cwd=repo)

    return repo


@pytest.fixture
def git_repo_single_commit(tmp_path):
    """コミットが 1 つだけの repo（空の diff）"""
    repo = tmp_path / "single"
    repo.mkdir()
    _run(["git", "init", "-q", "-b", "main"], cwd=repo)
    _run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    _run(["git", "config", "user.name", "Tester"], cwd=repo)

    (repo / "only.txt").write_text("only\n")
    _run(["git", "add", "only.txt"], cwd=repo)
    _run(["git", "commit", "-q", "-m", "init"], cwd=repo)

    return repo


@pytest.fixture
def git_repo_with_branch(tmp_path):
    """main と feature ブランチを持つ repo"""
    repo = tmp_path / "branched"
    repo.mkdir()
    _run(["git", "init", "-q", "-b", "main"], cwd=repo)
    _run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    _run(["git", "config", "user.name", "Tester"], cwd=repo)

    (repo / "base.txt").write_text("base\n")
    _run(["git", "add", "base.txt"], cwd=repo)
    _run(["git", "commit", "-q", "-m", "base"], cwd=repo)

    _run(["git", "checkout", "-q", "-b", "feature"], cwd=repo)
    (repo / "feature.txt").write_text("feature\n")
    _run(["git", "add", "feature.txt"], cwd=repo)
    _run(["git", "commit", "-q", "-m", "add feature"], cwd=repo)

    return repo


@requires_git
class TestGitIntegrationRefFormats:
    """bare hash / tag / branch 名など様々な ref 形式での動作"""

    def test_list_changed_files_with_tag_ref(self, git_repo_with_tag):
        git = GitIntegration(str(git_repo_with_tag))
        changed = git.list_changed_files("v0.1.0")
        assert "b.txt" in changed

    def test_get_diff_with_tag_ref(self, git_repo_with_tag):
        git = GitIntegration(str(git_repo_with_tag))
        diff = git.get_diff("v0.1.0")
        assert "b.txt" in diff

    def test_list_changed_files_with_bare_hash(self, git_repo_with_tag):
        """bare commit hash を ref として使える"""
        # タグが指す commit hash を取得
        result = subprocess.run(
            ["git", "rev-parse", "v0.1.0"],
            cwd=str(git_repo_with_tag),
            capture_output=True, text=True,
        )
        commit_hash = result.stdout.strip()
        git = GitIntegration(str(git_repo_with_tag))
        changed = git.list_changed_files(commit_hash)
        assert "b.txt" in changed

    def test_list_changed_files_with_branch_name(self, git_repo_with_branch):
        """branch 名を ref として使える"""
        git = GitIntegration(str(git_repo_with_branch))
        changed = git.list_changed_files("main")
        assert "feature.txt" in changed

    def test_get_diff_with_branch_name(self, git_repo_with_branch):
        git = GitIntegration(str(git_repo_with_branch))
        diff = git.get_diff("main")
        assert "feature.txt" in diff


@requires_git
class TestGitIntegrationEmptyResults:
    """変更なし / 空リスト になるケース"""

    def test_list_changed_files_returns_empty_when_no_diff(self, git_repo_single_commit):
        """HEAD...HEAD には差分がない -> 空リスト"""
        git = GitIntegration(str(git_repo_single_commit))
        changed = git.list_changed_files("HEAD")
        assert changed == []

    def test_list_changed_files_returns_list_type(self, git_repo_single_commit):
        """戻り値の型は必ず list"""
        git = GitIntegration(str(git_repo_single_commit))
        result = git.list_changed_files("HEAD")
        assert isinstance(result, list)

    def test_get_diff_returns_empty_string_when_no_diff(self, git_repo_single_commit):
        git = GitIntegration(str(git_repo_single_commit))
        diff = git.get_diff("HEAD")
        assert isinstance(diff, str)
        assert diff == ""


@requires_git
class TestGitIntegrationInvalidInputs:
    """不正 ref・存在しないディレクトリ等のエラーパス"""

    def test_invalid_ref_list_changed_raises_error(self, git_repo_with_tag):
        git = GitIntegration(str(git_repo_with_tag))
        with pytest.raises(KasuInvalidGitRefError):
            git.list_changed_files("totally-invalid-ref-abc123xyz")

    def test_invalid_ref_get_diff_raises_error(self, git_repo_with_tag):
        git = GitIntegration(str(git_repo_with_tag))
        with pytest.raises(KasuInvalidGitRefError):
            git.get_diff("totally-invalid-ref-abc123xyz")

    def test_empty_string_ref_raises_invalid_ref_error(self, git_repo_with_tag):
        git = GitIntegration(str(git_repo_with_tag))
        with pytest.raises(KasuInvalidGitRefError):
            git.list_changed_files("")

    def test_non_git_directory_raises_not_a_repo_error(self, tmp_path):
        non_git = tmp_path / "plain_dir"
        non_git.mkdir()
        with pytest.raises(KasuNotAGitRepoError):
            GitIntegration(str(non_git))

    def test_error_message_contains_directory(self, tmp_path):
        non_git = tmp_path / "my_dir"
        non_git.mkdir()
        with pytest.raises(KasuNotAGitRepoError) as exc_info:
            GitIntegration(str(non_git))
        assert "my_dir" in str(exc_info.value) or "git repository" in str(exc_info.value).lower()

    def test_invalid_ref_error_message_contains_ref(self, git_repo_with_tag):
        git = GitIntegration(str(git_repo_with_tag))
        bad_ref = "no-such-branch-xyz"
        with pytest.raises(KasuInvalidGitRefError) as exc_info:
            git.list_changed_files(bad_ref)
        assert bad_ref in str(exc_info.value)


@requires_git
class TestGitIntegrationSubmodule:
    """サブディレクトリ（ネストした git repo）での動作"""

    def test_init_inside_nested_dir_works(self, tmp_path):
        """ネストしたディレクトリでも git repo なら初期化できる"""
        outer = tmp_path / "outer"
        outer.mkdir()
        inner = outer / "sub"
        inner.mkdir()

        _run(["git", "init", "-q", "-b", "main"], cwd=outer)
        _run(["git", "config", "user.email", "test@example.com"], cwd=outer)
        _run(["git", "config", "user.name", "Tester"], cwd=outer)

        (outer / "root.txt").write_text("root\n")
        (inner / "sub.txt").write_text("sub\n")
        _run(["git", "add", "-A"], cwd=outer)
        _run(["git", "commit", "-q", "-m", "init"], cwd=outer)

        (inner / "sub.txt").write_text("sub changed\n")
        _run(["git", "add", "-A"], cwd=outer)
        _run(["git", "commit", "-q", "-m", "change sub"], cwd=outer)

        # outer のリポジトリとして inner ディレクトリを cwd に指定しても動く
        # (--is-inside-work-tree は work tree の中なら true を返す)
        git = GitIntegration(str(inner))
        changed = git.list_changed_files("HEAD~1")
        # inner/sub.txt の相対パスが returned
        assert any("sub.txt" in p for p in changed)
