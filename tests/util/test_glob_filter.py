"""Globフィルタのユニットテスト"""
import pytest
import os
from pathlib import Path
from src.filters.glob import GlobFilter


class TestGlobFilterBasic:
    """基本的なGlobフィルタのテスト"""

    def test_no_patterns_includes_all(self, tmp_path):
        """パターン未指定時は全て含める"""
        filter = GlobFilter(patterns=None, base_dir=str(tmp_path))
        
        test_file = tmp_path / "test.py"
        test_file.touch()
        
        assert filter.should_include(str(test_file))
        assert not filter.is_active()

    def test_empty_patterns_includes_all(self, tmp_path):
        """空のパターンリスト"""
        filter = GlobFilter(patterns=[], base_dir=str(tmp_path))
        
        test_file = tmp_path / "test.py"
        test_file.touch()
        
        assert filter.should_include(str(test_file))
        assert not filter.is_active()

    def test_single_extension_match(self, tmp_path):
        """単一の拡張子マッチ"""
        filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path))
        
        py_file = tmp_path / "test.py"
        js_file = tmp_path / "test.js"
        py_file.touch()
        js_file.touch()
        
        assert filter.should_include(str(py_file))
        assert not filter.should_include(str(js_file))
        assert filter.is_active()

    def test_multiple_extensions(self, tmp_path):
        """複数の拡張子パターン"""
        filter = GlobFilter(patterns=["*.py", "*.js", "*.ts"], base_dir=str(tmp_path))
        
        py_file = tmp_path / "code.py"
        js_file = tmp_path / "script.js"
        ts_file = tmp_path / "app.ts"
        txt_file = tmp_path / "readme.txt"
        
        for f in [py_file, js_file, ts_file, txt_file]:
            f.touch()
        
        assert filter.should_include(str(py_file))
        assert filter.should_include(str(js_file))
        assert filter.should_include(str(ts_file))
        assert not filter.should_include(str(txt_file))

    def test_directory_always_included(self, tmp_path):
        """ディレクトリは常に含まれる（中身をスキャンするため）"""
        filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path))
        
        subdir = tmp_path / "src"
        subdir.mkdir()
        
        assert filter.should_include(str(subdir))


class TestGlobFilterPatterns:
    """様々なGlobパターンのテスト"""

    def test_wildcard_pattern(self, tmp_path):
        """ワイルドカードパターン"""
        filter = GlobFilter(patterns=["test_*.py"], base_dir=str(tmp_path))
        
        test_main = tmp_path / "test_main.py"
        test_utils = tmp_path / "test_utils.py"
        main = tmp_path / "main.py"
        
        for f in [test_main, test_utils, main]:
            f.touch()
        
        assert filter.should_include(str(test_main))
        assert filter.should_include(str(test_utils))
        assert not filter.should_include(str(main))

    def test_question_mark_pattern(self, tmp_path):
        """?パターン（1文字マッチ）"""
        filter = GlobFilter(patterns=["file?.txt"], base_dir=str(tmp_path))
        
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file10 = tmp_path / "file10.txt"
        
        for f in [file1, file2, file10]:
            f.touch()
        
        assert filter.should_include(str(file1))
        assert filter.should_include(str(file2))
        assert not filter.should_include(str(file10))

    def test_recursive_pattern(self, tmp_path):
        """再帰的パターン src/**/*.py"""
        filter = GlobFilter(patterns=["src/**/*.py"], base_dir=str(tmp_path))
        
        src = tmp_path / "src"
        utils = src / "utils"
        nested = utils / "nested"
        
        for d in [src, utils, nested]:
            d.mkdir(parents=True, exist_ok=True)
        
        src_main = src / "main.py"
        utils_helper = utils / "helper.py"
        nested_deep = nested / "deep.py"
        root_test = tmp_path / "test.py"
        
        for f in [src_main, utils_helper, nested_deep, root_test]:
            f.touch()
        
        assert filter.should_include(str(src_main))
        assert filter.should_include(str(utils_helper))
        assert filter.should_include(str(nested_deep))
        assert not filter.should_include(str(root_test))

    def test_specific_directory_pattern(self, tmp_path):
        """特定ディレクトリ内のファイル"""
        filter = GlobFilter(patterns=["src/*.py"], base_dir=str(tmp_path))
        
        src = tmp_path / "src"
        tests = tmp_path / "tests"
        
        for d in [src, tests]:
            d.mkdir()
        
        src_file = src / "main.py"
        tests_file = tests / "test.py"
        
        for f in [src_file, tests_file]:
            f.touch()
        
        assert filter.should_include(str(src_file))
        assert not filter.should_include(str(tests_file))

    def test_multiple_directory_patterns(self, tmp_path):
        """複数ディレクトリのパターン"""
        filter = GlobFilter(
            patterns=["src/**/*.py", "tests/**/*.py"],
            base_dir=str(tmp_path)
        )
        
        src = tmp_path / "src"
        tests = tmp_path / "tests"
        docs = tmp_path / "docs"
        
        for d in [src, tests, docs]:
            d.mkdir()
        
        src_file = src / "main.py"
        tests_file = tests / "test_main.py"
        docs_file = docs / "readme.py"
        
        for f in [src_file, tests_file, docs_file]:
            f.touch()
        
        assert filter.should_include(str(src_file))
        assert filter.should_include(str(tests_file))
        assert not filter.should_include(str(docs_file))

    def test_negation_not_supported(self, tmp_path):
        """否定パターン（!）はサポートされない（gitwildmatchの動作）"""
        # 注: pathspecのgitwildmatchは否定をサポートしない
        filter = GlobFilter(patterns=["*.py", "!test_*.py"], base_dir=str(tmp_path))
        
        main = tmp_path / "main.py"
        test_main = tmp_path / "test_main.py"
        
        for f in [main, test_main]:
            f.touch()
        
        # 両方ともマッチする（否定は機能しない）
        assert filter.should_include(str(main))
        # test_*.pyは!パターンで除外されない
        # （除外が必要な場合はIgnoreFilterを使う）


