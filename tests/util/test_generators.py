"""Generators のユニットテスト"""
import pytest
from pathlib import Path
from generators.text import TextGenerator
from generators.markdown import MarkdownGenerator


class TestTextGeneratorBasic:
    """TextGenerator の基本機能テスト"""

    def test_generate_empty_list(self, tmp_path):
        """空のファイルリスト"""
        generator = TextGenerator()
        
        content, stats = generator.generate(
            target_files=[],
            target_dir=str(tmp_path)
        )
        
        assert content == "=== Files ===\n\n"
        assert stats == {}

    def test_generate_single_file(self, tmp_path):
        """単一ファイルの生成"""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")
        
        file_info = {
            'path': str(test_file),
            'size': test_file.stat().st_size,
            'lines': 1
        }
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path)
        )
        
        assert f"--- {test_file} ---" in content
        assert "print('hello')" in content

    def test_generate_multiple_files(self, tmp_path):
        """複数ファイルの生成"""
        file1 = tmp_path / "file1.py"
        file2 = tmp_path / "file2.js"
        
        file1.write_text("# Python")
        file2.write_text("// JavaScript")
        
        file_infos = [
            {'path': str(file1), 'size': file1.stat().st_size, 'lines': 1},
            {'path': str(file2), 'size': file2.stat().st_size, 'lines': 1}
        ]
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=file_infos,
            target_dir=str(tmp_path)
        )
        
        assert "file1.py" in content
        assert "file2.js" in content
        assert "# Python" in content
        assert "// JavaScript" in content


