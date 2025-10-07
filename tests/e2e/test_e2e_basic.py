"""E2Eテスト: 基本的なコマンド実行"""
import subprocess
import pytest
from pathlib import Path


class TestBasicCommands:
    """基本的なコマンド実行のテスト"""
    
    def test_basic_merge(self, tmp_path):
        """基本的なマージ: ks . -o output.txt"""
        # テスト用プロジェクト作成
        (tmp_path / "file1.py").write_text("print('hello')")
        (tmp_path / "file2.js").write_text("console.log('world')")
        
        output_file = tmp_path / "output.txt"
        
        # コマンド実行
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        # 検証
        assert result.returncode == 0
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "file1.py" in content
        assert "file2.js" in content
        assert "print('hello')" in content
        assert "console.log('world')" in content
    
    def test_stdout_output(self, tmp_path):
        """stdout出力: ks -i . --stdout"""
        (tmp_path / "test.txt").write_text("test content")
        
        result = subprocess.run(
            ["ks", "-i", ".", "--stdout"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "test.txt" in result.stdout
        assert "test content" in result.stdout
    
    def test_markdown_format(self, tmp_path):
        """Markdown形式: ks -i . -o output.md -f md"""
        (tmp_path / "code.py").write_text("def hello():\n    pass")
        
        output_file = tmp_path / "output.md"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-f", "md", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        content = output_file.read_text()
        
        # Markdown構造を検証
        assert "## Files" in content or "###" in content
        assert "```python" in content
        assert "def hello():" in content
    
    def test_tree_option(self, tmp_path):
        """ツリー表示: ks -i . -o output.txt -t"""
        subdir = tmp_path / "src"
        subdir.mkdir()
        (subdir / "main.py").write_text("pass")
        
        output_file = tmp_path / "output.txt"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-t", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        content = output_file.read_text()
        
        # ツリー構造が含まれるか
        assert "Directory Structure" in content or "├──" in content or "└──" in content


class TestFiltering:
    """フィルタリング機能のテスト"""
    
    def test_glob_filter_single_extension(self, tmp_path):
        """Globフィルタ: ks -i . -g '*.py'"""
        (tmp_path / "keep.py").write_text("# python")
        (tmp_path / "skip.js").write_text("// javascript")
        
        output_file = tmp_path / "output.txt"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-g", "*.py", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        content = output_file.read_text()
        
        assert "keep.py" in content
        assert "skip.js" not in content
    
    def test_glob_filter_multiple_patterns(self, tmp_path):
        """複数パターン: ks -i . -g '*.py' '*.js'"""
        (tmp_path / "file.py").write_text("pass")
        (tmp_path / "file.js").write_text("//")
        (tmp_path / "file.txt").write_text("text")
        
        output_file = tmp_path / "output.txt"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-g", "*.py", "*.js", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        content = output_file.read_text()
        assert "file.py" in content
        assert "file.js" in content
        assert "file.txt" not in content
    
    def test_exclude_pattern(self, tmp_path):
        """除外パターン: ks -i . -x '*.log'"""
        (tmp_path / "code.py").write_text("pass")
        (tmp_path / "debug.log").write_text("log data")
        
        output_file = tmp_path / "output.txt"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-x", "*.log", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        content = output_file.read_text()
        assert "code.py" in content
        assert "debug.log" not in content
    
    def test_gitignore_auto_detect(self, tmp_path):
        """.gitignore自動検出"""
        (tmp_path / ".gitignore").write_text("*.log\ntemp/\n")
        (tmp_path / "keep.py").write_text("pass")
        (tmp_path / "skip.log").write_text("log")
        
        temp_dir = tmp_path / "temp"
        temp_dir.mkdir()
        (temp_dir / "skip.txt").write_text("temp")
        
        output_file = tmp_path / "output.txt"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        content = output_file.read_text()
        assert "keep.py" in content
        assert "skip.log" not in content
        assert "skip.txt" not in content


class TestOptions:
    """各種オプションのテスト"""
    
    def test_head_option(self, tmp_path):
        """先頭N行: ks -i . --head 2"""
        (tmp_path / "file.txt").write_text("line1\nline2\nline3\nline4\nline5")
        
        output_file = tmp_path / "output.txt"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "--head", "2", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        content = output_file.read_text()
        assert "line1" in content
        assert "line2" in content
        assert "line5" not in content or "truncated" in content
    
    def test_tail_option(self, tmp_path):
        """末尾N行: ks -i . --tail 2"""
        (tmp_path / "file.txt").write_text("line1\nline2\nline3\nline4\nline5")
        
        output_file = tmp_path / "output.txt"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "--tail", "2", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        content = output_file.read_text()
        assert "line4" in content
        assert "line5" in content
        assert ("line1" not in content or "truncated" in content)
    
    def test_stats_option(self, tmp_path):
        """統計表示: ks -i . --stats"""
        (tmp_path / "file1.py").write_text("x = 1")
        (tmp_path / "file2.py").write_text("y = 2")
        
        result = subprocess.run(
            ["ks", "-i", ".", "--stats"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Statistics" in result.stdout or "Total files" in result.stdout


class TestErrorCases:
    """エラーケースのテスト"""
    
    def test_nonexistent_directory(self, tmp_path):
        """存在しないディレクトリ"""
        result = subprocess.run(
            ["ks", "-i", str(tmp_path / "nonexistent"), "-o", "output.txt"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "does not exist" in result.stderr.lower()
    
    def test_missing_output_file(self, tmp_path):
        """出力ファイル未指定（-i のみでエラー）"""
        (tmp_path / "test.txt").write_text("data")
        
        result = subprocess.run(
            ["ks", "-i", "."],  # -o も --stdout もない
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        # エラーメッセージに "output" または "required" が含まれることを確認
        stderr_lower = result.stderr.lower()
        assert "output" in stderr_lower or "required" in stderr_lower
    
    def test_head_and_tail_conflict(self, tmp_path):
        """--headと--tailの同時指定"""
        result = subprocess.run(
            ["ks", "-i", ".", "-o", "output.txt", "--head", "10", "--tail", "5"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "cannot use both" in result.stderr.lower()
    
    def test_invalid_glob_pattern(self, tmp_path):
        """無効なGlobパターン（エラーにならず、単にマッチしない）"""
        (tmp_path / "test.txt").write_text("data")
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", "output.txt", "-g", "[invalid", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        # 実装では無効なパターンでもエラーを出さず、マッチしないだけ
        # したがって、正常終了するが0ファイルが処理される
        assert result.returncode == 0
        assert "Found 0 files" in result.stdout or "Filtered by glob" in result.stdout


class TestNestedStructures:
    """ネストしたディレクトリ構造のテスト"""
    
    def test_nested_directories(self, tmp_path):
        """深くネストしたディレクトリ"""
        deep = tmp_path / "a" / "b" / "c" / "d"
        deep.mkdir(parents=True)
        (deep / "deep.py").write_text("# deep file")
        
        output_file = tmp_path / "output.txt"
        
        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        content = output_file.read_text()
        assert "deep.py" in content
    
    def test_recursive_glob(self, tmp_path):
        """再帰的Globパターン: src/**/*.py"""
        src = tmp_path / "src"
        nested = src / "nested"
        nested.mkdir(parents=True)
        
        (src / "main.py").write_text("# main")
        (nested / "util.py").write_text("# util")
        (tmp_path / "root.py").write_text("# root")
        
        output_file = tmp_path / "output.txt"

        result = subprocess.run(
            ["ls", "./src"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        print(result.stdout)

        result = subprocess.run(
            ["ks", "-i", ".", "-o", str(output_file), "-g", "src/**/*.py", "-y"],
            cwd=tmp_path,
            capture_output=True,
            text=True
        )
        
        content = output_file.read_text()
        assert "main.py" in content
        assert "util.py" in content
        assert "root.py" not in content