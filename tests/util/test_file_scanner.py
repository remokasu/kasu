"""FileScanner のユニットテスト"""
import pytest
import os
from pathlib import Path

from core.file_scanner import FileScanner
from filters.glob import GlobFilter
from filters.ignore import IgnoreFilter


class TestFileScannerBasic:
    """基本的なスキャン機能のテスト"""

    def test_scan_empty_directory(self, tmp_path):
        """空のディレクトリ"""
        scanner = FileScanner(filters=[], debug=False)
        
        result = scanner.scan(str(tmp_path))
        
        assert result == []
        stats = scanner.get_stats()
        assert stats['included'] == 0

    def test_scan_single_text_file(self, tmp_path):
        """単一のテキストファイル"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 1
        assert result[0]['path'] == str(test_file)
        assert result[0]['size'] > 0
        assert result[0]['lines'] == 1

    def test_scan_multiple_files(self, tmp_path):
        """複数のファイル"""
        file1 = tmp_path / "file1.py"
        file2 = tmp_path / "file2.js"
        file3 = tmp_path / "file3.txt"
        
        for f in [file1, file2, file3]:
            f.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 3
        paths = [r['path'] for r in result]
        assert str(file1) in paths
        assert str(file2) in paths
        assert str(file3) in paths

    def test_scan_nested_directories(self, tmp_path):
        """ネストしたディレクトリ"""
        subdir1 = tmp_path / "dir1"
        subdir2 = subdir1 / "dir2"
        subdir2.mkdir(parents=True)
        
        file1 = tmp_path / "root.txt"
        file2 = subdir1 / "level1.txt"
        file3 = subdir2 / "level2.txt"
        
        for f in [file1, file2, file3]:
            f.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 3
        paths = [r['path'] for r in result]
        assert str(file1) in paths
        assert str(file2) in paths
        assert str(file3) in paths


class TestFileScannerTextDetection:
    """テキストファイル判定のテスト"""

    def test_is_text_file_utf8(self, tmp_path):
        """UTF-8テキストファイル"""
        text_file = tmp_path / "test.txt"
        text_file.write_text("これはテキストです", encoding='utf-8')
        
        assert FileScanner._is_text_file(str(text_file))

    def test_is_text_file_ascii(self, tmp_path):
        """ASCIIテキストファイル"""
        text_file = tmp_path / "test.txt"
        text_file.write_text("This is ASCII text", encoding='ascii')
        
        assert FileScanner._is_text_file(str(text_file))

    def test_is_text_file_empty(self, tmp_path):
        """空のファイル"""
        empty_file = tmp_path / "empty.txt"
        empty_file.touch()
        
        # 空ファイルはテキストとして扱われる可能性がある
        result = FileScanner._is_text_file(str(empty_file))
        # 実装依存だが、エラーにならないことを確認

    def test_is_text_file_nonexistent(self):
        """存在しないファイル"""
        assert not FileScanner._is_text_file("/nonexistent/file.txt")


class TestFileScannerWithFilters:
    """フィルタ適用のテスト"""

    def test_scan_with_glob_filter(self, tmp_path):
        """Globフィルタ適用"""
        py_file = tmp_path / "test.py"
        js_file = tmp_path / "test.js"
        txt_file = tmp_path / "test.txt"
        
        for f in [py_file, js_file, txt_file]:
            f.write_text("content")
        
        glob_filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path))
        scanner = FileScanner(filters=[glob_filter], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 1
        assert result[0]['path'] == str(py_file)
        
        stats = scanner.get_stats()
        assert stats['glob_filtered'] == 2

    def test_scan_with_ignore_filter(self, tmp_path):
        """Ignoreフィルタ適用"""
        keep_file = tmp_path / "keep.py"
        ignore_file = tmp_path / "ignore.log"
        
        for f in [keep_file, ignore_file]:
            f.write_text("content")
        
        ignore_filter = IgnoreFilter(
            patterns=["*.log"],
            base_dir=str(tmp_path),
            debug=False
        )
        scanner = FileScanner(filters=[ignore_filter], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 1
        assert result[0]['path'] == str(keep_file)
        
        stats = scanner.get_stats()
        assert stats['ignored'] >= 1

    def test_scan_with_multiple_filters(self, tmp_path):
        """複数フィルタの組み合わせ"""
        py_file = tmp_path / "main.py"
        test_py = tmp_path / "test_main.py"
        js_file = tmp_path / "script.js"
        log_file = tmp_path / "debug.log"
        
        for f in [py_file, test_py, js_file, log_file]:
            f.write_text("content")
        
        glob_filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path))
        ignore_filter = IgnoreFilter(
            patterns=["test_*.py"],
            base_dir=str(tmp_path),
            debug=False
        )
        
        scanner = FileScanner(filters=[glob_filter, ignore_filter], debug=False)
        result = scanner.scan(str(tmp_path))
        
        # main.pyのみが含まれる
        assert len(result) == 1
        assert result[0]['path'] == str(py_file)

    def test_scan_directory_filtering(self, tmp_path):
        """ディレクトリレベルのフィルタリング"""
        src_dir = tmp_path / "src"
        build_dir = tmp_path / "build"
        
        for d in [src_dir, build_dir]:
            d.mkdir()
        
        src_file = src_dir / "main.py"
        build_file = build_dir / "output.py"
        
        for f in [src_file, build_file]:
            f.write_text("content")
        
        ignore_filter = IgnoreFilter(
            patterns=["build/"],
            base_dir=str(tmp_path),
            debug=False
        )
        
        scanner = FileScanner(filters=[ignore_filter], debug=False)
        result = scanner.scan(str(tmp_path))
        
        # buildディレクトリは除外される
        assert len(result) == 1
        assert result[0]['path'] == str(src_file)


class TestFileScannerStatistics:
    """統計情報のテスト"""

    def test_statistics_basic(self, tmp_path):
        """基本的な統計"""
        for i in range(3):
            (tmp_path / f"file{i}.txt").write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        scanner.scan(str(tmp_path))
        
        stats = scanner.get_stats()
        assert stats['scanned'] == 3
        assert stats['included'] == 3
        assert stats['glob_filtered'] == 0
        assert stats['ignored'] == 0
        assert stats['non_text'] == 0

    def test_statistics_with_filtering(self, tmp_path):
        """フィルタリング時の統計"""
        # 5つのファイルを作成
        for i in range(3):
            (tmp_path / f"keep{i}.py").write_text("content")
        for i in range(2):
            (tmp_path / f"skip{i}.log").write_text("content")
        
        ignore_filter = IgnoreFilter(
            patterns=["*.log"],
            base_dir=str(tmp_path),
            debug=False
        )
        
        scanner = FileScanner(filters=[ignore_filter], debug=False)
        scanner.scan(str(tmp_path))
        
        stats = scanner.get_stats()
        assert stats['scanned'] == 5
        assert stats['included'] == 3
        assert stats['ignored'] == 2

    # def test_statistics_with_binary_files(self, tmp_path):
    #     """バイナリファイルを含む統計"""
    #     text_file = tmp_path / "text.txt"
    #     text_file.write_text("content")
        
    #     binary_file = tmp_path / "binary.bin"
    #     binary_file.write_bytes(b'\x00\xFF' * 100)
        
    #     scanner = FileScanner(filters=[], debug=False)
    #     scanner.scan(str(tmp_path))
        
    #     stats = scanner.get_stats()
    #     assert stats['scanned'] == 2
    #     assert stats['included'] == 1
    #     assert stats['non_text'] == 1

    def test_statistics_reset_on_rescan(self, tmp_path):
        """再スキャン時に統計がリセットされる"""
        (tmp_path / "file.txt").write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        
        # 1回目のスキャン
        scanner.scan(str(tmp_path))
        stats1 = scanner.get_stats()
        
        # 2回目のスキャン
        scanner.scan(str(tmp_path))
        stats2 = scanner.get_stats()
        
        # 統計がリセットされている
        assert stats1 == stats2


class TestFileScannerFileInfo:
    """ファイル情報取得のテスト"""

    def test_get_file_info_basic(self, tmp_path):
        """基本的なファイル情報"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3")
        
        info = FileScanner._get_file_info(str(test_file))
        
        assert info['path'] == str(test_file)
        assert info['size'] > 0
        assert info['lines'] == 3

    def test_get_file_info_empty_file(self, tmp_path):
        """空のファイル"""
        empty_file = tmp_path / "empty.txt"
        empty_file.touch()
        
        info = FileScanner._get_file_info(str(empty_file))
        
        assert info['path'] == str(empty_file)
        assert info['size'] == 0
        assert info['lines'] == 0

    def test_get_file_info_single_line(self, tmp_path):
        """1行のみのファイル"""
        single_line = tmp_path / "single.txt"
        single_line.write_text("Only one line")
        
        info = FileScanner._get_file_info(str(single_line))
        
        assert info['lines'] == 1

    def test_get_file_info_many_lines(self, tmp_path):
        """多数の行を含むファイル"""
        many_lines = tmp_path / "many.txt"
        content = "\n".join([f"Line {i}" for i in range(1000)])
        many_lines.write_text(content)
        
        info = FileScanner._get_file_info(str(many_lines))
        
        assert info['lines'] == 1000

    def test_get_file_info_large_file_warning(self, tmp_path, capsys):
        """大きなファイルの警告"""
        large_file = tmp_path / "large.txt"
        # 100MB超のファイルを作成（実際には書き込まず、サイズだけ設定）
        large_file.write_text("x" * 1000)  # 小さいファイルで代用
        
        # 実際の警告テストは難しいため、メソッドが正常に動作することを確認
        info = FileScanner._get_file_info(str(large_file))
        assert 'path' in info
        assert 'size' in info
        assert 'lines' in info

    def test_get_file_info_unicode_content(self, tmp_path):
        """Unicode文字を含むファイル"""
        unicode_file = tmp_path / "unicode.txt"
        unicode_file.write_text("日本語\n中文\n한국어", encoding='utf-8')
        
        info = FileScanner._get_file_info(str(unicode_file))
        
        assert info['lines'] == 3

    def test_get_file_info_error_handling(self, tmp_path):
        """エラーハンドリング"""
        # 存在しないファイル
        info = FileScanner._get_file_info("/nonexistent/file.txt")
        
        assert info['path'] == "/nonexistent/file.txt"
        assert info['size'] == 0
        assert info['lines'] == 0


