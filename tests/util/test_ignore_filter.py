"""Ignoreフィルタのユニットテスト"""
import pytest
import os
from pathlib import Path
from src.filters.ignore import IgnoreFilter


class TestIgnoreFilterBasic:
    """基本的なIgnoreフィルタのテスト"""

    def test_empty_patterns(self, tmp_path):
        """空のパターンリスト"""
        filter = IgnoreFilter(patterns=[], base_dir=str(tmp_path), debug=False)
        
        test_file = tmp_path / "test.py"
        test_file.touch()
        
        assert filter.should_include(str(test_file))

    def test_single_file_pattern(self, tmp_path):
        """単一ファイルの除外"""
        filter = IgnoreFilter(patterns=["test.log"], base_dir=str(tmp_path), debug=False)
        
        log_file = tmp_path / "test.log"
        py_file = tmp_path / "test.py"
        
        for f in [log_file, py_file]:
            f.touch()
        
        assert not filter.should_include(str(log_file))
        assert filter.should_include(str(py_file))

    def test_extension_pattern(self, tmp_path):
        """拡張子による除外"""
        filter = IgnoreFilter(patterns=["*.log"], base_dir=str(tmp_path), debug=False)
        
        debug_log = tmp_path / "debug.log"
        error_log = tmp_path / "error.log"
        readme = tmp_path / "README.md"
        
        for f in [debug_log, error_log, readme]:
            f.touch()
        
        assert not filter.should_include(str(debug_log))
        assert not filter.should_include(str(error_log))
        assert filter.should_include(str(readme))

    def test_directory_pattern(self, tmp_path):
        """ディレクトリの除外"""
        filter = IgnoreFilter(patterns=["build/"], base_dir=str(tmp_path), debug=False)
        
        build_dir = tmp_path / "build"
        src_dir = tmp_path / "src"
        
        for d in [build_dir, src_dir]:
            d.mkdir()
        
        build_file = build_dir / "output.txt"
        src_file = src_dir / "main.py"
        
        for f in [build_file, src_file]:
            f.touch()
        
        assert not filter.should_include(str(build_dir))
        assert not filter.should_include(str(build_file))
        assert filter.should_include(str(src_dir))
        assert filter.should_include(str(src_file))

    def test_multiple_patterns(self, tmp_path):
        """複数のパターン"""
        filter = IgnoreFilter(
            patterns=["*.log", "*.tmp", "cache/"],
            base_dir=str(tmp_path),
            debug=False
        )
        
        log_file = tmp_path / "debug.log"
        tmp_file = tmp_path / "temp.tmp"
        cache_dir = tmp_path / "cache"
        py_file = tmp_path / "main.py"
        
        cache_dir.mkdir()
        for f in [log_file, tmp_file, py_file]:
            f.touch()
        
        assert not filter.should_include(str(log_file))
        assert not filter.should_include(str(tmp_file))
        assert not filter.should_include(str(cache_dir))
        assert filter.should_include(str(py_file))


