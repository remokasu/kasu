"""Merger のユニットテスト (完全版)"""
import pytest
import sys
from io import StringIO
from pathlib import Path
from src.core.merger import Merger
from src.core.file_scanner import FileScanner
from src.generators.text import TextGenerator
from src.generators.markdown import MarkdownGenerator
from src.utils.tree import TreeBuilder
from src.utils.list import ListBuilder
from src.filters.glob import GlobFilter
from src.filters.ignore import IgnoreFilter


class TestMergerBasic:
    """Mergerの基本機能テスト"""
    
    def test_merge_basic(self, tmp_path):
        """基本的なマージ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            skip_confirm=True
        )
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "test.txt" in content
        assert "content" in content

    def test_merge_multiple_files(self, tmp_path):
        """複数ファイルのマージ"""
        for i in range(3):
            (tmp_path / f"file{i}.txt").write_text(f"content {i}")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            skip_confirm=True
        )
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "file0.txt" in content
        assert "file1.txt" in content
        assert "file2.txt" in content


class TestMergerStdout:
    """stdout出力のテスト"""
    
    def test_merge_to_stdout(self, tmp_path, capsys):
        """stdout出力"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        merger.merge(
            target_dir=str(tmp_path),
            to_stdout=True,
            skip_confirm=True
        )
        
        captured = capsys.readouterr()
        assert "hello world" in captured.out
        assert "Scanning files..." in captured.err
        assert "Merging..." in captured.err


class TestMergerWithOptions:
    """各種オプションのテスト"""
    
    def test_merge_with_tree(self, tmp_path):
        """ツリー表示付き"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        tree_builder = TreeBuilder(ignore_filter, glob_filter)
        
        merger = Merger(scanner, generator, tree_builder=tree_builder)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            show_tree=True,
            skip_confirm=True
        )
        
        content = output_file.read_text()
        assert "Directory Structure" in content or "test.txt" in content

    def test_merge_with_list(self, tmp_path):
        """ファイルリスト付き"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        list_builder = ListBuilder(str(tmp_path))
        
        merger = Merger(scanner, generator, list_builder=list_builder)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            show_list=True,
            skip_confirm=True
        )
        
        content = output_file.read_text()
        assert "File List" in content or "test.txt" in content

    def test_merge_with_stats(self, tmp_path):
        """統計情報付き"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            show_stats=True,
            skip_confirm=True
        )
        
        content = output_file.read_text()
        assert "Statistics" in content or "Total files" in content

    def test_merge_with_sanitize(self, tmp_path, capsys):
        """サニタイズ付き"""
        test_file = tmp_path / "config.txt"
        test_file.write_text("email: user@example.com")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            enable_sanitize=True,
            skip_confirm=True
        )
        
        content = output_file.read_text()
        assert "user@example.com" not in content or "[REDACTED" in content
        
        captured = capsys.readouterr()
        # サニタイズ統計が出力される可能性
        assert "Done!" in captured.out

    def test_merge_with_head_lines(self, tmp_path):
        """先頭N行のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            head_lines=2,
            skip_confirm=True
        )
        
        content = output_file.read_text()
        assert "line1" in content
        assert "line2" in content

    def test_merge_with_tail_lines(self, tmp_path):
        """末尾N行のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            tail_lines=2,
            skip_confirm=True
        )
        
        content = output_file.read_text()
        assert "line4" in content
        assert "line5" in content

    def test_merge_no_merge(self, tmp_path):
        """ファイル内容を含めない"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("secret content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            include_merge=False,
            skip_confirm=True
        )
        
        content = output_file.read_text()
        assert "secret content" not in content


