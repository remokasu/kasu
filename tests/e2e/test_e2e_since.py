"""E2E: ``--since`` / ``--diff`` の CLI 動作"""
import json
import shutil
import subprocess

import pytest


_GIT_AVAILABLE = shutil.which("git") is not None
requires_git = pytest.mark.skipif(not _GIT_AVAILABLE, reason="git not in PATH")


def _git(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


@pytest.fixture
def git_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(["git", "init", "-q", "-b", "main"], cwd=repo)
    _git(["git", "config", "user.email", "t@example.com"], cwd=repo)
    _git(["git", "config", "user.name", "Tester"], cwd=repo)

    (repo / "keep.txt").write_text("keep\n")
    (repo / "a.py").write_text("print('v1')\n")
    _git(["git", "add", "-A"], cwd=repo)
    _git(["git", "commit", "-q", "-m", "first"], cwd=repo)

    (repo / "a.py").write_text("print('v2')\n")
    (repo / "b.md").write_text("# added\n")
    _git(["git", "add", "-A"], cwd=repo)
    _git(["git", "commit", "-q", "-m", "second"], cwd=repo)

    return repo


@requires_git
class TestSince:
    def test_since_filters_to_changed_files(self, git_repo, run_cli):
        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--since", "HEAD~1"],
            cwd=git_repo,
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        paths = {f["path"] for f in data["files"]}
        assert paths == {"a.py", "b.md"}

    def test_since_invalid_ref_exits_2(self, git_repo, run_cli):
        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--since", "nonexistent-ref-xyz"],
            cwd=git_repo,
        )
        assert result.returncode == 2
        assert "Invalid git ref" in result.stderr

    def test_since_on_non_git_dir_exits_2(self, tmp_path, run_cli):
        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--since", "HEAD"],
            cwd=tmp_path,
        )
        assert result.returncode == 2
        assert "Not a git repository" in result.stderr


@requires_git
class TestDiff:
    def test_diff_emits_diff_section_in_json(self, git_repo, run_cli):
        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--diff", "HEAD~1"],
            cwd=git_repo,
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        assert data["diff"] is not None
        assert "v2" in data["diff"]
        assert "b.md" in data["diff"]

    def test_diff_emits_section_in_markdown(self, git_repo, run_cli):
        out = git_repo / "out.md"
        result = run_cli(
            ["-i", ".", "-o", str(out), "-f", "markdown", "--diff", "HEAD~1", "-y"],
            cwd=git_repo,
        )
        assert result.returncode == 0, result.stderr
        content = out.read_text()
        assert "diff" in content.lower()
        assert "v2" in content
