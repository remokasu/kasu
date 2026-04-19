"""テキスト形式のジェネレータ"""
import sys
import os
import re
from typing import List, Dict, Tuple, Optional

from generators.base import ContentGenerator
from sanitizers.sanitizer import Sanitizer
from utils.statistics import Statistics
from utils.path_utils import format_display_path
from utils.format_utils import format_size
from utils.outline import OutlineExtractor


class TextGenerator(ContentGenerator):
    """プレーンテキスト形式でコンテンツを生成"""

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
        list_structure: Optional[str] = None
    ) -> Tuple[str, Dict[str, int]]:
        """テキスト形式でコンテンツを生成"""
        content_parts = []
        all_stats = {}

        sanitizer = Sanitizer(enable_sanitize, custom_replacements)

        # ベースディレクトリ名を取得
        base_name = os.path.basename(os.path.abspath(target_dir))

        # # プロジェクト名
        # project_name = os.path.basename(os.path.abspath(target_dir))

        # 統計情報
        if include_stats:
            stats = Statistics.calculate(target_files)
            content_parts.append("=== Statistics ===\n")
            content_parts.append(f"Total files: {stats['total_files']:,}\n")
            content_parts.append(f"Total lines: {stats['total_lines']:,}\n")
            content_parts.append(f"Total size: {format_size(stats['total_size'])}\n")
            
            if stats['by_extension']:
                content_parts.append("\nBy extension:\n")
                sorted_exts = sorted(
                    stats['by_extension'].items(),
                    key=lambda x: x[1]['count'],
                    reverse=True
                )
                for ext, ext_stats in sorted_exts:
                    content_parts.append(
                        f"  {ext:15} {ext_stats['count']:4} files  "
                        f"{ext_stats['lines']:6,} lines  "
                        f"{format_size(ext_stats['size']):>10}\n"
                    )
            
            content_parts.append("\n")

        # ディレクトリツリー
        if include_tree and tree_structure:
            content_parts.append("=== Directory Structure ===\n")
            content_parts.append(tree_structure)
            if not tree_structure.endswith('\n'):
                content_parts.append('\n')
            content_parts.append("\n")

        # ファイル一覧
        if include_list and list_structure:
            content_parts.append("=== File List ===\n")
            content_parts.append(list_structure)
            if not list_structure.endswith('\n'):
                content_parts.append('\n')
            content_parts.append("\n")

        # アウトライン
        if include_outline:
            default_patterns = OutlineExtractor.load_default_patterns()
            outline_content, outline_stats = self._build_outline(
                target_files,
                target_dir,
                root_dir,
                default_patterns,
                outline_patterns,
                sanitizer
            )
            for key, count in outline_stats.items():
                all_stats[key] = all_stats.get(key, 0) + count
            if outline_content:
                content_parts.append("=== Outline ===\n")
                content_parts.append(outline_content)
                if not outline_content.endswith('\n'):
                    content_parts.append('\n')
                content_parts.append("\n")

        # ファイル結合
        if include_merge:
            content_parts.append("=== Files ===\n\n")
            for file_info in target_files:
                file_path = file_info['path']
                display_path = format_display_path(
                    file_path,
                    target_dir,
                    root_dir=root_dir,
                    leading_slash=True
                )

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()

                    lines = file_content.splitlines()

                    # grep 処理
                    if isinstance(grep_pattern, str):
                        grep_pattern = [grep_pattern]
                    if grep_pattern:
                        matched_ranges = self._find_grep_ranges(
                            lines,
                            grep_pattern,
                            grep_context,
                            grep_regex,
                            grep_ignore_case
                        )
                        if not matched_ranges:
                            continue

                        for start, end in matched_ranges:
                            range_label = f"{start + 1}" if start == end else f"{start + 1}-{end + 1}"
                            content_parts.append(f"--- {display_path}:{range_label} ---\n")
                            block_lines, block_stats = self._format_block(
                                lines,
                                start,
                                end,
                                sanitizer
                            )
                            for key, count in block_stats.items():
                                all_stats[key] = all_stats.get(key, 0) + count
                            content_parts.append(block_lines)
                            content_parts.append('\n')
                        content_parts.append('\n')
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

                    content_parts.append(f"--- {display_path} ---\n")
                    content_parts.append(file_content)
                    content_parts.append('\n\n')
                except UnicodeDecodeError:
                    content_parts.append(f"[Error: Cannot decode file {file_path} as text]\n\n")
                    print(f"Warning: Failed to read {file_path} (encoding issue)", file=sys.stderr)
                except PermissionError:
                    content_parts.append(f"[Error: Permission denied reading {file_path}]\n\n")
                    print(f"Warning: Permission denied reading {file_path}", file=sys.stderr)
                except Exception as e:
                    content_parts.append(f"[Error reading {file_path}: {e}]\n\n")
                    print(f"Warning: Failed to read {file_path}: {e}", file=sys.stderr)

        return ''.join(content_parts), all_stats

    @staticmethod
    def _build_outline(
        target_files: List[Dict[str, any]],
        target_dir: str,
        root_dir: Optional[str],
        default_patterns: Dict[str, List[str]],
        outline_patterns: Optional[Dict[str, List[str]]],
        sanitizer: Sanitizer
    ) -> Tuple[str, Dict[str, int]]:
        parts: List[str] = []
        all_stats: Dict[str, int] = {}

        for file_info in target_files:
            file_path = file_info['path']
            display_path = format_display_path(
                file_path,
                target_dir,
                root_dir=root_dir,
                leading_slash=True
            )

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.read().splitlines()
            except Exception:
                continue

            entries = OutlineExtractor.extract(file_path, lines, default_patterns, outline_patterns)
            if not entries:
                continue

            max_line = max(line_no for line_no, _ in entries)
            width = len(str(max_line))
            parts.append(f"--- {display_path} ---\n")
            for line_no, text in entries:
                safe_text, stats = sanitizer.sanitize(text)
                for key, count in stats.items():
                    all_stats[key] = all_stats.get(key, 0) + count
                parts.append(f"{line_no:>{width}} | {safe_text}\n")
            parts.append("\n")

        return ''.join(parts).rstrip(), all_stats

    @staticmethod
    def _find_grep_ranges(
        lines: List[str],
        patterns: List[str],
        context: int,
        use_regex: bool,
        ignore_case: bool
    ) -> List[Tuple[int, int]]:
        if context < 0:
            context = 0

        match_lines = []
        if use_regex:
            flags = re.IGNORECASE if ignore_case else 0
            regexes = [re.compile(pattern, flags) for pattern in patterns]
            for i, line in enumerate(lines):
                if any(regex.search(line) for regex in regexes):
                    match_lines.append(i)
        else:
            if ignore_case:
                needles = [pattern.lower() for pattern in patterns]
                for i, line in enumerate(lines):
                    lower = line.lower()
                    if any(needle in lower for needle in needles):
                        match_lines.append(i)
            else:
                for i, line in enumerate(lines):
                    if any(pattern in line for pattern in patterns):
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
