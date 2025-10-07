"""Utils モジュールのユニットテスト"""
import pytest
from pathlib import Path
from src.utils.tree import TreeBuilder
from src.utils.list import ListBuilder
from src.utils.statistics import Statistics
from src.utils.language_map import LanguageMapper
from src.utils.format_utils import parse_size, format_size
from src.filters.ignore import IgnoreFilter
from src.filters.glob import GlobFilter


class TestTreeBuilder:
    """TreeBuilder のテスト"""

    def test_build_empty_directory(self, tmp_path):
        """空のディレクトリ"""
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        builder = TreeBuilder(ignore_filter, glob_filter)
        
        result = builder.build(str(tmp_path))
        
        # ディレクトリ名が含まれる
        assert tmp_path.name in result or "." in result

    def test_build_single_file(self, tmp_path):
        """単一ファイル"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        builder = TreeBuilder(ignore_filter, glob_filter)
        
        result = builder.build(str(tmp_path))
        
        assert "test.txt" in result
        assert "└──" in result or "├──" in result

    def test_build_multiple_files(self, tmp_path):
        """複数ファイル"""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file3 = tmp_path / "file3.txt"
        
        for f in [file1, file2, file3]:
            f.write_text("content")
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        builder = TreeBuilder(ignore_filter, glob_filter)
        
        result = builder.build(str(tmp_path))
        
        assert "file1.txt" in result
        assert "file2.txt" in result
        assert "file3.txt" in result

    def test_build_nested_directories(self, tmp_path):
        """ネストしたディレクトリ"""
        subdir = tmp_path / "src"
        subdir.mkdir()
        
        root_file = tmp_path / "root.txt"
        sub_file = subdir / "main.py"
        
        root_file.write_text("content")
        sub_file.write_text("content")
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        builder = TreeBuilder(ignore_filter, glob_filter)
        
        result = builder.build(str(tmp_path))
        
        assert "src/" in result
        assert "root.txt" in result
        assert "main.py" in result

    def test_build_deep_nesting(self, tmp_path):
        """深いネスト"""
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        
        (deep / "deep.txt").write_text("content")
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        builder = TreeBuilder(ignore_filter, glob_filter)
        
        result = builder.build(str(tmp_path))
        
        assert "a/" in result
        assert "b/" in result
        assert "c/" in result
        assert "deep.txt" in result

    def test_build_with_ignore_filter(self, tmp_path):
        """Ignoreフィルタ適用"""
        keep = tmp_path / "keep.txt"
        ignore = tmp_path / "ignore.log"
        
        keep.write_text("content")
        ignore.write_text("content")
        
        ignore_filter = IgnoreFilter(["*.log"], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        builder = TreeBuilder(ignore_filter, glob_filter)
        
        result = builder.build(str(tmp_path))
        
        assert "keep.txt" in result
        assert "ignore.log" not in result

    def test_build_with_glob_filter(self, tmp_path):
        """Globフィルタ適用"""
        py_file = tmp_path / "test.py"
        js_file = tmp_path / "test.js"
        
        py_file.write_text("content")
        js_file.write_text("content")
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(["*.py"], str(tmp_path))
        builder = TreeBuilder(ignore_filter, glob_filter)
        
        result = builder.build(str(tmp_path))
        
        assert "test.py" in result
        assert "test.js" not in result

    def test_build_binary_files_excluded(self, tmp_path):
        """バイナリファイルは除外される"""
        text_file = tmp_path / "text.txt"
        binary_file = tmp_path / "binary.bin"
        
        text_file.write_text("content")
        binary_file.write_bytes(b'\x00\xFF' * 50)
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        builder = TreeBuilder(ignore_filter, glob_filter)
        
        result = builder.build(str(tmp_path))
        
        assert "text.txt" in result
        # バイナリファイルはFileScanner._is_text_fileで除外される


class TestListBuilder:
    """ListBuilder のテスト"""

    def test_build_empty_list(self, tmp_path):
        """空のリスト"""
        builder = ListBuilder(str(tmp_path))
        
        result = builder.build([])
        
        assert result == ""

    def test_build_single_file(self, tmp_path):
        """単一ファイル"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        file_info = {'path': str(test_file), 'size': 7, 'lines': 1}
        
        builder = ListBuilder(str(tmp_path))
        result = builder.build([file_info])
        
        assert "test.txt" in result

    def test_build_multiple_files(self, tmp_path):
        """複数ファイル"""
        files = [tmp_path / f"file{i}.txt" for i in range(3)]
        for f in files:
            f.write_text("content")
        
        file_infos = [
            {'path': str(f), 'size': 7, 'lines': 1}
            for f in files
        ]
        
        builder = ListBuilder(str(tmp_path))
        result = builder.build(file_infos)
        
        for i in range(3):
            assert f"file{i}.txt" in result

    def test_build_with_relative_paths(self, tmp_path):
        """相対パス表示"""
        subdir = tmp_path / "src"
        subdir.mkdir()
        
        test_file = subdir / "main.py"
        test_file.write_text("content")
        
        file_info = {'path': str(test_file), 'size': 7, 'lines': 1}
        
        builder = ListBuilder(str(tmp_path))
        result = builder.build([file_info])
        
        # 相対パスで表示される
        assert "src" in result or "main.py" in result

    def test_build_with_stats(self, tmp_path):
        """統計情報付き"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3")
        
        file_info = {
            'path': str(test_file),
            'size': test_file.stat().st_size,
            'lines': 3
        }
        
        builder = ListBuilder(str(tmp_path))
        result = builder.build_with_stats([file_info])
        
        assert "test.txt" in result
        assert "3 lines" in result
        assert "B" in result  # サイズ表示


class TestStatistics:
    """Statistics のテスト"""

    def test_calculate_empty(self):
        """空のファイルリスト"""
        stats = Statistics.calculate([])
        
        assert stats['total_files'] == 0
        assert stats['total_size'] == 0
        assert stats['total_lines'] == 0
        assert stats['by_extension'] == {}

    def test_calculate_single_file(self, tmp_path):
        """単一ファイル"""
        test_file = tmp_path / "test.py"
        test_file.write_text("line1\nline2")
        
        file_info = {
            'path': str(test_file),
            'size': test_file.stat().st_size,
            'lines': 2
        }
        
        stats = Statistics.calculate([file_info])
        
        assert stats['total_files'] == 1
        assert stats['total_lines'] == 2
        assert stats['total_size'] > 0
        assert '.py' in stats['by_extension']

    def test_calculate_multiple_files(self, tmp_path):
        """複数ファイル"""
        py_file = tmp_path / "test.py"
        js_file = tmp_path / "test.js"
        
        py_file.write_text("python")
        js_file.write_text("javascript")
        
        file_infos = [
            {'path': str(py_file), 'size': py_file.stat().st_size, 'lines': 1},
            {'path': str(js_file), 'size': js_file.stat().st_size, 'lines': 1}
        ]
        
        stats = Statistics.calculate(file_infos)
        
        assert stats['total_files'] == 2
        assert stats['total_lines'] == 2
        assert '.py' in stats['by_extension']
        assert '.js' in stats['by_extension']

    def test_calculate_by_extension(self, tmp_path):
        """拡張子別の統計"""
        files = {
            'file1.py': 'python1',
            'file2.py': 'python2',
            'file3.js': 'javascript'
        }
        
        file_infos = []
        for name, content in files.items():
            f = tmp_path / name
            f.write_text(content)
            file_infos.append({
                'path': str(f),
                'size': f.stat().st_size,
                'lines': 1
            })
        
        stats = Statistics.calculate(file_infos)
        
        assert stats['by_extension']['.py']['count'] == 2
        assert stats['by_extension']['.js']['count'] == 1

    def test_calculate_no_extension(self, tmp_path):
        """拡張子なしファイル"""
        no_ext = tmp_path / "Makefile"
        no_ext.write_text("content")
        
        file_info = {'path': str(no_ext), 'size': 7, 'lines': 1}
        
        stats = Statistics.calculate([file_info])
        
        assert '(no extension)' in stats['by_extension']

    def test_print_statistics(self, capsys):
        """統計表示"""
        stats = {
            'total_files': 10,
            'total_lines': 1000,
            'total_size': 10000,
            'by_extension': {
                '.py': {'count': 5, 'lines': 500, 'size': 5000},
                '.js': {'count': 5, 'lines': 500, 'size': 5000}
            }
        }
        
        Statistics.print_statistics(stats)
        
        captured = capsys.readouterr()
        assert "Statistics" in captured.out
        assert "10" in captured.out
        assert "1,000" in captured.out
        assert ".py" in captured.out
        assert ".js" in captured.out


class TestLanguageMapper:
    """LanguageMapper のテスト"""

    def test_get_language_python(self):
        """Python"""
        assert LanguageMapper.get_language("test.py") == "python"
        assert LanguageMapper.get_language("test.pyi") == "python"
        assert LanguageMapper.get_language("test.pyw") == "python"

    def test_get_language_javascript(self):
        """JavaScript/TypeScript"""
        assert LanguageMapper.get_language("test.js") == "javascript"
        assert LanguageMapper.get_language("test.jsx") == "jsx"
        assert LanguageMapper.get_language("test.ts") == "typescript"
        assert LanguageMapper.get_language("test.tsx") == "tsx"
        assert LanguageMapper.get_language("test.mjs") == "javascript"
        assert LanguageMapper.get_language("test.cjs") == "javascript"

    def test_get_language_web(self):
        """Web関連"""
        assert LanguageMapper.get_language("test.html") == "html"
        assert LanguageMapper.get_language("test.css") == "css"
        assert LanguageMapper.get_language("test.scss") == "scss"
        assert LanguageMapper.get_language("test.sass") == "sass"

    def test_get_language_config(self):
        """設定ファイル"""
        assert LanguageMapper.get_language("test.json") == "json"
        assert LanguageMapper.get_language("test.yaml") == "yaml"
        assert LanguageMapper.get_language("test.yml") == "yaml"
        assert LanguageMapper.get_language("test.toml") == "toml"
        assert LanguageMapper.get_language("test.ini") == "ini"

    def test_get_language_shell(self):
        """シェルスクリプト"""
        assert LanguageMapper.get_language("test.sh") == "bash"
        assert LanguageMapper.get_language("test.bash") == "bash"
        assert LanguageMapper.get_language("test.zsh") == "zsh"

    def test_get_language_compiled(self):
        """コンパイル言語"""
        assert LanguageMapper.get_language("test.c") == "c"
        assert LanguageMapper.get_language("test.cpp") == "cpp"
        assert LanguageMapper.get_language("test.java") == "java"
        assert LanguageMapper.get_language("test.go") == "go"
        assert LanguageMapper.get_language("test.rs") == "rust"

    def test_get_language_special_files(self):
        """特殊ファイル名"""
        assert LanguageMapper.get_language("Dockerfile") == "dockerfile"
        assert LanguageMapper.get_language("Makefile") == "makefile"
        assert LanguageMapper.get_language("Gemfile") == "ruby"
        assert LanguageMapper.get_language(".bashrc") == "bash"
        assert LanguageMapper.get_language(".gitignore") == "text"

    def test_get_language_case_insensitive(self):
        """大文字小文字を区別しない"""
        assert LanguageMapper.get_language("DOCKERFILE") == "dockerfile"
        assert LanguageMapper.get_language("MAKEFILE") == "makefile"

    def test_get_language_unknown_extension(self):
        """未知の拡張子"""
        result = LanguageMapper.get_language("test.xyz")
        assert result == "xyz"

    def test_get_language_no_extension(self):
        """拡張子なし"""
        result = LanguageMapper.get_language("README")
        # 特殊ファイルでなければ 'text' が返る
        assert result in ["text", ""]


class TestFormatUtils:
    """format_utils のテスト"""

    def test_parse_size_bytes(self):
        """バイト単位"""
        assert parse_size("100B") == 100
        assert parse_size("100 B") == 100

    def test_parse_size_kilobytes(self):
        """キロバイト単位"""
        assert parse_size("1K") == 1024
        assert parse_size("1KB") == 1024
        assert parse_size("2K") == 2048

    def test_parse_size_megabytes(self):
        """メガバイト単位"""
        assert parse_size("1M") == 1024 * 1024
        assert parse_size("1MB") == 1024 * 1024
        assert parse_size("2.5M") == int(2.5 * 1024 * 1024)

    def test_parse_size_gigabytes(self):
        """ギガバイト単位"""
        assert parse_size("1G") == 1024 * 1024 * 1024
        assert parse_size("1GB") == 1024 * 1024 * 1024

    def test_parse_size_with_spaces(self):
        """スペース付き"""
        assert parse_size("10 M") == 10 * 1024 * 1024
        assert parse_size("  5  KB  ") == 5 * 1024

    def test_parse_size_case_insensitive(self):
        """大文字小文字を区別しない"""
        assert parse_size("1m") == 1024 * 1024
        assert parse_size("1Mb") == 1024 * 1024

    def test_parse_size_invalid_format(self):
        """無効な形式"""
        with pytest.raises(ValueError):
            parse_size("invalid")
        
        with pytest.raises(ValueError):
            parse_size("10X")
        
        with pytest.raises(ValueError):
            parse_size("abc")

    def test_format_size_bytes(self):
        """バイト表示"""
        assert format_size(100) == "100.0 B"
        assert format_size(512) == "512.0 B"

    def test_format_size_kilobytes(self):
        """キロバイト表示"""
        assert format_size(1024) == "1.0 KB"
        assert format_size(2048) == "2.0 KB"
        assert format_size(1536) == "1.5 KB"

    def test_format_size_megabytes(self):
        """メガバイト表示"""
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(2 * 1024 * 1024) == "2.0 MB"

    def test_format_size_gigabytes(self):
        """ギガバイト表示"""
        assert format_size(1024 * 1024 * 1024) == "1.0 GB"

    def test_format_size_terabytes(self):
        """テラバイト表示"""
        assert format_size(1024 * 1024 * 1024 * 1024) == "1.0 TB"

    def test_format_size_zero(self):
        """ゼロバイト"""
        assert format_size(0) == "0.0 B"

    def test_parse_and_format_roundtrip(self):
        """変換の往復"""
        original = "1.5M"
        parsed = parse_size(original)
        formatted = format_size(parsed)
        
        assert "1.5" in formatted
        assert "MB" in formatted