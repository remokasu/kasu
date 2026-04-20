"""E2E: ``--dry-run`` の CLI 動作"""
import json


class TestDryRun:
    def test_dry_run_json_sets_content_null(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("print('a')\n")
        (tmp_path / "b.md").write_text("# b\n")

        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--dry-run"],
            cwd=tmp_path,
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)

        assert data["meta"]["dry_run"] is True
        assert data["meta"]["total_files"] == 2
        for f in data["files"]:
            assert f["content"] is None
            # size/lines などのメタデータは正しく入る
            assert f["size"] > 0

    def test_dry_run_requires_output_or_stdout(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("x")
        result = run_cli(["-i", ".", "--dry-run"], cwd=tmp_path)
        assert result.returncode != 0
        assert "--dry-run requires" in result.stderr

    def test_dry_run_disables_sanitize_with_info(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("AWS_KEY=AKIA1234567890ABCDEF\n")
        result = run_cli(
            ["-i", ".", "--stdout", "-f", "json", "--dry-run", "--sanitize"],
            cwd=tmp_path,
        )
        assert result.returncode == 0, result.stderr
        assert "sanitize" in result.stderr.lower()

    def test_dry_run_with_text_format_works(self, tmp_path, run_cli):
        (tmp_path / "a.py").write_text("print('a')\n")
        out = tmp_path / "out.txt"
        result = run_cli(
            ["-i", ".", "-o", str(out), "-f", "text", "--dry-run", "-y"],
            cwd=tmp_path,
        )
        assert result.returncode == 0, result.stderr
        # text 形式は content 部分を "skipped" マーカで置き換える or 出さない
        content = out.read_text()
        # dry_run 時は "print('a')" がそのまま入っていてはいけない
        assert "print('a')" not in content
