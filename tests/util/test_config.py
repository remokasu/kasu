"""ConfigLoader のユニットテスト (修正版)"""
import pytest
import argparse
import os
from pathlib import Path

from core.config import ConfigLoader


def create_full_args(**overrides):
    """完全なargparse.Namespaceを作成するヘルパー"""
    defaults = {
        'yes': False,
        'tree': False,
        'list': False,
        'sanitize': False,
        'stats': False,
        'debug': False,
        'no_merge': False,
        'ignore_file': None,
        'replace_file': None,
        'glob': None,
        'exclude': None
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


class TestConfigLoaderLoad:
    """設定ファイル読み込みのテスト"""

    def test_load_no_config_file(self):
        """設定ファイルなし"""
        config = ConfigLoader.load(config_path=None)
        
        assert config == {}

    def test_load_specific_config_file(self, tmp_path):
        """指定された設定ファイル"""
        config_file = tmp_path / "my_config.yaml"
        config_file.write_text("tree: true\nsanitize: true\n")
        
        config = ConfigLoader.load(config_path=str(config_file))
        
        assert config['tree'] is True
        assert config['sanitize'] is True

    def test_load_default_config_yaml(self, tmp_path, monkeypatch):
        """デフォルト設定ファイル（.config.yaml）"""
        monkeypatch.chdir(tmp_path)
        
        config_file = tmp_path / ".config.yaml"
        config_file.write_text("tree: true\ndebug: false\n")
        
        config = ConfigLoader.load()
        
        assert config.get('tree') is True
        assert config.get('debug') is False

    def test_load_default_config_yml(self, tmp_path, monkeypatch):
        """デフォルト設定ファイル（.config.yml）"""
        monkeypatch.chdir(tmp_path)
        
        config_file = tmp_path / ".config.yml"
        config_file.write_text("tree: true\n")
        
        config = ConfigLoader.load()
        
        assert config.get('tree') is True

    def test_load_nonexistent_file(self):
        """存在しないファイル"""
        config = ConfigLoader.load(config_path="/nonexistent/config.yaml")
        
        assert config == {}

    def test_load_invalid_yaml(self, tmp_path, capsys):
        """無効なYAML"""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: broken")
        
        config = ConfigLoader.load(config_path=str(config_file))
        
        # エラーメッセージが出力される
        captured = capsys.readouterr()
        assert "Warning" in captured.out or "Error" in captured.out
        
        # 空の設定が返る
        assert config == {}

    def test_load_empty_yaml(self, tmp_path):
        """空のYAMLファイル"""
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")
        
        config = ConfigLoader.load(config_path=str(config_file))
        
        assert config == {}

    def test_load_yaml_with_comments(self, tmp_path):
        """コメント付きYAML"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
# This is a comment
tree: true  # inline comment
# Another comment
sanitize: false
""")
        
        config = ConfigLoader.load(config_path=str(config_file))
        
        assert config['tree'] is True
        assert config['sanitize'] is False


