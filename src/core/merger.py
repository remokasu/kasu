"""メイン処理ロジック"""
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

from core.file_scanner import FileScanner
from generators.base import ContentGenerator
from utils.statistics import Statistics
from utils.tree import TreeBuilder
from utils.list import ListBuilder


class Merger:
    """ファイルマージの主要ロジックを管理"""

    def __init__(
        self,
        scanner: FileScanner,
        generator: ContentGenerator,
        tree_builder: Optional[TreeBuilder] = None,
        list_builder: Optional[ListBuilder] = None,
    ):
        self.scanner = scanner
        self.generator = generator
        self.tree_builder = tree_builder
        self.list_builder = list_builder

    def merge(
        self,
        target_dir: str,
        output_file: Optional[str] = None,
        to_stdout: bool = False,
        show_tree: bool = False,
        show_list: bool = False,
        show_stats: bool = False,
        skip_confirm: bool = False,
        enable_sanitize: bool = False,
        custom_replacements: Optional[List] = None,
        head_lines: Optional[int] = None,
        tail_lines: Optional[int] = None,
        root_dir: Optional[str] = None,
        grep_pattern: Optional[List[str]] = None,
        grep_context: int = 3,
        grep_regex: bool = False,
        grep_ignore_case: bool = False,
        include_outline: bool = False,
        outline_patterns: Optional[Dict[str, List[str]]] = None,
        include_merge: bool = True,
        dry_run: bool = False,
        absolute_paths: bool = False,
        max_tokens: Optional[int] = None,
        max_bytes: Optional[int] = None,
        token_counter=None,
        since_paths: Optional[List[str]] = None,
        diff_text: Optional[str] = None,
        render_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        ファイルをマージして出力

        Args:
            target_dir: ターゲットディレクトリ
            output_file: 出力ファイル
            to_stdout: 標準出力に出力するか
            show_tree: ツリーを含めるか
            show_stats: 統計を含めるか
            skip_confirm: 確認をスキップするか
            enable_sanitize: サニタイズを有効にするか
            custom_replacements: カスタム置換パターン
            head_lines: 各ファイルの先頭N行のみ
            tail_lines: 各ファイルの末尾N行のみ
            grep_pattern: 検索パターン
            grep_context: 前後の行数
            grep_regex: 正規表現として扱うか
            grep_ignore_case: 大文字小文字を無視するか
            include_outline: アウトラインを含めるか
            outline_patterns: アウトライン用の追加パターン
            include_merge: ファイル結合を含めるか
            dry_run: dry-run モード（content を出さない）
            absolute_paths: ファイルパスを絶対パスで出力するか
            max_tokens: 出力上限（tokens）。超えたらファイル単位で truncate
            max_bytes: 出力上限（bytes）。超えたらファイル単位で truncate
            token_counter: トークン数計算用（``TokenCounter`` インスタンス）
            since_paths: ``--since`` で取得したファイルパス（指定時は
                scanner.scan() の代わりに使う）
            diff_text: ``git diff`` の生出力（``--diff`` 指定時）
            render_context: Generator に渡す追加コンテキスト
        """
        # 表示のみモード判定（dry_run は表示のみ扱いにしない。
        # 必ず output_file or stdout で出す）
        display_only = (show_tree or show_list or show_stats) \
            and not output_file and not to_stdout and not dry_run

        # ファイルスキャン（--since 指定時はそちらを優先）
        if to_stdout:
            print("Scanning files...", file=sys.stderr)
        else:
            print("Scanning files...")

        if since_paths is not None:
            target_files = self.scanner.scan_from_paths(target_dir, since_paths)
        else:
            target_files = self.scanner.scan(target_dir)
        scan_stats = self.scanner.get_stats()

        output_stream = sys.stderr if to_stdout else sys.stdout
        print(f"Found {len(target_files)} files", file=output_stream)

        if scan_stats['glob_filtered'] > 0:
            print(f"Filtered by glob: {scan_stats['glob_filtered']} files", file=output_stream)
        if scan_stats['ignored'] > 0:
            print(f"Ignored by patterns: {scan_stats['ignored']} files/directories", file=output_stream)

        # 出力上限の適用（ファイル単位で truncate）
        truncated = False
        truncate_reason: Optional[str] = None
        if max_bytes is not None or max_tokens is not None:
            target_files, truncated, truncate_reason = self._apply_limits(
                target_files, max_bytes, max_tokens, token_counter
            )
            if truncated:
                print(
                    f"Warning: Output truncated at {len(target_files)} files "
                    f"(reason: {truncate_reason})",
                    file=sys.stderr,
                )

        # dry_run 時に sanitize を無視
        if dry_run and enable_sanitize:
            print("Info: --sanitize is ignored in --dry-run mode", file=sys.stderr)
            enable_sanitize = False
            custom_replacements = None

        # ツリー・リスト
        tree_output = None
        if show_tree and self.tree_builder:
            tree_output = self.tree_builder.build(target_dir, display_root=root_dir)

        list_output = None
        if show_list and self.list_builder:
            list_output = self.list_builder.build(target_files)

        if display_only:
            if show_tree and tree_output:
                stream = sys.stderr if to_stdout else sys.stdout
                print("\nDirectory tree:", file=stream)
                print(tree_output, file=stream)
                print("", file=stream)
            if show_list and list_output:
                stream = sys.stderr if to_stdout else sys.stdout
                print("\nFile list:", file=stream)
                print(list_output, file=stream)
                print("", file=stream)
            if show_stats:
                stats = Statistics.calculate(target_files, token_counter=token_counter)
                Statistics.print_statistics(stats, show_tokens=token_counter is not None)
            return

        if not skip_confirm and not to_stdout and output_file:
            response = input(f"Merge into '{output_file}'? (y/n): ")
            if response.lower() not in ['y', 'yes']:
                print("Cancelled")
                return

        # dry_run なら generator に content を出させない
        effective_include_merge = include_merge and not dry_run

        # render_context をマージして generator に渡す
        final_render_context = dict(render_context or {})
        final_render_context.setdefault('token_counter', token_counter)
        final_render_context.setdefault('show_tokens', token_counter is not None)
        final_render_context['dry_run'] = dry_run
        final_render_context['truncated'] = truncated
        final_render_context['truncate_reason'] = truncate_reason

        self._write_output(
            target_files=target_files,
            target_dir=target_dir,
            output_file=output_file,
            to_stdout=to_stdout,
            enable_sanitize=enable_sanitize,
            custom_replacements=custom_replacements,
            head_lines=head_lines,
            tail_lines=tail_lines,
            root_dir=root_dir,
            grep_pattern=grep_pattern,
            grep_context=grep_context,
            grep_regex=grep_regex,
            grep_ignore_case=grep_ignore_case,
            include_outline=include_outline,
            outline_patterns=outline_patterns,
            include_tree=show_tree,
            include_list=show_list,
            include_stats=show_stats,
            include_merge=effective_include_merge,
            tree_structure=tree_output,
            list_structure=list_output,
            absolute_paths=absolute_paths,
            diff_text=diff_text,
            render_context=final_render_context,
        )

    @staticmethod
    def _apply_limits(
        target_files: List[Dict],
        max_bytes: Optional[int],
        max_tokens: Optional[int],
        token_counter,
    ) -> Tuple[List[Dict], bool, Optional[str]]:
        """ファイル単位で累計 size / tokens をチェックし、上限到達時に切る

        Returns:
            (採択されたファイルリスト, truncated フラグ, truncate 理由)
        """
        if max_bytes is None and max_tokens is None:
            return target_files, False, None

        if max_tokens is not None and token_counter is None:
            # ``--max-tokens`` 指定時は CLI 側で TokenCounter が必ず初期化される。
            # Merger を直接使うコードから token_counter=None で呼ばれた場合は
            # サイレントで無視せず、ユーザに警告する（CLI経由なら到達しない）
            print(
                "Warning: --max-tokens requires a token_counter; "
                "tokens limit will be ignored.",
                file=sys.stderr,
            )

        accepted: List[Dict] = []
        total_bytes = 0
        total_tokens = 0
        truncated = False
        reason: Optional[str] = None

        for file_info in target_files:
            size = file_info.get('size', 0)
            next_bytes = total_bytes + size

            tokens = 0
            if max_tokens is not None and token_counter is not None:
                tokens = file_info.get('tokens')
                if tokens is None:
                    tokens = Merger._count_tokens_for_file(file_info['path'], token_counter)
                    file_info['tokens'] = tokens
            next_tokens = total_tokens + tokens

            if max_bytes is not None and next_bytes > max_bytes:
                truncated = True
                reason = 'max_bytes'
                break
            if max_tokens is not None and next_tokens > max_tokens:
                truncated = True
                reason = 'max_tokens'
                break

            accepted.append(file_info)
            total_bytes = next_bytes
            total_tokens = next_tokens

        return accepted, truncated, reason

    @staticmethod
    def _count_tokens_for_file(file_path: str, token_counter) -> int:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return token_counter.count(f.read())
        except (OSError, UnicodeDecodeError):
            return 0

    def _write_output(
        self,
        *,
        target_files: List[Dict],
        target_dir: str,
        output_file: Optional[str],
        to_stdout: bool,
        enable_sanitize: bool,
        custom_replacements: Optional[List],
        head_lines: Optional[int],
        tail_lines: Optional[int],
        root_dir: Optional[str],
        grep_pattern: Optional[List[str]],
        grep_context: int,
        grep_regex: bool,
        grep_ignore_case: bool,
        include_outline: bool,
        outline_patterns: Optional[Dict[str, List[str]]],
        include_tree: bool,
        include_list: bool,
        include_stats: bool,
        include_merge: bool,
        tree_structure: Optional[str],
        list_structure: Optional[str],
        absolute_paths: bool,
        diff_text: Optional[str],
        render_context: Dict[str, Any],
    ) -> None:
        """出力を書き込む"""
        if to_stdout:
            print("Merging...", file=sys.stderr)
        else:
            print("Merging...")

        content, sanitize_stats = self.generator.generate(
            target_files,
            target_dir,
            enable_sanitize,
            custom_replacements,
            head_lines,
            tail_lines,
            root_dir,
            grep_pattern,
            grep_context,
            grep_regex,
            grep_ignore_case,
            include_outline,
            outline_patterns,
            include_tree,
            include_list,
            include_stats,
            include_merge,
            tree_structure,
            list_structure,
            absolute_paths,
            diff_text,
            render_context,
        )

        if to_stdout:
            print(content)
            print(f"Done! {len(target_files)} files merged", file=sys.stderr)
            if sanitize_stats:
                print("\nSanitization stats:", file=sys.stderr)
                for key, count in sanitize_stats.items():
                    print(f"  {key}: {count}", file=sys.stderr)
        else:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"\nDone! {len(target_files)} files merged into '{output_file}'")
                if sanitize_stats:
                    print("\nSanitization stats:")
                    for key, count in sanitize_stats.items():
                        print(f"  {key}: {count}")
            except PermissionError:
                print(f"\nError: Permission denied writing to '{output_file}'", file=sys.stderr)
                print("Check that you have write permissions for this location.", file=sys.stderr)
                sys.exit(1)
            except OSError as e:
                print(f"\nError: Cannot write to '{output_file}': {e}", file=sys.stderr)
                sys.exit(1)