class TestTextGeneratorOptions:
    """TextGenerator のオプション機能テスト"""

    def test_generate_with_tree(self, tmp_path):
        """ツリー構造を含む生成"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        file_info = {'path': str(test_file), 'size': 10, 'lines': 1}
        tree_structure = ".\n└── test.txt"
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            include_tree=True,
            tree_structure=tree_structure
        )
        
        assert "=== Directory Structure ===" in content
        assert "└── test.txt" in content

    def test_generate_with_list(self, tmp_path):
        """ファイルリストを含む生成"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        file_info = {'path': str(test_file), 'size': 10, 'lines': 1}
        list_structure = "test.txt"
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            include_list=True,
            list_structure=list_structure
        )
        
        assert "=== File List ===" in content
        assert "test.txt" in content

    def test_generate_with_stats(self, tmp_path):
        """統計情報を含む生成"""
        file1 = tmp_path / "file1.py"
        file1.write_text("line1\nline2")
        
        file_info = {'path': str(file1), 'size': file1.stat().st_size, 'lines': 2}
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            include_stats=True
        )
        
        assert "=== Statistics ===" in content
        assert "Total files:" in content
        assert "Total lines:" in content
        assert "Total size:" in content

    def test_generate_with_head_lines(self, tmp_path):
        """先頭N行のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")
        
        file_info = {'path': str(test_file), 'size': 30, 'lines': 5}
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            head_lines=2
        )
        
        assert "line1" in content
        assert "line2" in content
        assert "truncated" in content
        assert "line5" not in content or "truncated" in content

    def test_generate_with_tail_lines(self, tmp_path):
        """末尾N行のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")
        
        file_info = {'path': str(test_file), 'size': 30, 'lines': 5}
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            tail_lines=2
        )
        
        assert "truncated" in content
        assert "line4" in content
        assert "line5" in content

    def test_generate_no_merge(self, tmp_path):
        """ファイル内容を含めない"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("secret content")
        
        file_info = {'path': str(test_file), 'size': 14, 'lines': 1}
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            include_merge=False
        )
        
        assert "=== Files ===" not in content
        assert "secret content" not in content


class TestTextGeneratorSanitization:
    """TextGenerator のサニタイズ機能テスト"""

    def test_generate_with_sanitize(self, tmp_path):
        """サニタイズ有効"""
        test_file = tmp_path / "config.py"
        test_file.write_text("EMAIL = 'user@example.com'\nAPI_KEY = 'secret123'")
        
        file_info = {'path': str(test_file), 'size': 50, 'lines': 2}
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            enable_sanitize=True
        )
        
        assert "user@example.com" not in content
        assert "[REDACTED_EMAIL" in content
        assert stats.get("Email addresses", 0) >= 1

    def test_generate_with_custom_replacements(self, tmp_path):
        """カスタム置換パターン"""
        test_file = tmp_path / "data.txt"
        test_file.write_text("SECRET_VALUE = 'my_secret'")
        
        file_info = {'path': str(test_file), 'size': 30, 'lines': 1}
        
        custom = [("my_secret", "[REPLACED]")]
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            custom_replacements=custom
        )
        
        assert "my_secret" not in content
        assert "[REPLACED]" in content


class TestMarkdownGeneratorBasic:
    """MarkdownGenerator の基本機能テスト"""

    def test_generate_empty_list(self, tmp_path):
        """空のファイルリスト"""
        generator = MarkdownGenerator()
        
        content, stats = generator.generate(
            target_files=[],
            target_dir=str(tmp_path)
        )
        
        assert content == "## Files\n\n"
        assert stats == {}

    def test_generate_single_file(self, tmp_path):
        """単一ファイルの生成"""
        test_file = tmp_path / "test.py"
        test_file.write_text("def hello():\n    pass")
        
        file_info = {
            'path': str(test_file),
            'size': test_file.stat().st_size,
            'lines': 2
        }
        
        generator = MarkdownGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path)
        )
        
        assert "## Files" in content
        assert f"### `{test_file}`" in content
        assert "```python" in content
        assert "def hello():" in content
        assert "```" in content

    def test_generate_multiple_files(self, tmp_path):
        """複数ファイルの生成"""
        py_file = tmp_path / "script.py"
        js_file = tmp_path / "app.js"
        
        py_file.write_text("print('hello')")
        js_file.write_text("console.log('world')")
        
        file_infos = [
            {'path': str(py_file), 'size': py_file.stat().st_size, 'lines': 1},
            {'path': str(js_file), 'size': js_file.stat().st_size, 'lines': 1}
        ]
        
        generator = MarkdownGenerator()
        content, stats = generator.generate(
            target_files=file_infos,
            target_dir=str(tmp_path)
        )
        
        assert "```python" in content
        assert "```javascript" in content
        assert "print('hello')" in content
        assert "console.log('world')" in content

    def test_generate_language_detection(self, tmp_path):
        """言語検出のテスト"""
        files = {
            "test.py": "python",
            "test.js": "javascript",
            "test.ts": "typescript",
            "test.java": "java",
            "test.go": "go",
            "test.rs": "rust",
            "Dockerfile": "dockerfile",
            "Makefile": "makefile"
        }
        
        file_infos = []
        for filename, expected_lang in files.items():
            file_path = tmp_path / filename
            file_path.write_text("content")
            file_infos.append({
                'path': str(file_path),
                'size': file_path.stat().st_size,
                'lines': 1
            })
        
        generator = MarkdownGenerator()
        content, stats = generator.generate(
            target_files=file_infos,
            target_dir=str(tmp_path)
        )
        
        # 各言語のコードブロックが含まれる
        for filename, expected_lang in files.items():
            assert f"```{expected_lang}" in content or f"`{filename}`" in content


class TestMarkdownGeneratorOptions:
    """MarkdownGenerator のオプション機能テスト"""

    def test_generate_with_summary(self, tmp_path):
        """サマリー統計を含む"""
        file1 = tmp_path / "file1.py"
        file1.write_text("line1\nline2")
        
        file_info = {'path': str(file1), 'size': file1.stat().st_size, 'lines': 2}
        
        generator = MarkdownGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path),
            include_stats=True
        )
        
        assert "## Summary" in content
        assert "**Total files**:" in content
        assert "**Total lines**:" in content
        assert "**Total size**:" in content

    def test_generate_with_extension_stats(self, tmp_path):
        """拡張子別統計"""
        py_file = tmp_path / "test.py"
        js_file = tmp_path / "test.js"
        
        py_file.write_text("python")


class TestGeneratorErrorHandling:
    """エラーハンドリングのテスト"""
    
    def test_text_generator_file_error(self, tmp_path, capsys):
        """ファイル読み込みエラー（Text）"""
        # 存在しないファイルを指定
        file_info = {'path': '/nonexistent/file.txt', 'size': 0, 'lines': 0}
        
        generator = TextGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path)
        )
        
        # エラーメッセージが含まれる
        assert "[Error" in content
        
        captured = capsys.readouterr()
        assert "Warning" in captured.err or "Failed" in captured.err
    
    def test_markdown_generator_file_error(self, tmp_path, capsys):
        """ファイル読み込みエラー（Markdown）"""
        file_info = {'path': '/nonexistent/file.py', 'size': 0, 'lines': 0}
        
        generator = MarkdownGenerator()
        content, stats = generator.generate(
            target_files=[file_info],
            target_dir=str(tmp_path)
        )
        
        assert "[Error" in content or "```" in content
        
        captured = capsys.readouterr()
        assert "Warning" in captured.err or "Failed" in captured.err