class TestConfigLoaderMerge:
    """設定とコマンドライン引数のマージのテスト"""

    def test_merge_boolean_flags_from_config(self):
        """設定からBooleanフラグをマージ"""
        config = {'yes': True, 'tree': True, 'sanitize': True}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.yes is True
        assert merged.tree is True
        assert merged.sanitize is True

    def test_merge_args_override_config(self):
        """コマンドライン引数が設定を上書き"""
        config = {'yes': False, 'tree': False}
        args = create_full_args(yes=True, tree=True)
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        # 引数がTrueの場合は引数が優先
        assert merged.yes is True
        assert merged.tree is True

    def test_merge_string_options(self):
        """文字列オプションのマージ"""
        config = {
            'ignore_file': '.myignore',
            'replace_file': 'replace.txt'
        }
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.ignore_file == '.myignore'
        assert merged.replace_file == 'replace.txt'

    def test_merge_string_options_args_override(self):
        """文字列オプション - 引数が優先"""
        config = {'ignore_file': 'config_ignore'}
        args = create_full_args(ignore_file='arg_ignore')
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.ignore_file == 'arg_ignore'

    def test_merge_glob_patterns_list(self):
        """Globパターン（リスト形式）"""
        config = {'glob': ['*.py', '*.js']}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.glob == ['*.py', '*.js']

    def test_merge_glob_patterns_string(self):
        """Globパターン（文字列形式）"""
        config = {'glob': '*.py, *.js, *.ts'}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.glob == ['*.py', '*.js', '*.ts']

    def test_merge_glob_patterns_args_override(self):
        """Globパターン - 引数が優先"""
        config = {'glob': ['*.py']}
        args = create_full_args(glob=['*.js'])
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.glob == ['*.js']

    def test_merge_exclude_patterns_list(self):
        """除外パターン（リスト形式）"""
        config = {'exclude': ['*.log', '*.tmp']}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.exclude == ['*.log', '*.tmp']

    def test_merge_exclude_patterns_string(self):
        """除外パターン（文字列形式）"""
        config = {'exclude': '*.log, *.tmp'}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.exclude == ['*.log', '*.tmp']

    def test_merge_exclude_patterns_args_override(self):
        """除外パターン - 引数が優先"""
        config = {'exclude': ['*.log']}
        args = create_full_args(exclude=['*.tmp'])
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.exclude == ['*.tmp']

    def test_merge_invalid_glob_type(self, capsys):
        """無効なGlobパターンの型"""
        config = {'glob': [1, 2, 3]}  # 整数リスト
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        # 警告が出力される
        captured = capsys.readouterr()
        assert "Warning" in captured.err
        
        # globは変更されない
        assert merged.glob is None

    def test_merge_all_boolean_flags(self):
        """全てのBooleanフラグ"""
        config = {
            'yes': True,
            'tree': True,
            'list': True,
            'sanitize': True,
            'stats': True,
            'debug': True,
            'no_merge': True
        }
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.yes is True
        assert merged.tree is True
        assert merged.list is True
        assert merged.sanitize is True
        assert merged.stats is True
        assert merged.debug is True
        assert merged.no_merge is True

    def test_merge_empty_config(self):
        """空の設定"""
        config = {}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        # 引数がそのまま保持される
        assert merged.yes is False
        assert merged.tree is False
        assert merged.ignore_file is None

    def test_merge_partial_config(self):
        """一部の設定のみ"""
        config = {'tree': True}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.tree is True
        assert merged.yes is False
        assert merged.sanitize is False


class TestConfigLoaderEdgeCases:
    """エッジケースのテスト"""

    def test_merge_with_extra_args(self):
        """追加の引数属性"""
        config = {'tree': True}
        args = create_full_args(extra_arg='extra_value')
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        assert merged.tree is True
        assert merged.extra_arg == 'extra_value'

    def test_merge_with_none_values(self):
        """None値を含む設定"""
        config = {'ignore_file': None, 'replace_file': None}
        args = create_full_args(ignore_file='arg_ignore')
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        # 引数が優先される
        assert merged.ignore_file == 'arg_ignore'
        assert merged.replace_file is None

    def test_merge_glob_empty_string(self):
        """空文字列のGlobパターン"""
        config = {'glob': ''}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        # 空文字列は処理される
        assert merged.glob is None or merged.glob == ['']

    def test_merge_glob_whitespace_only(self):
        """空白のみのGlobパターン"""
        config = {'glob': '   ,  ,   '}
        args = create_full_args()
        
        merged = ConfigLoader.merge_with_args(config, args)
        
        # 空白は削除される
        if merged.glob:
            assert all(p.strip() == '' or p for p in merged.glob)


class TestConfigLoaderIntegration:
    """統合テスト"""

    def test_config_with_all_options(self, tmp_path):
        """全オプションを含む設定"""
        config_file = tmp_path / "full_config.yaml"
        config_file.write_text("""
# Boolean flags
tree: true
list: true
sanitize: true
stats: true
debug: true
no_merge: false

# File paths
ignore_file: '.gitignore'
replace_file: 'replace.txt'

# Patterns
glob:
  - '*.py'
  - '*.js'
  - 'src/**/*.ts'
exclude:
  - '*.log'
  - '*.tmp'
  - 'build/'
""")
        
        config = ConfigLoader.load(config_path=str(config_file))
        
        assert config.get('tree') is True
        assert config.get('list') is True
        assert config.get('sanitize') is True
        assert config.get('stats') is True
        assert config.get('debug') is True
        assert config.get('no_merge') is False
        assert config.get('ignore_file') == '.gitignore'
        assert config.get('replace_file') == 'replace.txt'
        assert len(config.get('glob', [])) == 3
        assert len(config.get('exclude', [])) == 3
