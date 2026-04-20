import argparse
import datetime
import sys
import os

from core.config import ConfigLoader
from core.file_scanner import FileScanner
from core.merger import Merger
from utils.exceptions import (
    KasuGitNotFoundError,
    KasuInvalidGitRefError,
    KasuNotAGitRepoError,
)
from generators.text import TextGenerator
from generators.markdown import MarkdownGenerator
from generators.json_gen import JsonGenerator
from filters.ignore import IgnoreFilter
from filters.glob import GlobFilter
from sanitizers.sanitizer import Sanitizer
from utils.git import GitIntegration
from utils.tokenizer import TokenCounter
from utils.tree import TreeBuilder
from utils.list import ListBuilder

KASU_VERSION = "0.0.8"


def main():
    parser = argparse.ArgumentParser(
        description="Merge all text files in a directory into one output.",
        epilog="Examples:\n"
               "  ks -i . -o output.txt                       # Basic merge\n"
               "  ks -i . -o output.md -f md                  # Markdown format\n"
               "  ks -i . -o output.json -f json              # JSON format (agent-friendly)\n"
               "  ks -i . -o output.txt -t                    # With tree\n"
               "  ks -i . -o output.txt --head 100            # First 100 lines per file\n"
               "  ks -i . -o output.txt --tail 50             # Last 50 lines per file\n"
               "  ks -i . -t                                  # Display tree only\n"
               "  ks -i . -o output.txt -t --no-merge         # Tree only (no files)\n"
               "  ks -i . -o output.txt -g '*.py' '*.js'      # Python and JS only\n"
               "  ks -i . -o output.txt -g 'src/**/*.py'      # Recursive pattern\n"
               "  ks -i . -o output.txt -x 'README.md'        # Exclude specific files\n"
               "  ks -i . -o output.txt -g '*.py' -x 'test_*' # Combine glob and exclude\n"
               "  ks -i project/ -o out.txt -s                # Auto-sanitize sensitive info\n"
               "  ks -i . -f json --since HEAD~3              # Files changed since HEAD~3\n"
               "  ks -i . -f markdown --diff main             # Include git diff vs main\n"
               "  ks -i . --dry-run                           # Preview files without content\n"
               "  ks -i . -f json --token-count --max-tokens 100000 # Bound output for LLM context\n"
               "  ks --config config.yaml                     # Use config file\n"
               "  ks -c config.yaml -o custom.txt             # Config + override\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 入出力オプション
    io_group = parser.add_argument_group('Input/Output')
    io_group.add_argument(
        "--input", "-i",
        dest="target_dir",
        metavar="DIR",
        help="Directory to search for text files"
    )
    io_group.add_argument(
        "--root",
        dest="root_dir",
        metavar="DIR",
        help="Display root directory for paths"
    )
    io_group.add_argument(
        "--output", "-o",
        dest="output_file",
        metavar="FILE",
        help="Output file path"
    )
    io_group.add_argument(
        "--stdout",
        action="store_true",
        help="Output to stdout instead of file"
    )
    io_group.add_argument(
        "--format", "-f",
        choices=['text', 'markdown', 'md', 'json'],
        default='text',
        help="Output format (default: text)"
    )
    io_group.add_argument(
        "--absolute-paths",
        dest="absolute_paths",
        action="store_true",
        help="Emit file paths as absolute paths (useful for agents)"
    )

    # 情報追加オプション
    include_group = parser.add_argument_group('Information inclusion options')
    include_group.add_argument(
        "--tree", "-t",
        action="store_true",
        help="Include directory tree structure"
    )
    include_group.add_argument(
        "--list", "-l",
        action="store_true",
        help="Include file list"
    )

    include_group.add_argument(
        "--stats",
        action="store_true",
        help="Include file statistics"
    )

    include_group.add_argument(
        "--outline",
        action="store_true",
        help="Include outline extracted from files"
    )

    include_group.add_argument(
        "--token-count",
        dest="token_count",
        action="store_true",
        help="Include token count (uses tiktoken if installed, else approximation)"
    )


    # 除外オプション
    exclude_group = parser.add_argument_group('Exclusion options')
    exclude_group.add_argument(
        "--no-merge",
        action="store_true",
        dest="no_merge",
        help="Exclude file contents (only output metadata)"
    )

    # フィルタリングオプション
    filter_group = parser.add_argument_group('Filtering options')
    filter_group.add_argument(
        "--glob", "-g",
        nargs='+',
        metavar="PATTERN",
        help="File patterns to match (e.g., '*.py' 'src/**/*.js'). Supports glob wildcards."
    )
    filter_group.add_argument(
        "--ignore",
        metavar="FILE",
        dest="ignore_file",
        help="Ignore patterns file (default: auto-detect .gitignore)"
    )
    filter_group.add_argument(
        "--exclude", "-x",
        nargs='+',
        metavar="PATTERN",
        help="Exclude patterns (e.g., 'README.md' '*.log' 'temp/*')"
    )
    filter_group.add_argument(
        "--head",
        type=int,
        metavar="N",
        help="Limit each file to first N lines"
    )
    filter_group.add_argument(
        "--tail",
        type=int,
        metavar="N",
        help="Limit each file to last N lines"
    )
    filter_group.add_argument(
        "--no-auto-ignore",
        action="store_true",
        help="Disable automatic .gitignore detection"
    )
    filter_group.add_argument(
        "--since",
        dest="since",
        metavar="REF",
        help="Only include files changed since the given git ref (e.g., HEAD~3, main)"
    )
    filter_group.add_argument(
        "--max-tokens",
        dest="max_tokens",
        type=int,
        metavar="N",
        help="Truncate output when total tokens exceed N (file-level truncation)"
    )
    filter_group.add_argument(
        "--max-bytes",
        dest="max_bytes",
        type=int,
        metavar="N",
        help="Truncate output when total bytes exceed N (file-level truncation)"
    )

    # 検索オプション
    search_group = parser.add_argument_group('Search options')
    search_group.add_argument(
        "--grep",
        dest="grep_pattern",
        action="append",
        metavar="PATTERN",
        help="Extract lines matching pattern with surrounding context"
    )
    search_group.add_argument(
        "--context",
        dest="grep_context",
        type=int,
        default=None,
        metavar="N",
        help="Lines of context to include before/after matches (default: 3)"
    )
    search_group.add_argument(
        "--ignore-case",
        dest="grep_ignore_case",
        action="store_true",
        help="Case-insensitive search for --grep"
    )
    search_group.add_argument(
        "--regex",
        dest="grep_regex",
        action="store_true",
        help="Treat --grep as a regular expression"
    )
    search_group.add_argument(
        "--diff",
        dest="diff_ref",
        metavar="REF",
        help="Include 'git diff <REF>...HEAD' output as a section"
    )

    # サニタイズオプション
    sanitize_group = parser.add_argument_group('Sanitization options')
    sanitize_group.add_argument(
        "--sanitize", "-s",
        action="store_true",
        help="Auto-sanitize sensitive information"
    )
    sanitize_group.add_argument(
        "--replace", "-r",
        dest="replace_file",
        metavar="FILE",
        help="Custom replacement patterns file"
    )

    # 実行制御オプション
    control_group = parser.add_argument_group('Execution control')
    control_group.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Skip confirmation prompt"
    )
    control_group.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Show debug information"
    )
    control_group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Preview target files and sizes without emitting file content"
    )

    # その他
    parser.add_argument(
        "--config", "-c",
        metavar="FILE",
        dest="config_file",
        help="Configuration file path (YAML format)"
    )
    parser.add_argument(
        "--outline-config",
        metavar="FILE",
        dest="outline_config",
        help="Outline patterns configuration file (YAML format)"
    )

    args = parser.parse_args()

    # 設定ファイルを読み込み
    config = ConfigLoader.load(args.config_file)
    args = ConfigLoader.merge_with_args(config, args)

    outline_patterns = None
    if getattr(args, 'outline_patterns', None):
        outline_patterns = args.outline_patterns

    if args.outline_config:
        if not os.path.exists(args.outline_config):
            print(f"Warning: Outline config file not found: {args.outline_config}", file=sys.stderr)
        else:
            from utils.outline import OutlineExtractor
            loaded_patterns = OutlineExtractor.load_patterns(args.outline_config)
            if outline_patterns:
                for key, value in loaded_patterns.items():
                    outline_patterns.setdefault(key, [])
                    outline_patterns[key].extend(value)
            else:
                outline_patterns = loaded_patterns

    if args.grep_context is None:
        args.grep_context = 3

    # target_dirのチェック（設定ファイルマージ後に実施）
    if not args.target_dir:
        parser.error("--input/-i is required (either via command line or config file)")

    # 表示のみモード（tree, stats, list のいずれか）
    display_only_mode = (args.tree or args.stats or args.list) \
                        and not args.output_file and not args.stdout \
                        and not args.dry_run

    # dry_run は必ず出力先が要る
    if args.dry_run and not args.output_file and not args.stdout:
        parser.error("--dry-run requires --output/-o or --stdout")

    # output_fileチェック
    if not args.stdout and not display_only_mode and not args.output_file:
        parser.error("--output/-o is required unless using --stdout, --tree, or --stats")

    # 出力ファイルパスが空文字列でないかチェック
    if args.output_file is not None and args.output_file.strip() == "":
        parser.error("Output file path cannot be empty")

    # --head と --tail の排他チェック
    if args.head and args.tail:
        parser.error("Cannot use both --head and --tail at the same time")

    # --absolute-paths と --root の排他チェック
    if args.absolute_paths and args.root_dir:
        parser.error("Cannot use --absolute-paths with --root")

    # target_dirが存在するかチェック
    if not os.path.exists(args.target_dir):
        parser.error(f"Input directory does not exist: {args.target_dir}")

    if not os.path.isdir(args.target_dir):
        parser.error(f"Input path is not a directory: {args.target_dir}")

    # フォーマットの正規化
    if args.format == 'md':
        args.format = 'markdown'

    # Ignoreファイルの決定
    ignore_files = []
    exclude_patterns = []
    auto_vcs_ignore = False

    if args.ignore_file:
        if not os.path.exists(args.ignore_file):
            print(f"Warning: Ignore file not found: {args.ignore_file}", file=sys.stderr)
        else:
            ignore_files.append(args.ignore_file)
            if args.debug:
                print(f"[DEBUG] Using specified ignore file: {args.ignore_file}", file=sys.stderr)

    if not args.no_auto_ignore and not args.ignore_file:
        auto_ignore = IgnoreFilter.auto_detect_ignore_file(args.target_dir)
        if auto_ignore:
            ignore_files.append(auto_ignore)
            auto_vcs_ignore = True
            print(f"Auto-detected and using: {auto_ignore}")

    if args.exclude:
        exclude_patterns = args.exclude
        if args.debug:
            print(f"[DEBUG] Exclude patterns: {exclude_patterns}", file=sys.stderr)

    # フィルタの構築
    filters = []
    ignore_filter = None
    glob_filter = None

    glob_filter = GlobFilter(args.glob, args.target_dir, args.debug)
    filters.append(glob_filter)

    ignore_patterns = []
    if ignore_files:
        ignore_patterns = IgnoreFilter.load_patterns_from_multiple(ignore_files)
    if exclude_patterns:
        ignore_patterns.extend(exclude_patterns)

    if ignore_patterns:
        ignore_filter = IgnoreFilter(ignore_patterns, args.target_dir, args.debug, auto_vcs_ignore)
        filters.append(ignore_filter)
    else:
        ignore_filter = IgnoreFilter([], args.target_dir, args.debug, auto_vcs_ignore)
        filters.append(ignore_filter)

    scanner = FileScanner(filters, args.debug)

    # Git 連携（--since / --diff）
    git_integration = None
    since_paths = None
    diff_text = None
    if args.since or args.diff_ref:
        try:
            git_integration = GitIntegration(args.target_dir)
        except (KasuGitNotFoundError, KasuNotAGitRepoError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(2)

        if args.since:
            try:
                since_paths = git_integration.list_changed_files(args.since)
            except KasuInvalidGitRefError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(2)

        if args.diff_ref:
            try:
                diff_text = git_integration.get_diff(args.diff_ref)
            except KasuInvalidGitRefError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(2)

    # TokenCounter の初期化（--token-count / --format json / --max-tokens 時）
    token_counter = None
    needs_tokens = args.token_count or args.format == 'json' or args.max_tokens is not None
    if needs_tokens:
        token_counter = TokenCounter()
        if token_counter.method == 'approx':
            print(
                "Info: Using approximate token count "
                "(install 'kasu[tokens]' for tiktoken)",
                file=sys.stderr,
            )

    # ツリービルダー（tree オプションが指定されている場合のみ）
    tree_builder = None
    if args.tree:
        tree_builder = TreeBuilder(ignore_filter, glob_filter)

    # リストビルダー（list オプションが指定されている場合のみ）
    list_builder = None
    if args.list:
        list_builder = ListBuilder(args.target_dir, root_dir=args.root_dir)

    # ジェネレータ選択
    if args.format == 'json':
        generator = JsonGenerator()
    elif args.format == 'markdown':
        generator = MarkdownGenerator()
    else:
        generator = TextGenerator()

    custom_replacements = None
    if args.replace_file:
        if not os.path.exists(args.replace_file):
            print(f"Warning: Replacement patterns file not found: {args.replace_file}", file=sys.stderr)
        else:
            custom_replacements = Sanitizer.load_replacement_patterns(args.replace_file)

    # Render context for generators (mostly used by JsonGenerator)
    render_context = {
        'kasu_version': KASU_VERSION,
        'generated_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
        'token_counter': token_counter,
        'show_tokens': args.token_count,
        'cli_options': {
            'since': args.since,
            # CLI args.dest は ``diff_ref`` だが、JSON schema の meta.options は
            # CLI フラグ名 ``--diff`` に合わせて ``diff`` で出す
            'diff': args.diff_ref,
            'format': args.format,
            'sanitize': bool(args.sanitize),
            'max_tokens': args.max_tokens,
            'max_bytes': args.max_bytes,
            'absolute_paths': bool(args.absolute_paths),
            'dry_run': bool(args.dry_run),
        },
    }

    merger = Merger(scanner, generator, tree_builder, list_builder)
    merger.merge(
        target_dir=args.target_dir,
        output_file=args.output_file,
        to_stdout=args.stdout,
        show_tree=args.tree,
        show_list=args.list,
        show_stats=args.stats,
        skip_confirm=args.yes,
        enable_sanitize=args.sanitize,
        custom_replacements=custom_replacements,
        head_lines=args.head,
        tail_lines=args.tail,
        root_dir=args.root_dir,
        grep_pattern=args.grep_pattern,
        grep_context=args.grep_context,
        grep_regex=args.grep_regex,
        grep_ignore_case=args.grep_ignore_case,
        include_outline=args.outline,
        outline_patterns=outline_patterns,
        include_merge=not args.no_merge,
        dry_run=args.dry_run,
        absolute_paths=args.absolute_paths,
        max_tokens=args.max_tokens,
        max_bytes=args.max_bytes,
        token_counter=token_counter,
        since_paths=since_paths,
        diff_text=diff_text,
        render_context=render_context,
    )


if __name__ == "__main__":
    main()
