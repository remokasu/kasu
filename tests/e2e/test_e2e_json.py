"""E2E: ``--format json`` の CLI 動作 + JSON Schema 契約テスト"""
import json
from pathlib import Path

import pytest


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "kasu_output_schema.json"


@pytest.fixture
def schema():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


class TestFormatJson:
    def test_stdout_json_is_parseable(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("print('a')\n")
        (tmp_path / "b.md").write_text("# b\n")

        result = run_cli(["-i", ".", "--stdout", "-f", "json"], cwd=tmp_path)
        assert result.returncode == 0, result.stderr

        data = json.loads(result.stdout)
        assert data["meta"]["schema_version"] == "1.0"
        assert data["meta"]["total_files"] == 2
        paths = {f["path"] for f in data["files"]}
        assert paths == {"a.py", "b.md"}

    def test_file_output_json_is_parseable(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("print('a')\n")
        out = tmp_path / "out.json"

        result = run_cli(
            ["-i", ".", "-o", str(out), "-f", "json", "-y"],
            cwd=tmp_path,
        )
        assert result.returncode == 0, result.stderr
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["meta"]["schema_version"] == "1.0"

    def test_output_passes_jsonschema(self, tmp_path, run_cli, schema):
        jsonschema = pytest.importorskip("jsonschema")
        (tmp_path / "a.py").write_text("print('a')\n")
        (tmp_path / "b.md").write_text("# b\n")

        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--token-count"],
            cwd=tmp_path,
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        jsonschema.validate(instance=data, schema=schema)

    def test_absolute_paths_option(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("x\n")

        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--absolute-paths"],
            cwd=tmp_path,
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        # absolute_path は常に絶対パス、path は absolute_paths フラグに関係なく相対
        for f in data["files"]:
            assert f["absolute_path"].startswith("/")

    def test_max_bytes_truncates_and_flags_meta(self, tmp_path, run_cli):
        (tmp_path / "big.txt").write_text("a" * 10_000)
        (tmp_path / "other.txt").write_text("b" * 10_000)

        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--max-bytes", "1000"],
            cwd=tmp_path,
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        assert data["meta"]["truncated"] is True
        assert data["meta"]["truncate_reason"] == "max_bytes"
        assert "Output truncated" in result.stderr


class TestBackwardCompatText:
    """既存 text/markdown 出力が破壊されていないことを smoke test"""

    def test_text_output_still_works(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("print('a')\n")
        out = tmp_path / "out.txt"
        result = run_cli(
            ["-i", ".", "-o", str(out), "-f", "text", "-y"], cwd=tmp_path
        )
        assert result.returncode == 0, result.stderr
        content = out.read_text()
        # 既存ヘッダ
        assert "=== Files ===" in content
        assert "a.py" in content
        assert "print('a')" in content

    def test_markdown_output_still_works(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("print('a')\n")
        out = tmp_path / "out.md"
        result = run_cli(
            ["-i", ".", "-o", str(out), "-f", "markdown", "-y"], cwd=tmp_path
        )
        assert result.returncode == 0, result.stderr
        content = out.read_text()
        assert "a.py" in content
        assert "```" in content
