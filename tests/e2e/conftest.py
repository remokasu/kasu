"""E2E テスト共通ヘルパ

``PYTHONPATH`` を src/ に向けた状態で CLI を叩く fixture を提供する。
これにより実装中の最新コードでも e2e テストが走る（installed 版の
``ks`` には依存しない）。
"""
import os
import subprocess
import sys

import pytest


_SRC = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "src")
)


@pytest.fixture
def run_cli():
    """CLI を subprocess で呼ぶ fixture

    Usage::

        result = run_cli(["-i", ".", "-o", str(out), "-y"], cwd=tmp_path)
        assert result.returncode == 0
    """
    def _run(args, cwd=None, check=False):
        env = os.environ.copy()
        env["PYTHONPATH"] = _SRC + os.pathsep + env.get("PYTHONPATH", "")
        cmd = [
            sys.executable,
            "-c",
            "from kasu.cli import main; main()",
            *args,
        ]
        return subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            env=env,
            check=check,
        )

    return _run