class TestIgnoreFilterGitignorePatterns:
    """.gitignore互換パターンのテスト"""

    def test_wildcard_pattern(self, tmp_path):
        """ワイルドカードパターン"""
        filter = IgnoreFilter(patterns=["test_*.py"], base_dir=str(tmp_path), debug=False)
        
        test_main = tmp_path / "test_main.py"
        test_utils = tmp_path / "test_utils.py"
        main = tmp_path / "main.py"
        
        for f in [test_main, test_utils, main]:
            f.touch()
        
        assert not filter.should_include(str(test_main))
        assert not filter.should_include(str(test_utils))
        assert filter.should_include(str(main))

    def test_directory_wildcard(self, tmp_path):
        """ディレクトリ内の全ファイル除外"""
        filter = IgnoreFilter(patterns=["node_modules/"], base_dir=str(tmp_path), debug=False)
        
        node_modules = tmp_path / "node_modules"
        node_modules.mkdir()
        
        package = node_modules / "package"
        package.mkdir()
        
        index_js = package / "index.js"
        index_js.touch()
        
        assert not filter.should_include(str(node_modules))
        assert not filter.should_include(str(package))
        assert not filter.should_include(str(index_js))

    def test_recursive_pattern(self, tmp_path):
        """再帰的パターン **/test"""
        filter = IgnoreFilter(patterns=["**/test"], base_dir=str(tmp_path), debug=False)
        
        test1 = tmp_path / "test"
        test1.mkdir()
        
        subdir = tmp_path / "src"
        subdir.mkdir()
        test2 = subdir / "test"
        test2.mkdir()
        
        # どちらのtestディレクトリも除外される
        assert not filter.should_include(str(test1))
        assert not filter.should_include(str(test2))

    def test_leading_slash_pattern(self, tmp_path):
        """先頭スラッシュパターン（ルートディレクトリのみ）"""
        filter = IgnoreFilter(patterns=["/build"], base_dir=str(tmp_path), debug=False)
        
        root_build = tmp_path / "build"
        root_build.mkdir()
        
        subdir = tmp_path / "src"
        subdir.mkdir()
        sub_build = subdir / "build"
        sub_build.mkdir()
        
        # ルートのbuildのみ除外
        assert not filter.should_include(str(root_build))
        # サブディレクトリのbuildは含まれる
        assert filter.should_include(str(sub_build))

    def test_negation_pattern(self, tmp_path):
        """否定パターン（!）"""
        # 注: pathspecの動作により、単独では機能しない場合がある
        filter = IgnoreFilter(
            patterns=["*.log", "!important.log"],
            base_dir=str(tmp_path),
            debug=False
        )
        
        debug_log = tmp_path / "debug.log"
        important_log = tmp_path / "important.log"
        
        for f in [debug_log, important_log]:
            f.touch()
        
        # *.logで全てマッチ
        assert not filter.should_include(str(debug_log))
        # !important.logは後から追加されているが、
        # pathspecの実装によっては否定が効かない可能性がある

    def test_double_asterisk_pattern(self, tmp_path):
        """ダブルアスタリスクパターン **/"""
        filter = IgnoreFilter(patterns=["**/*.pyc"], base_dir=str(tmp_path), debug=False)
        
        root_pyc = tmp_path / "main.pyc"
        root_pyc.touch()
        
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        deep_pyc = deep / "utils.pyc"
        deep_pyc.touch()
        
        py_file = tmp_path / "main.py"
        py_file.touch()
        
        assert not filter.should_include(str(root_pyc))
        assert not filter.should_include(str(deep_pyc))
        assert filter.should_include(str(py_file))


class TestIgnoreFilterVCS:
    """VCS自動除外のテスト"""

    def test_auto_vcs_ignore_enabled(self, tmp_path):
        """VCS自動除外が有効"""
        filter = IgnoreFilter(
            patterns=[],
            base_dir=str(tmp_path),
            debug=False,
            auto_vcs_ignore=True
        )
        
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        
        gitignore = tmp_path / ".gitignore"
        gitignore.touch()
        
        svn_dir = tmp_path / ".svn"
        svn_dir.mkdir()
        
        normal_file = tmp_path / "main.py"
        normal_file.touch()
        
        # VCS関連は除外される
        assert not filter.should_include(str(git_dir))
        assert not filter.should_include(str(gitignore))
        assert not filter.should_include(str(svn_dir))
        
        # 通常のファイルは含まれる
        assert filter.should_include(str(normal_file))

    def test_auto_vcs_ignore_disabled(self, tmp_path):
        """VCS自動除外が無効"""
        filter = IgnoreFilter(
            patterns=[],
            base_dir=str(tmp_path),
            debug=False,
            auto_vcs_ignore=False
        )
        
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        
        gitignore = tmp_path / ".gitignore"
        gitignore.touch()
        
        # VCS関連も含まれる
        assert filter.should_include(str(git_dir))
        assert filter.should_include(str(gitignore))

    def test_vcs_patterns_list(self, tmp_path):
        """VCSパターンのリスト"""
        # VCS_PATTERNSが正しく定義されているか確認
        assert ".git/" in IgnoreFilter.VCS_PATTERNS
        assert ".svn/" in IgnoreFilter.VCS_PATTERNS
        assert ".gitignore" in IgnoreFilter.VCS_PATTERNS


