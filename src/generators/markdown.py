"""Markdown形式のジェネレータ"""
import os
import sys
import re
from typing import List, Dict, Tuple, Optional

from generators.base import ContentGenerator
from sanitizers.sanitizer import Sanitizer
from utils.language_map import LanguageMapper
from utils.path_utils import format_display_path
from utils.format_utils import format_size


class MarkdownGenerator(ContentGenerator):
    """Markdown形式でコンテンツを生成"""

    def __init__(self):
        """初期化"""
        pass

    def generate(
        self,
        target_files: List[Dict[str, any]],
        target_dir: str,
        enable_sanitize: bool = False,
        custom_replacements: Optional[List[Tuple[str, str]]] = None,
        head_lines: Optional[int] = None,
        tail_lines: Optional[int] = None,
        root_dir: Optional[str] = None,
        grep_pattern: Optional[str] = None,
        grep_context: int = 3,
        grep_regex: bool = False,
        grep_ignore_case: bool = False,
        include_tree: bool = False,
        include_list: bool = False,
        include_stats: bool = False,
        include_merge: bool = True,
        tree_structure: Optional[str] = None,
        list_structure: Optional[str] = None
    ) -> Tuple[str, Dict[str, int]]:
        """
        Markdown形式でコンテンツを生成

        Args:
            target_files: ファイル情報のリスト
            target_dir: ターゲットディレクトリ
            enable_sanitize: サニタイズを有効にするか
            custom_replacements: カスタム置換パターン
            head_lines: 各ファイルの先頭N行のみ
            tail_lines: 各ファイルの末尾N行のみ
            include_tree: ツリー構造を含めるか
            include_stats: 統計情報を含めるか
            include_merge: ファイル結合を含めるか
            tree_structure: ツリー構造文字列

        Returns:
            (生成されたMarkdownコンテンツ, サニタイズ統計)
        """
        content_parts = []
        all_stats = {}

        sanitizer = Sanitizer(enable_sanitize, custom_replacements)

        # サマリー統計
        if include_stats:
            total_size = sum(f['size'] for f in target_files)
            total_lines = sum(f['lines'] for f in target_files)

            content_parts.append("## Summary\n\n")
            content_parts.append(f"- **Total files**: {len(target_files)}\n")
            content_parts.append(f"- **Total lines**: {total_lines:,}\n")
            content_parts.append(f"- **Total size**: {format_size(total_size)}\n\n")

            # 拡張子別の統計
            ext_stats = self._calculate_extension_stats(target_files)
            if ext_stats:
                content_parts.append("### By Extension\n\n")
                content_parts.append("| Extension | Files | Lines | Size |\n")
                content_parts.append("|-----------|-------|-------|------|\n")
                for ext, stats in sorted(ext_stats.items(), key=lambda x: x[1]['count'], reverse=True):
                    content_parts.append(
                        f"| {ext} | {stats['count']} | {stats['lines']:,} | {format_size(stats['size'])} |\n"
                    )
                content_parts.append("\n")

            content_parts.append("---\n\n")

        # ディレクトリ構造（ツリー）
        if include_tree and tree_structure:
            content_parts.append("## Directory Structure\n\n")
            content_parts.append("```\n")
            content_parts.append(tree_structure)
            if not tree_structure.endswith('\n'):
                content_parts.append('\n')
            content_parts.append("```\n\n")
            content_parts.append("---\n\n")

        # ファイル一覧
        if include_list and list_structure:
            content_parts.append("## File List\n\n")
            content_parts.append("```\n")
            content_parts.append(list_structure)
            if not list_structure.endswith('\n'):
                content_parts.append('\n')
            content_parts.append("```\n\n")
            content_parts.append("---\n\n")

        # 各ファイルの内容
        if include_merge:
            content_parts.append("## Files\n\n")

            for file_info in target_files:
                file_path = file_info['path']
                display_path = format_display_path(
                    file_path,
                    target_dir,
                    root_dir=root_dir,
                    leading_slash=True
                )

                language = LanguageMapper.get_language(file_path)

                # ファイル名をヘッダーに
                content_parts.append(f"### `{display_path}`\n\n")

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()

                    lines = file_content.split('\n')

                    # grep 処理
                    if grep_pattern:
                        matched_ranges = self._find_grep_ranges(
                            lines,
                            grep_pattern,
                            grep_context,
                            grep_regex,
                            grep_ignore_case
                        )
                        if not matched_ranges:
                            # ファイル内にヒットなし
                            content_parts.pop()  # ファイルヘッダーを取り消し
                            continue

                        for start, end in matched_ranges:
                            range_label = f"{start + 1}" if start == end else f"{start + 1}-{end + 1}"
                            content_parts.append(f"#### `{display_path}:{range_label}`\n\n")
                            block_lines, block_stats = self._format_block(
                                lines,
                                start,
                                end,
                                sanitizer
                            )
                            for key, count in block_stats.items():
                                all_stats[key] = all_stats.get(key, 0) + count
                            content_parts.append("```text\n")
                            content_parts.append(block_lines)
                            content_parts.append("\n```\n\n")
                        continue

                    # head/tail 処理
                    if head_lines is not None:
                        lines = lines[:head_lines]
                        file_content = '\n'.join(lines)
                        if len(lines) == head_lines and file_content:
                            file_content += "\n... (truncated)\n"
                    elif tail_lines is not None:
                        lines = lines[-tail_lines:]
                        file_content = "... (truncated)\n" + '\n'.join(lines)

                    # サニタイズ
                    file_content, stats = sanitizer.sanitize(file_content)
                    for key, count in stats.items():
                        all_stats[key] = all_stats.get(key, 0) + count

                    # コードブロック
                    content_parts.append(f"```{language}\n")
                    content_parts.append(file_content)
                    if not file_content.endswith('\n'):
                        content_parts.append('\n')
                    content_parts.append("```\n\n")
                except UnicodeDecodeError:
                    content_parts.append(f"```text\n[Error: Cannot decode file {file_path} as text]\n```\n\n")
                    print(f"Warning: Failed to read {file_path} (encoding issue)", file=sys.stderr)
                except PermissionError:
                    content_parts.append(f"```text\n[Error: Permission denied reading {file_path}]\n```\n\n")
                    print(f"Warning: Permission denied reading {file_path}", file=sys.stderr)
                except Exception as e:
                    content_parts.append(f"```text\n[Error reading {file_path}: {e}]\n```\n\n")
                    print(f"Warning: Failed to read {file_path}: {e}", file=sys.stderr)

        return ''.join(content_parts), all_stats

    @staticmethod
    def _find_grep_ranges(
        lines: List[str],
        pattern: str,
        context: int,
        use_regex: bool,
        ignore_case: bool
    ) -> List[Tuple[int, int]]:
        if context < 0:
            context = 0

        match_lines = []
        if use_regex:
            flags = re.IGNORECASE if ignore_case else 0
            regex = re.compile(pattern, flags)
            for i, line in enumerate(lines):
                if regex.search(line):
                    match_lines.append(i)
        else:
            if ignore_case:
                needle = pattern.lower()
                for i, line in enumerate(lines):
                    if needle in line.lower():
                        match_lines.append(i)
            else:
                for i, line in enumerate(lines):
                    if pattern in line:
                        match_lines.append(i)

        if not match_lines:
            return []

        ranges = []
        for i in match_lines:
            start = max(0, i - context)
            end = min(len(lines) - 1, i + context)
            if not ranges or start > ranges[-1][1] + 1:
                ranges.append([start, end])
            else:
                ranges[-1][1] = max(ranges[-1][1], end)

        return [(r[0], r[1]) for r in ranges]

    @staticmethod
    def _format_block(
        lines: List[str],
        start: int,
        end: int,
        sanitizer: Sanitizer
    ) -> Tuple[str, Dict[str, int]]:
        width = len(str(end + 1))
        rendered = []
        stats: Dict[str, int] = {}
        for idx in range(start, end + 1):
            line = lines[idx]
            line, line_stats = sanitizer.sanitize(line)
            for key, count in line_stats.items():
                stats[key] = stats.get(key, 0) + count
            rendered.append(f"{idx + 1:>{width}} | {line}")

        return "\n".join(rendered), stats

    def _calculate_extension_stats(self, target_files: List[Dict[str, any]]) -> Dict[str, Dict]:
        """拡張子別の統計を計算"""
        stats = {}
        for file_info in target_files:
            ext = os.path.splitext(file_info['path'])[1] or '(no extension)'
            if ext not in stats:
                stats[ext] = {'count': 0, 'lines': 0, 'size': 0}
            stats[ext]['count'] += 1
            stats[ext]['lines'] += file_info['lines']
            stats[ext]['size'] += file_info['size']
        return stats