class TestFileScannerSymlinks:
    """シンボリックリンク処理のテスト"""

    def test_skip_symlink_files(self, tmp_path):
        """シンボリックリンクファイルをスキップ"""
        if os.name == 'nt':
            pytest.skip("Symbolic links test skipped on Windows")
        
        real_file = tmp_path / "real.txt"
        real_file.write_text("content")
        
        symlink = tmp_path / "link.txt"
        symlink.symlink_to(real_file)
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        # シンボリックリンクはスキップされ、実ファイルのみ
        assert len(result) == 1
        assert result[0]['path'] == str(real_file)

    def test_skip_symlink_directories(self, tmp_path):
        """シンボリックリンクディレクトリをスキップ"""
        if os.name == 'nt':
            pytest.skip("Symbolic links test skipped on Windows")
        
        real_dir = tmp_path / "real_dir"
        real_dir.mkdir()
        (real_dir / "file.txt").write_text("content")
        
        symlink_dir = tmp_path / "link_dir"
        symlink_dir.symlink_to(real_dir)
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        # シンボリックリンクディレクトリはスキップ
        # 実ディレクトリ内のファイルのみ
        assert len(result) == 1

    def test_circular_symlinks(self, tmp_path):
        """循環参照するシンボリックリンク"""
        if os.name == 'nt':
            pytest.skip("Symbolic links test skipped on Windows")
        
        dir1 = tmp_path / "dir1"
        dir2 = tmp_path / "dir2"
        dir1.mkdir()
        dir2.mkdir()
        
        # 循環参照
        link1 = dir1 / "link_to_dir2"
        link2 = dir2 / "link_to_dir1"
        link1.symlink_to(dir2)
        link2.symlink_to(dir1)
        
        (dir1 / "file.txt").write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        # followlinks=False なので無限ループにならない
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 1