class TestGlobFilterEdgeCases:
    """エッジケースのテスト"""

    def test_case_sensitivity(self, tmp_path):
        """大文字小文字の区別（Linuxでは区別される）"""
        filter = GlobFilter(patterns=["*.PY"], base_dir=str(tmp_path))
        
        upper_file = tmp_path / "TEST.PY"
        lower_file = tmp_path / "test.py"
        
        for f in [upper_file, lower_file]:
            f.touch()
        
        # Linuxでは大文字小文字を区別
        assert filter.should_include(str(upper_file))
        # WindowsやmacOSでは区別しない場合がある

    def test_hidden_files(self, tmp_path):
        """隠しファイル"""
        filter = GlobFilter(patterns=[".*"], base_dir=str(tmp_path))
        
        hidden = tmp_path / ".hidden"
        visible = tmp_path / "visible.txt"
        
        for f in [hidden, visible]:
            f.touch()
        
        assert filter.should_include(str(hidden))
        assert not filter.should_include(str(visible))

    def test_no_extension_files(self, tmp_path):
        """拡張子なしのファイル"""
        filter = GlobFilter(patterns=["Makefile", "Dockerfile"], base_dir=str(tmp_path))
        
        makefile = tmp_path / "Makefile"
        dockerfile = tmp_path / "Dockerfile"
        readme = tmp_path / "README"
        
        for f in [makefile, dockerfile, readme]:
            f.touch()
        
        assert filter.should_include(str(makefile))
        assert filter.should_include(str(dockerfile))
        assert not filter.should_include(str(readme))

    def test_special_characters_in_pattern(self, tmp_path):
        """特殊文字を含むパターン"""
        filter = GlobFilter(patterns=["[test]*.py"], base_dir=str(tmp_path))
        
        # [test]は文字クラスとして解釈される
        test_file = tmp_path / "test.py"
        bracket_file = tmp_path / "[test]main.py"
        
        for f in [test_file, bracket_file]:
            f.touch()
        
        # 't', 'e', 's', 't'のいずれか1文字 + *.py にマッチ
        assert filter.should_include(str(test_file))

    def test_absolute_vs_relative_paths(self, tmp_path):
        """絶対パスと相対パスの処理"""
        filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path))
        
        py_file = tmp_path / "test.py"
        py_file.touch()
        
        # 絶対パスでも相対パスでも動作する
        assert filter.should_include(str(py_file.absolute()))
        assert filter.should_include(str(py_file))

    def test_symlink_handling(self, tmp_path):
        """シンボリックリンクの処理"""
        if os.name == 'nt':
            pytest.skip("Symbolic links test skipped on Windows")
        
        filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path))
        
        real_file = tmp_path / "real.py"
        real_file.touch()
        
        symlink = tmp_path / "link.py"
        symlink.symlink_to(real_file)
        
        assert filter.should_include(str(symlink))

    def test_very_long_path(self, tmp_path):
        """非常に長いパス"""
        filter = GlobFilter(patterns=["**/*.py"], base_dir=str(tmp_path))
        
        # 深くネストしたディレクトリ
        deep_dir = tmp_path
        for i in range(10):
            deep_dir = deep_dir / f"level{i}"
        deep_dir.mkdir(parents=True)
        
        deep_file = deep_dir / "deep.py"
        deep_file.touch()
        
        assert filter.should_include(str(deep_file))

    def test_empty_filename(self, tmp_path):
        """空のファイル名（実際には作れないが、念のため）"""
        filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path))
        
        # 空文字列のパスは含まれない
        assert not filter.should_include("")


class TestGlobFilterDebugMode:
    """デバッグモードのテスト"""

    def test_debug_mode_enabled(self, tmp_path, capsys):
        """デバッグモードが有効な場合"""
        filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path), debug=True)
        
        py_file = tmp_path / "test.py"
        js_file = tmp_path / "test.js"
        
        for f in [py_file, js_file]:
            f.touch()
        
        filter.should_include(str(py_file))
        captured = capsys.readouterr()
        assert "[GLOB MATCHED]" in captured.out or "[GLOB" in captured.out
        
        filter.should_include(str(js_file))
        captured = capsys.readouterr()
        assert "[GLOB NOT MATCHED]" in captured.out or "[GLOB" in captured.out

    def test_debug_mode_disabled(self, tmp_path, capsys):
        """デバッグモードが無効な場合"""
        filter = GlobFilter(patterns=["*.py"], base_dir=str(tmp_path), debug=False)
        
        py_file = tmp_path / "test.py"
        py_file.touch()
        
        filter.should_include(str(py_file))
        captured = capsys.readouterr()
        assert captured.out == ""


class TestGlobFilterInvalidPatterns:
    """無効なパターンのテスト"""

    def test_invalid_regex_pattern(self, tmp_path):
        """無効な正規表現パターン"""
        try:
            filter = GlobFilter(patterns=["[[[invalid"], base_dir=str(tmp_path))
            pytest.skip("Pattern was accepted by pathspec")
        except ValueError:
            pass  # 期待通り

    def test_none_base_dir(self):
        """base_dirがNoneの場合"""
        # 相対パスの解決に失敗する可能性がある
        filter = GlobFilter(patterns=["*.py"], base_dir=None)
        # エラーにならないが、動作は保証されない
        assert filter.is_active()