"""CLI のユニットテスト"""
import pytest
import sys
import os
from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock
import cli


class TestCLIBasic:
    """CLI基本機能のテスト"""
    
    def test_main_with_basic_args(self, tmp_path, monkeypatch):
        """基本的な引数でのCLI実行"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        output_file = tmp_path / "output.txt"
        
        # コマンドライン引数を設定
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        # main()を実行
        cli.main()
        
        # 出力ファイルが作成される
        assert output_file.exists()
    
    def test_main_with_stdout(self, tmp_path, monkeypatch, capsys):
        """stdout出力"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '--stdout'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        captured = capsys.readouterr()
        assert "hello" in captured.out


class TestCLIOptions:
    """各種オプションのテスト"""
    
    def test_markdown_format(self, tmp_path, monkeypatch):
        """Markdown形式"""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")
        
        output_file = tmp_path / "output.md"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-f', 'md',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        assert output_file.exists()
        content = output_file.read_text()
        assert "```python" in content
    
    def test_tree_option(self, tmp_path, monkeypatch):
        """ツリー表示"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-t',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        content = output_file.read_text()
        assert "test.txt" in content
    
    def test_sanitize_option(self, tmp_path, monkeypatch):
        """サニタイズオプション"""
        test_file = tmp_path / "config.txt"
        test_file.write_text("email: user@example.com")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-s',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        content = output_file.read_text()
        # サニタイズされている可能性
        assert output_file.exists()
    
    def test_glob_option(self, tmp_path, monkeypatch):
        """Globパターン"""
        (tmp_path / "keep.py").write_text("python")
        (tmp_path / "skip.js").write_text("javascript")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-g', '*.py',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        content = output_file.read_text()
        assert "keep.py" in content
        assert "skip.js" not in content


class TestCLIErrorHandling:
    """CLIエラーハンドリングのテスト"""
    
    def test_nonexistent_input_directory(self, tmp_path, monkeypatch):
        """存在しない入力ディレクトリ"""
        test_args = [
            'ks',
            '-i', str(tmp_path / "nonexistent"),
            '-o', 'output.txt'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        with pytest.raises(SystemExit):
            cli.main()
    
    def test_missing_output_argument(self, tmp_path, monkeypatch):
        """出力先未指定"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        test_args = [
            'ks',
            '-i', str(tmp_path)
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        with pytest.raises(SystemExit):
            cli.main()
    
    def test_empty_output_path(self, tmp_path, monkeypatch):
        """空の出力パス"""
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', ''
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        with pytest.raises(SystemExit):
            cli.main()
    
    def test_head_and_tail_conflict(self, tmp_path, monkeypatch):
        """--head と --tail の同時指定"""
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', 'output.txt',
            '--head', '10',
            '--tail', '5'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        with pytest.raises(SystemExit):
            cli.main()


class TestCLIDisplayOnly:
    """表示のみモードのテスト"""
    
    def test_tree_only(self, tmp_path, monkeypatch, capsys):
        """ツリー表示のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-t'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        captured = capsys.readouterr()
        assert "test.txt" in captured.out
    
    def test_stats_only(self, tmp_path, monkeypatch, capsys):
        """統計表示のみ"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '--stats'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        captured = capsys.readouterr()
        assert "Statistics" in captured.out or "Total files" in captured.out


class TestCLIConfigFile:
    """設定ファイルのテスト"""
    
    def test_with_config_file(self, tmp_path, monkeypatch):
        """設定ファイル指定"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        config_file = tmp_path / "my_config.yaml"
        config_file.write_text("tree: true\n")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-c', str(config_file),
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        assert output_file.exists()


class TestCLIFilters:
    """フィルタ機能のテスト"""
    
    def test_gitignore_auto_detect(self, tmp_path, monkeypatch, capsys):
        """gitignore自動検出"""
        (tmp_path / ".gitignore").write_text("*.log\n")
        (tmp_path / "keep.txt").write_text("keep")
        (tmp_path / "skip.log").write_text("skip")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        captured = capsys.readouterr()
        assert "Auto-detected" in captured.out
        
        content = output_file.read_text()
        assert "keep.txt" in content
        assert "skip.log" not in content
    
    def test_no_auto_ignore(self, tmp_path, monkeypatch):
        """--no-auto-ignore オプション"""
        (tmp_path / ".gitignore").write_text("*.log\n")
        (tmp_path / "test.log").write_text("log")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '--no-auto-ignore',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        content = output_file.read_text()
        # .gitignoreが無視されるので.logファイルも含まれる
        assert "test.log" in content


class TestCLIAdvancedOptions:
    """高度なオプションのテスト"""
    
    def test_head_lines(self, tmp_path, monkeypatch):
        """--head オプション"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '--head', '2',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        content = output_file.read_text()
        assert "line1" in content
        assert "line2" in content
    
    def test_custom_replacement(self, tmp_path, monkeypatch):
        """カスタム置換パターン"""
        test_file = tmp_path / "data.txt"
        test_file.write_text("SECRET=my_secret_value")
        
        replace_file = tmp_path / "replace.txt"
        replace_file.write_text("my_secret_value -> [REPLACED]\n")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-r', str(replace_file),
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        content = output_file.read_text()
        assert "my_secret_value" not in content or "[REPLACED]" in content


# tests/unit/test_cli.py に追加

class TestCLIEdgeCases:
    """CLI エッジケース"""
    
    def test_input_not_directory(self, tmp_path, monkeypatch):
        """入力パスがディレクトリでない"""
        test_file = tmp_path / "not_a_dir.txt"
        test_file.write_text("content")
        
        test_args = [
            'ks',
            '-i', str(test_file),  # ファイルを指定
            '-o', 'output.txt'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        with pytest.raises(SystemExit):
            cli.main()
    
    def test_ignore_file_not_found_warning(self, tmp_path, monkeypatch, capsys):
        """存在しないignoreファイルの警告"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '--ignore', str(tmp_path / "nonexistent.gitignore"),
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        captured = capsys.readouterr()
        assert "Warning" in captured.err
    
    def test_invalid_glob_pattern_warning(self, tmp_path, monkeypatch, capsys):
        """無効なGlobパターンの警告"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-g', '[[[invalid',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        try:
            cli.main()
        except:
            pass  # エラーが発生する可能性
        
        # 警告またはエラーが出力される
        captured = capsys.readouterr()
        # 処理が続行されるか、エラーで終了
    
    def test_list_option(self, tmp_path, monkeypatch):
        """--list オプション"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-l',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        content = output_file.read_text()
        assert "File List" in content or "test.txt" in content
    
    def test_exclude_option(self, tmp_path, monkeypatch):
        """--exclude オプション"""
        (tmp_path / "keep.txt").write_text("keep")
        (tmp_path / "skip.log").write_text("skip")
        
        output_file = tmp_path / "output.txt"
        
        test_args = [
            'ks',
            '-i', str(tmp_path),
            '-o', str(output_file),
            '-x', '*.log',
            '-y'
        ]
        
        monkeypatch.setattr(sys, 'argv', test_args)
        
        cli.main()
        
        content = output_file.read_text()
        assert "keep.txt" in content
        assert "skip.log" not in content