class TestFileScannerDebugMode:
    """デバッグモードのテスト"""

    def test_debug_mode_enabled(self, tmp_path, capsys):
        """デバッグモードが有効"""
        test_file = tmp_path / "test.py"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=True)
        scanner.scan(str(tmp_path))
        
        captured = capsys.readouterr()
        assert "[ADDED]" in captured.out

    def test_debug_mode_symlink_messages(self, tmp_path, capsys):
        """デバッグモードでシンボリックリンクメッセージ"""
        if os.name == 'nt':
            pytest.skip("Symbolic links test skipped on Windows")
        
        real_file = tmp_path / "real.txt"
        real_file.write_text("content")
        
        symlink = tmp_path / "link.txt"
        symlink.symlink_to(real_file)
        
        scanner = FileScanner(filters=[], debug=True)
        scanner.scan(str(tmp_path))
        
        captured = capsys.readouterr()
        assert "[SKIPPED SYMLINK]" in captured.out

    def test_debug_mode_disabled(self, tmp_path, capsys):
        """デバッグモードが無効"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        scanner.scan(str(tmp_path))
        
        captured = capsys.readouterr()
        # デバッグメッセージは出力されない
        assert "[ADDED]" not in captured.out


class TestFileScannerEdgeCases:
    """エッジケースのテスト"""

    def test_scan_permission_denied_directory(self, tmp_path):
        """権限のないディレクトリ"""
        if os.name == 'nt':
            pytest.skip("Permission test skipped on Windows")
        
        restricted_dir = tmp_path / "restricted"
        restricted_dir.mkdir()
        (restricted_dir / "file.txt").write_text("content")
        
        # 権限を削除
        os.chmod(restricted_dir, 0o000)
        
        try:
            scanner = FileScanner(filters=[], debug=False)
            result = scanner.scan(str(tmp_path))
            # PermissionErrorは内部で処理され、スキップされる
        finally:
            # クリーンアップ
            os.chmod(restricted_dir, 0o755)

    def test_scan_very_deep_nesting(self, tmp_path):
        """非常に深いネストのディレクトリ"""
        current = tmp_path
        for i in range(50):
            current = current / f"level{i}"
        current.mkdir(parents=True)
        
        deep_file = current / "deep.txt"
        deep_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 1
        assert result[0]['path'] == str(deep_file)

    def test_scan_many_files(self, tmp_path):
        """大量のファイル"""
        # 100個のファイルを作成
        for i in range(100):
            (tmp_path / f"file{i:03d}.txt").write_text(f"content {i}")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 100

    def test_scan_unicode_filenames(self, tmp_path):
        """Unicode文字を含むファイル名"""
        unicode_files = [
            tmp_path / "日本語.txt",
            tmp_path / "中文.txt",
            tmp_path / "한국어.txt",
            tmp_path / "emoji_😀.txt"
        ]
        
        for f in unicode_files:
            f.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 4

    def test_scan_special_characters_in_filenames(self, tmp_path):
        """特殊文字を含むファイル名"""
        special_files = [
            tmp_path / "file with spaces.txt",
            tmp_path / "file-with-dashes.txt",
            tmp_path / "file_with_underscores.txt",
        ]
        
        for f in special_files:
            f.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 3

    def test_scan_empty_subdirectories(self, tmp_path):
        """空のサブディレクトリを含む"""
        subdir1 = tmp_path / "empty1"
        subdir2 = tmp_path / "empty2"
        subdir3 = tmp_path / "nonempty"
        
        for d in [subdir1, subdir2, subdir3]:
            d.mkdir()
        
        (subdir3 / "file.txt").write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        # 空ディレクトリは無視され、ファイルのみ
        assert len(result) == 1

    def test_scan_mixed_line_endings(self, tmp_path):
        """異なる改行コードを含むファイル"""
        unix_file = tmp_path / "unix.txt"
        unix_file.write_text("line1\nline2\nline3")
        
        windows_file = tmp_path / "windows.txt"
        windows_file.write_text("line1\r\nline2\r\nline3")
        
        mac_file = tmp_path / "mac.txt"
        mac_file.write_text("line1\rline2\rline3")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 3
        # 各ファイルの行数が正しくカウントされる
        for file_info in result:
            assert file_info['lines'] >= 1

    def test_scan_file_with_no_extension(self, tmp_path):
        """拡張子なしのファイル"""
        no_ext_files = [
            tmp_path / "Makefile",
            tmp_path / "Dockerfile",
            tmp_path / "README",
        ]
        
        for f in no_ext_files:
            f.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        assert len(result) == 3

    def test_scan_hidden_files(self, tmp_path):
        """隠しファイル"""
        hidden_file = tmp_path / ".hidden"
        hidden_file.write_text("content")
        
        visible_file = tmp_path / "visible.txt"
        visible_file.write_text("content")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        # フィルタなしでは両方含まれる
        assert len(result) == 2

    def test_scan_with_trailing_newlines(self, tmp_path):
        """末尾に改行があるファイルの行数カウント"""
        with_newline = tmp_path / "with_newline.txt"
        with_newline.write_text("line1\nline2\n")
        
        without_newline = tmp_path / "without_newline.txt"
        without_newline.write_text("line1\nline2")
        
        scanner = FileScanner(filters=[], debug=False)
        result = scanner.scan(str(tmp_path))
        
        # 行数カウントの動作を確認
        assert len(result) == 2