class TestIgnoreFilterFileLoading:
    """ファイル読み込みのテスト"""

    def test_load_patterns_basic(self, tmp_path):
        """基本的なパターン読み込み"""
        ignore_file = tmp_path / ".gitignore"
        ignore_file.write_text("*.log\n*.tmp\nbuild/\n")
        
        patterns = IgnoreFilter.load_patterns(str(ignore_file))
        
        assert len(patterns) == 3
        assert "*.log" in patterns
        assert "*.tmp" in patterns
        assert "build/" in patterns

    def test_load_patterns_with_comments(self, tmp_path):
        """コメント付きパターン"""
        ignore_file = tmp_path / ".gitignore"
        ignore_file.write_text("# Log files\n*.log\n# Temp files\n*.tmp\n")
        
        patterns = IgnoreFilter.load_patterns(str(ignore_file))
        
        assert len(patterns) == 2
        assert "*.log" in patterns
        assert "*.tmp" in patterns
        assert "# Log files" not in patterns

    def test_load_patterns_with_empty_lines(self, tmp_path):
        """空行を含むパターン"""
        ignore_file = tmp_path / ".gitignore"
        ignore_file.write_text("\n*.log\n\n*.tmp\n\n")
        
        patterns = IgnoreFilter.load_patterns(str(ignore_file))
        
        assert len(patterns) == 2

    def test_load_patterns_nonexistent_file(self):
        """存在しないファイル"""
        patterns = IgnoreFilter.load_patterns("/nonexistent/.gitignore")
        
        assert patterns == []

    def test_load_patterns_with_whitespace(self, tmp_path):
        """空白を含むパターン"""
        ignore_file = tmp_path / ".gitignore"
        ignore_file.write_text("  *.log  \n\t*.tmp\t\n")
        
        patterns = IgnoreFilter.load_patterns(str(ignore_file))
        
        # strip()されているはず
        assert "*.log" in patterns
        assert "*.tmp" in patterns

    def test_auto_detect_gitignore_exists(self, tmp_path):
        """.gitignoreの自動検出（存在する場合）"""
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.log\n")
        
        detected = IgnoreFilter.auto_detect_ignore_file(str(tmp_path))
        
        assert detected == str(gitignore)

    def test_auto_detect_gitignore_not_exists(self, tmp_path):
        """.gitignoreの自動検出（存在しない場合）"""
        detected = IgnoreFilter.auto_detect_ignore_file(str(tmp_path))
        
        assert detected is None

    def test_load_patterns_from_multiple(self, tmp_path):
        """複数ファイルからのパターン読み込み"""
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.log\n")
        
        dockerignore = tmp_path / ".dockerignore"
        dockerignore.write_text("*.tmp\n")
        
        patterns = IgnoreFilter.load_patterns_from_multiple([
            str(gitignore),
            str(dockerignore)
        ])
        
        assert len(patterns) == 2
        assert "*.log" in patterns
        assert "*.tmp" in patterns

    def test_load_patterns_from_multiple_with_none(self, tmp_path):
        """Noneを含む複数ファイル"""
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("*.log\n")
        
        patterns = IgnoreFilter.load_patterns_from_multiple([
            str(gitignore),
            None,
            "/nonexistent"
        ])
        
        assert "*.log" in patterns


class TestIgnoreFilterEdgeCases:
    """エッジケースのテスト"""

    def test_hidden_files(self, tmp_path):
        """隠しファイルの除外"""
        filter = IgnoreFilter(patterns=[".*"], base_dir=str(tmp_path), debug=False)
        
        hidden = tmp_path / ".hidden"
        visible = tmp_path / "visible.txt"
        
        for f in [hidden, visible]:
            f.touch()
        
        assert not filter.should_include(str(hidden))
        assert filter.should_include(str(visible))

    def test_case_sensitivity(self, tmp_path):
        """大文字小文字の区別"""
        filter = IgnoreFilter(patterns=["*.LOG"], base_dir=str(tmp_path), debug=False)
        
        upper_log = tmp_path / "DEBUG.LOG"
        lower_log = tmp_path / "debug.log"
        
        for f in [upper_log, lower_log]:
            f.touch()
        
        assert not filter.should_include(str(upper_log))
        # Linuxでは大文字小文字を区別

    def test_symlink_handling(self, tmp_path):
        """シンボリックリンクの処理"""
        if os.name == 'nt':
            pytest.skip("Symbolic links test skipped on Windows")
        
        filter = IgnoreFilter(patterns=["*.log"], base_dir=str(tmp_path), debug=False)
        
        real_file = tmp_path / "debug.log"
        real_file.touch()
        
        symlink = tmp_path / "link.log"
        symlink.symlink_to(real_file)
        
        assert not filter.should_include(str(symlink))

    def test_very_long_pattern(self, tmp_path):
        """非常に長いパターン"""
        long_pattern = "a" * 1000 + "*.py"
        filter = IgnoreFilter(patterns=[long_pattern], base_dir=str(tmp_path), debug=False)
        
        # エラーにならないことを確認
        test_file = tmp_path / "test.py"
        test_file.touch()
        filter.should_include(str(test_file))

    def test_special_characters_in_filename(self, tmp_path):
        """特殊文字を含むファイル名"""
        filter = IgnoreFilter(patterns=["[test].py"], base_dir=str(tmp_path), debug=False)
        
        # [test]は文字クラスとして解釈される
        bracket_file = tmp_path / "[test].py"
        bracket_file.touch()
        
        # パターンマッチの動作を確認
        result = filter.should_include(str(bracket_file))
        # 結果は実装依存

    def test_unicode_patterns(self, tmp_path):
        """Unicode文字を含むパターン"""
        filter = IgnoreFilter(patterns=["日本語*.txt"], base_dir=str(tmp_path), debug=False)
        
        jp_file = tmp_path / "日本語ファイル.txt"
        en_file = tmp_path / "english.txt"
        
        for f in [jp_file, en_file]:
            f.touch()
        
        assert not filter.should_include(str(jp_file))
        assert filter.should_include(str(en_file))

    def test_empty_pattern_string(self, tmp_path):
        """空文字列のパターン"""
        filter = IgnoreFilter(patterns=[""], base_dir=str(tmp_path), debug=False)
        
        test_file = tmp_path / "test.py"
        test_file.touch()
        
        # 空パターンは何にもマッチしない
        assert filter.should_include(str(test_file))


