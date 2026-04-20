"""Git 連携（subprocess による git コマンド実行）

See: docs/adr/0002-git-integration-strategy.md
"""
import shutil
import subprocess
from typing import List

from utils.exceptions import (
    KasuGitNotFoundError,
    KasuInvalidGitRefError,
    KasuNotAGitRepoError,
)


class GitIntegration:
    """``git`` コマンドを subprocess 経由で呼び出すラッパ

    本クラスはインスタンス化された時点で ``git`` コマンドの存在と、
    ``target_dir`` が git リポジトリであることを検証する。
    検証に失敗すると ``KasuGitNotFoundError`` または
    ``KasuNotAGitRepoError`` を送出する。
    """

    def __init__(self, target_dir: str) -> None:
        """GitIntegration を初期化

        Args:
            target_dir: git リポジトリとして扱うディレクトリ。

        Raises:
            KasuGitNotFoundError: ``git`` コマンドが PATH に無い場合。
            KasuNotAGitRepoError: ``target_dir`` が git リポジトリでない場合。
        """
        self._target_dir = target_dir
        self._ensure_git_available()
        self._ensure_is_git_repo()

    def list_changed_files(self, ref: str) -> List[str]:
        """``git diff --name-only <ref>...HEAD`` の結果を返す

        Args:
            ref: 比較元の git ref。

        Returns:
            変更ファイルの相対パスリスト。

        Raises:
            KasuInvalidGitRefError: ``ref`` が解決できない場合。
        """
        self._ensure_ref_valid(ref)
        # ``--`` セパレータで後続をファイルパス扱いにし、ref が偽装された
        # オプションフラグとして解釈されないようにする（argument injection 対策）
        result = self._run(
            ["git", "diff", "--name-only", f"{ref}...HEAD", "--"],
        )
        return [line for line in result.stdout.splitlines() if line.strip()]

    def get_diff(self, ref: str) -> str:
        """``git diff <ref>...HEAD`` の生出力を返す

        Args:
            ref: 比較元の git ref。

        Returns:
            diff の標準出力。``--no-color`` 指定でパース想定の文字列。

        Raises:
            KasuInvalidGitRefError: ``ref`` が解決できない場合。
        """
        self._ensure_ref_valid(ref)
        result = self._run(
            ["git", "--no-pager", "diff", "--no-color", f"{ref}...HEAD", "--"],
        )
        return result.stdout

    def _ensure_git_available(self) -> None:
        if shutil.which("git") is None:
            raise KasuGitNotFoundError(
                "git command not found in PATH. Install git or remove --since/--diff."
            )

    def _ensure_is_git_repo(self) -> None:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self._target_dir,
                capture_output=True,
                text=True,
                check=False,
                shell=False,
            )
        except FileNotFoundError as e:
            raise KasuGitNotFoundError(str(e)) from e
        if result.returncode != 0 or result.stdout.strip() != "true":
            raise KasuNotAGitRepoError(
                f"Not a git repository: {self._target_dir}"
            )

    def _ensure_ref_valid(self, ref: str) -> None:
        # ``-`` 始まりの ref は git のオプションフラグとして解釈される
        # 余地があるため、rev-parse に渡す前に拒否する
        if not ref or ref.startswith("-"):
            raise KasuInvalidGitRefError(f"Invalid git ref: {ref!r}")
        result = subprocess.run(
            ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
            cwd=self._target_dir,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
        if result.returncode != 0:
            raise KasuInvalidGitRefError(
                f"Invalid git ref: {ref!r} ({result.stderr.strip()})"
            )

    def _run(self, args: List[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            args,
            cwd=self._target_dir,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
