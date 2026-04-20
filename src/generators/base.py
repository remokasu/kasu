"""コンテンツジェネレータの基底クラス"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class ContentGenerator(ABC):
    """コンテンツ生成の抽象基底クラス"""

    @abstractmethod
    def generate(
        self,
        target_files: List[Dict[str, any]],
        target_dir: str,
        enable_sanitize: bool = False,
        custom_replacements: Optional[List[Tuple[str, str]]] = None,
        head_lines: Optional[int] = None,
        tail_lines: Optional[int] = None,
        root_dir: Optional[str] = None,
        grep_pattern: Optional[List[str]] = None,
        grep_context: int = 3,
        grep_regex: bool = False,
        grep_ignore_case: bool = False,
        include_outline: bool = False,
        outline_patterns: Optional[Dict[str, List[str]]] = None,
        include_tree: bool = False,
        include_list: bool = False,
        include_stats: bool = False,
        include_merge: bool = True,
        tree_structure: Optional[str] = None,
        list_structure: Optional[str] = None,
        absolute_paths: bool = False,
        diff_text: Optional[str] = None,
        render_context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, Dict[str, int]]:
        """
        ファイルリストからコンテンツを生成

        Args:
            target_files: ファイル情報のリスト
            target_dir: ターゲットディレクトリ
            enable_sanitize: サニタイズを有効にするか
            custom_replacements: カスタム置換パターン
            head_lines: 各ファイルの先頭N行のみ
            tail_lines: 各ファイルの末尾N行のみ
            root_dir: 表示用ルートディレクトリ
            grep_pattern: 検索パターン（指定時は該当周辺のみ出力）
            grep_context: 前後の行数
            grep_regex: 正規表現として扱うか
            grep_ignore_case: 大文字小文字を無視するか
            include_outline: アウトラインを含めるか
            outline_patterns: アウトライン用の追加パターン
            include_tree: ツリー構造を含めるか
            include_list: ファイル一覧を含めるか
            include_stats: 統計情報を含めるか
            include_merge: ファイル結合を含めるか
            tree_structure: ツリー構造文字列
            list_structure: ファイル一覧文字列
            absolute_paths: ファイルパスを絶対パスで出力するか
            diff_text: ``git diff`` の生出力（``--diff`` 指定時のみ）
            render_context: JsonGenerator 用のメタ情報辞書
                （``kasu_version`` / ``token_counter`` / ``truncated`` /
                ``truncate_reason`` / ``dry_run`` / ``cli_options``）。
                text / markdown generator は無視する。

        Returns:
            (生成されたコンテンツ, サニタイズ統計)
        """
        pass