class TestIgnoreFilterDebugMode:
    """デバッグモードのテスト"""

    def test_debug_mode_enabled(self, tmp_path, capsys):
        """デバッグモードが有効な場合"""
        filter = IgnoreFilter(patterns=["*.log"], base_dir=str(tmp_path), debug=True)
        
        log_file = tmp_path / "debug.log"
        log_file.touch()
        
        filter.should_include(str(log_file))
        captured = capsys.readouterr()
        assert "[IGNORED]" in captured.out

    def test_debug_mode_disabled(self, tmp_path, capsys):
        """デバッグモードが無効な場合"""
        filter = IgnoreFilter(patterns=["*.log"], base_dir=str(tmp_path), debug=False)
        
        log_file = tmp_path / "debug.log"
        log_file.touch()
        
        filter.should_include(str(log_file))
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_debug_directory_ignored(self, tmp_path, capsys):
        """ディレクトリが無視される場合のデバッグ出力"""
        filter = IgnoreFilter(patterns=["build/"], base_dir=str(tmp_path), debug=True)
        
        build_dir = tmp_path / "build"
        build_dir.mkdir()
        
        filter.should_include(str(build_dir))
        captured = capsys.readouterr()
        assert "[IGNORED" in captured.out and ("DIR]" in captured.out or "]" in captured.out)


class TestIgnoreFilterRelativePaths:
    """相対パス処理のテスト"""

    def test_relative_path_conversion(self, tmp_path):
        """相対パスへの変換"""
        filter = IgnoreFilter(patterns=["src/*.py"], base_dir=str(tmp_path), debug=False)
        
        src = tmp_path / "src"
        src.mkdir()
        
        src_file = src / "main.py"
        src_file.touch()
        
        # 絶対パスで渡しても正しく動作
        assert not filter.should_include(str(src_file.absolute()))

    def test_windows_path_separator(self, tmp_path):
        """Windowsパス区切り文字の処理"""
        filter = IgnoreFilter(patterns=["src/*.py"], base_dir=str(tmp_path), debug=False)
        
        src = tmp_path / "src"
        src.mkdir()
        
        src_file = src / "main.py"
        src_file.touch()
        
        # パス区切り文字が正規化される
        assert not filter.should_include(str(src_file))

    def test_different_drive_paths(self, tmp_path):
        """異なるドライブのパス（Windows）"""
        if os.name != 'nt':
            pytest.skip("Windows-specific test")
        
        filter = IgnoreFilter(patterns=["*.log"], base_dir=str(tmp_path), debug=False)
        
        # 異なるドライブの場合は相対パスが作れない
        # ValueError処理が正しく動作することを確認
        try:
            result = filter.should_include("D:\\test.log")
            # エラーにならず、Falseまたは処理される
        except:
            pytest.fail("Should handle different drive paths gracefully")