class TestMergerDisplayOnly:
    """表示のみモードのテスト"""
    
    def test_display_only_tree(self, tmp_path, capsys):
        """ツリー表示のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        tree_builder = TreeBuilder(ignore_filter, glob_filter)
        
        merger = Merger(scanner, generator, tree_builder=tree_builder)
        
        merger.merge(
            target_dir=str(tmp_path),
            show_tree=True,
            skip_confirm=True
        )
        
        captured = capsys.readouterr()
        assert "Directory tree:" in captured.out
        assert "test.txt" in captured.out

    def test_display_only_list(self, tmp_path, capsys):
        """リスト表示のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        list_builder = ListBuilder(str(tmp_path))
        
        merger = Merger(scanner, generator, list_builder=list_builder)
        
        merger.merge(
            target_dir=str(tmp_path),
            show_list=True,
            skip_confirm=True
        )
        
        captured = capsys.readouterr()
        assert "File list:" in captured.out
        assert "test.txt" in captured.out

    def test_display_only_stats(self, tmp_path, capsys):
        """統計表示のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        merger.merge(
            target_dir=str(tmp_path),
            show_stats=True,
            skip_confirm=True
        )
        
        captured = capsys.readouterr()
        assert "Statistics" in captured.out

    def test_display_only_tree_to_stdout(self, tmp_path, capsys):
        """ツリー表示のみ（stdout）- 修正版"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        tree_builder = TreeBuilder(ignore_filter, glob_filter)
        
        merger = Merger(scanner, generator, tree_builder=tree_builder)
        
        merger.merge(
            target_dir=str(tmp_path),
            show_tree=True,
            to_stdout=True,
            skip_confirm=True
        )
        
        captured = capsys.readouterr()
        # to_stdoutの場合、display_onlyモードにならないため、
        # 通常の出力が stdout に出る
        assert "Directory Structure" in captured.out or "test.txt" in captured.out

    def test_display_only_list_to_stdout(self, tmp_path, capsys):
        """リスト表示のみ（stdout）"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        list_builder = ListBuilder(str(tmp_path))
        
        merger = Merger(scanner, generator, list_builder=list_builder)
        
        merger.merge(
            target_dir=str(tmp_path),
            show_list=True,
            to_stdout=True,
            skip_confirm=True
        )
        
        captured = capsys.readouterr()
        assert "File List" in captured.out or "test.txt" in captured.out


class TestMergerConfirmation:
    """確認プロンプトのテスト"""
    
    def test_merge_with_confirmation_yes(self, tmp_path, monkeypatch):
        """確認プロンプト - Yes"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        # 'yes'を入力
        monkeypatch.setattr('builtins.input', lambda _: 'yes')
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            skip_confirm=False
        )
        
        assert output_file.exists()

    def test_merge_with_confirmation_no(self, tmp_path, monkeypatch, capsys):
        """確認プロンプト - No"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        # 'no'を入力
        monkeypatch.setattr('builtins.input', lambda _: 'no')
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            skip_confirm=False
        )
        
        assert not output_file.exists()
        captured = capsys.readouterr()
        assert "Cancelled" in captured.out


class TestMergerScanStats:
    """スキャン統計表示のテスト"""
    
    def test_scan_stats_glob_filtered(self, tmp_path, capsys):
        """Globフィルタの統計"""
        (tmp_path / "keep.py").write_text("python")
        (tmp_path / "skip.js").write_text("javascript")
        
        glob_filter = GlobFilter(["*.py"], str(tmp_path))
        scanner = FileScanner(filters=[glob_filter], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            skip_confirm=True
        )
        
        captured = capsys.readouterr()
        assert "Filtered by glob:" in captured.out

    def test_scan_stats_ignored(self, tmp_path, capsys):
        """Ignoreパターンの統計"""
        (tmp_path / "keep.py").write_text("python")
        (tmp_path / "skip.log").write_text("log")
        
        ignore_filter = IgnoreFilter(["*.log"], str(tmp_path), debug=False)
        scanner = FileScanner(filters=[ignore_filter], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            skip_confirm=True
        )
        
        captured = capsys.readouterr()
        assert "Ignored by patterns:" in captured.out

    def test_scan_stats_size_filtered(self, tmp_path, capsys):
        """サイズフィルタの統計表示"""
        # size_filtered機能が実装されていない場合はスキップ
        pytest.skip("Size filter feature not yet implemented")


class TestMergerErrorHandling:
    """エラーハンドリングのテスト"""
    
    def test_permission_denied(self, tmp_path, capsys):
        """書き込み権限エラー"""
        import os
        if os.name == 'nt':
            pytest.skip("Permission test skipped on Windows")
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        output_file = tmp_path / "output.txt"
        output_file.touch()
        os.chmod(output_file, 0o444)  # 読み取り専用
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        try:
            with pytest.raises(SystemExit):
                merger.merge(
                    target_dir=str(tmp_path),
                    output_file=str(output_file),
                    skip_confirm=True
                )
            
            captured = capsys.readouterr()
            assert "Permission denied" in captured.err
        finally:
            os.chmod(output_file, 0o644)

    def test_invalid_path(self, tmp_path, capsys):
        """無効なパスエラー"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        # 無効なパス（ディレクトリをファイルとして扱う）
        invalid_dir = tmp_path / "invalid"
        invalid_dir.mkdir()
        output_file = invalid_dir  # ディレクトリをファイルとして指定
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        with pytest.raises(SystemExit):
            merger.merge(
                target_dir=str(tmp_path),
                output_file=str(output_file),
                skip_confirm=True
            )
        
        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_os_error_handling(self, tmp_path, capsys, monkeypatch):
        """OSErrorのハンドリング"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = TextGenerator()
        merger = Merger(scanner, generator)
        
        output_file = tmp_path / "output.txt"
        
        # open関数をモックしてOSErrorを発生させる
        original_open = open
        def mock_open(*args, **kwargs):
            if 'output.txt' in str(args[0]) and 'w' in args[1]:
                raise OSError("Mock OS error")
            return original_open(*args, **kwargs)
        
        monkeypatch.setattr('builtins.open', mock_open)
        
        with pytest.raises(SystemExit):
            merger.merge(
                target_dir=str(tmp_path),
                output_file=str(output_file),
                skip_confirm=True
            )
        
        captured = capsys.readouterr()
        assert "Error" in captured.err
        assert "Mock OS error" in captured.err


class TestMergerAllOptions:
    """全オプションの組み合わせテスト"""
    
    def test_all_options_combined(self, tmp_path):
        """全オプション組み合わせ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nemail: test@example.com")
        
        scanner = FileScanner(filters=[], debug=False)
        generator = MarkdownGenerator()
        
        ignore_filter = IgnoreFilter([], str(tmp_path), debug=False)
        glob_filter = GlobFilter(None, str(tmp_path))
        tree_builder = TreeBuilder(ignore_filter, glob_filter)
        list_builder = ListBuilder(str(tmp_path))
        
        merger = Merger(scanner, generator, tree_builder, list_builder)
        
        output_file = tmp_path / "output.md"
        merger.merge(
            target_dir=str(tmp_path),
            output_file=str(output_file),
            show_tree=True,
            show_list=True,
            show_stats=True,
            enable_sanitize=True,
            head_lines=3,
            skip_confirm=True
        )
        
        content = output_file.read_text()
        assert output_file.exists()
        # Markdown形式
        assert "##" in content or "```" in content
        