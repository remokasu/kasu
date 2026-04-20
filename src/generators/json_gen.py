"""JSON形式のジェネレータ

SPEC-0001 FR-1 / ADR-0003 に従い、``schema_version: "1.0"`` を
必須とする構造化出力を生成する。
"""
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

from generators.base import ContentGenerator
from sanitizers.sanitizer import Sanitizer
from utils.language_map import LanguageMapper
from utils.outline import OutlineExtractor
from utils.path_utils import format_display_path
from utils.statistics import Statistics

SCHEMA_VERSION = "1.0"


class JsonGenerator(ContentGenerator):
    """SPEC-0001 FR-1 のスキーマに従う JSON 出力を生成

    Notes:
        - ``files[].content`` は ``include_merge=False`` または
          ``render_context['dry_run']=True`` の時 ``None`` を入れる
          （キーは常に存在、ADR-0003）。
        - ``files[].tokens`` は ``token_counter`` が渡されれば正確に、
          無ければ 0 を入れる。
    """

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
        ctx = render_context or {}
        token_counter = ctx.get('token_counter')
        dry_run = bool(ctx.get('dry_run'))
        truncated = bool(ctx.get('truncated'))
        truncate_reason = ctx.get('truncate_reason')
        kasu_version = ctx.get('kasu_version', '0.0.0')
        generated_at = ctx.get('generated_at')
        cli_options = ctx.get('cli_options', {})

        sanitizer = Sanitizer(enable_sanitize and not dry_run, custom_replacements if not dry_run else None)
        all_stats: Dict[str, int] = {}

        emit_content = include_merge and not dry_run

        files_output: List[Dict[str, Any]] = []
        if isinstance(grep_pattern, str):
            grep_pattern = [grep_pattern]

        for file_info in target_files:
            file_path = file_info['path']
            abs_path = os.path.abspath(file_path)
            rel_path = format_display_path(
                file_path,
                target_dir,
                root_dir=root_dir,
                leading_slash=False,
            )

            file_entry: Dict[str, Any] = {
                'path': rel_path,
                'absolute_path': abs_path,
                'size': file_info.get('size', 0),
                'lines': file_info.get('lines', 0),
                'tokens': 0,
                'encoding': 'utf-8',
                'language': LanguageMapper.get_language(file_path),
                'content': None,
                'truncated': False,
            }

            raw_content: Optional[str] = None
            if emit_content:
                raw_content, read_error = self._read_file(file_path)
                if read_error:
                    file_entry['content'] = f"[Error: {read_error}]"
                    files_output.append(file_entry)
                    continue

            if emit_content and raw_content is not None:
                rendered, file_truncated, stats = self._render_content(
                    raw_content,
                    grep_pattern,
                    grep_context,
                    grep_regex,
                    grep_ignore_case,
                    head_lines,
                    tail_lines,
                    sanitizer,
                )
                for key, count in stats.items():
                    all_stats[key] = all_stats.get(key, 0) + count

                if rendered is None:
                    continue  # grep hit なし

                file_entry['content'] = rendered
                file_entry['truncated'] = file_truncated

            if token_counter is not None:
                if raw_content is not None:
                    file_entry['tokens'] = token_counter.count(raw_content)
                else:
                    file_entry['tokens'] = self._count_file_tokens(file_path, token_counter)

            files_output.append(file_entry)

        # stats 計算
        stats_obj: Optional[Dict[str, Any]] = None
        if include_stats:
            stats_obj = Statistics.calculate(target_files, token_counter=token_counter)

        # outline 抽出
        outline_obj: Optional[Dict[str, List[Dict[str, Any]]]] = None
        if include_outline:
            default_patterns = OutlineExtractor.load_default_patterns()
            outline_obj, outline_stats = self._build_outline(
                target_files,
                target_dir,
                root_dir,
                default_patterns,
                outline_patterns,
                sanitizer,
                absolute_paths,
            )
            for key, count in outline_stats.items():
                all_stats[key] = all_stats.get(key, 0) + count

        total_bytes = sum(f.get('size', 0) for f in target_files)
        total_lines = sum(f.get('lines', 0) for f in target_files)
        total_tokens = sum(f.get('tokens', 0) for f in files_output)

        meta: Dict[str, Any] = {
            'schema_version': SCHEMA_VERSION,
            'kasu_version': kasu_version,
            'target_dir': os.path.abspath(target_dir),
            'root_dir': root_dir,
            'generated_at': generated_at,
            'total_files': len(target_files),
            'total_bytes': total_bytes,
            'total_lines': total_lines,
            'total_tokens': total_tokens,
            'token_method': token_counter.method if token_counter is not None else None,
            'truncated': truncated,
            'truncate_reason': truncate_reason,
            'dry_run': dry_run,
            'options': cli_options,
        }

        output: Dict[str, Any] = {
            'meta': meta,
            'tree': tree_structure if include_tree else None,
            'stats': stats_obj,
            'outline': outline_obj,
            'diff': diff_text,
            'files': files_output,
            'sanitize_stats': all_stats,
        }

        return json.dumps(output, indent=2, ensure_ascii=False), all_stats

    @staticmethod
    def _read_file(file_path: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(), None
        except UnicodeDecodeError:
            return None, f"Cannot decode file {file_path} as text"
        except PermissionError:
            return None, f"Permission denied reading {file_path}"
        except OSError as e:
            return None, f"Cannot read {file_path}: {e}"

    @staticmethod
    def _count_file_tokens(file_path: str, token_counter) -> int:
        content, _ = JsonGenerator._read_file(file_path)
        if content is None:
            return 0
        return token_counter.count(content)

    @staticmethod
    def _render_content(
        file_content: str,
        grep_pattern: Optional[List[str]],
        grep_context: int,
        grep_regex: bool,
        grep_ignore_case: bool,
        head_lines: Optional[int],
        tail_lines: Optional[int],
        sanitizer: Sanitizer,
    ) -> Tuple[Optional[str], bool, Dict[str, int]]:
        lines = file_content.splitlines()
        stats: Dict[str, int] = {}
        truncated = False

        if grep_pattern:
            matched_ranges = JsonGenerator._find_grep_ranges(
                lines, grep_pattern, grep_context, grep_regex, grep_ignore_case
            )
            if not matched_ranges:
                return None, False, stats
            blocks: List[str] = []
            for start, end in matched_ranges:
                block_str, block_stats = JsonGenerator._format_block(
                    lines, start, end, sanitizer
                )
                for k, v in block_stats.items():
                    stats[k] = stats.get(k, 0) + v
                blocks.append(block_str)
            return "\n".join(blocks), False, stats

        if head_lines is not None:
            if len(lines) > head_lines:
                lines = lines[:head_lines]
                truncated = True
            file_content = "\n".join(lines)
        elif tail_lines is not None:
            if len(lines) > tail_lines:
                lines = lines[-tail_lines:]
                truncated = True
            file_content = "\n".join(lines)

        sanitized, sanitize_stats = sanitizer.sanitize(file_content)
        for k, v in sanitize_stats.items():
            stats[k] = stats.get(k, 0) + v
        return sanitized, truncated, stats

    @staticmethod
    def _find_grep_ranges(
        lines: List[str],
        patterns: List[str],
        context: int,
        use_regex: bool,
        ignore_case: bool,
    ) -> List[Tuple[int, int]]:
        if context < 0:
            context = 0

        match_lines: List[int] = []
        if use_regex:
            flags = re.IGNORECASE if ignore_case else 0
            regexes = [re.compile(p, flags) for p in patterns]
            for i, line in enumerate(lines):
                if any(r.search(line) for r in regexes):
                    match_lines.append(i)
        else:
            if ignore_case:
                needles = [p.lower() for p in patterns]
                for i, line in enumerate(lines):
                    lower = line.lower()
                    if any(n in lower for n in needles):
                        match_lines.append(i)
            else:
                for i, line in enumerate(lines):
                    if any(p in line for p in patterns):
                        match_lines.append(i)

        if not match_lines:
            return []

        ranges: List[List[int]] = []
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
        sanitizer: Sanitizer,
    ) -> Tuple[str, Dict[str, int]]:
        width = len(str(end + 1))
        rendered: List[str] = []
        stats: Dict[str, int] = {}
        for idx in range(start, end + 1):
            line = lines[idx]
            line, line_stats = sanitizer.sanitize(line)
            for k, v in line_stats.items():
                stats[k] = stats.get(k, 0) + v
            rendered.append(f"{idx + 1:>{width}} | {line}")
        return "\n".join(rendered), stats

    @staticmethod
    def _build_outline(
        target_files: List[Dict[str, any]],
        target_dir: str,
        root_dir: Optional[str],
        default_patterns: Dict[str, List[str]],
        outline_patterns: Optional[Dict[str, List[str]]],
        sanitizer: Sanitizer,
        absolute_paths: bool,
    ) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
        outline: Dict[str, List[Dict[str, Any]]] = {}
        all_stats: Dict[str, int] = {}

        for file_info in target_files:
            file_path = file_info['path']
            if absolute_paths:
                display_path = os.path.abspath(file_path)
            else:
                display_path = format_display_path(
                    file_path, target_dir, root_dir=root_dir, leading_slash=False
                )

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.read().splitlines()
            except (OSError, UnicodeDecodeError):
                continue

            entries = OutlineExtractor.extract(file_path, lines, default_patterns, outline_patterns)
            if not entries:
                continue

            outline[display_path] = []
            for line_no, text in entries:
                safe_text, stats = sanitizer.sanitize(text)
                for k, v in stats.items():
                    all_stats[k] = all_stats.get(k, 0) + v
                outline[display_path].append({'line': line_no, 'text': safe_text})

        return outline, all_stats
