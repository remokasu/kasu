import os
from typing import Dict, List, Optional

from utils.format_utils import format_size
from utils.tokenizer import TokenCounter


class Statistics:
    """ファイル統計情報を管理"""

    @staticmethod
    def calculate(
        target_files: List[Dict[str, any]],
        token_counter: Optional[TokenCounter] = None,
    ) -> Dict[str, any]:
        """ファイルリストから統計情報を計算

        Args:
            target_files: ファイル情報のリスト。
            token_counter: トークン数計算用のカウンタ。指定時のみ
                ファイル内容を読んでトークン数を集計する。

        Returns:
            統計情報の辞書。``total_tokens`` / ``by_extension[*].tokens``
            は常にキーが存在し、``token_counter`` 未指定時は 0 となる。
        """
        stats = {
            'total_files': len(target_files),
            'total_size': sum(f['size'] for f in target_files),
            'total_lines': sum(f['lines'] for f in target_files),
            'total_tokens': 0,
            'by_extension': {},
        }

        for file_info in target_files:
            ext = os.path.splitext(file_info['path'])[1] or '(no extension)'
            if ext not in stats['by_extension']:
                stats['by_extension'][ext] = {
                    'count': 0,
                    'size': 0,
                    'lines': 0,
                    'tokens': 0,
                }

            stats['by_extension'][ext]['count'] += 1
            stats['by_extension'][ext]['size'] += file_info['size']
            stats['by_extension'][ext]['lines'] += file_info['lines']

            if token_counter is not None:
                tokens = file_info.get('tokens')
                if tokens is None:
                    tokens = Statistics._count_file_tokens(file_info['path'], token_counter)
                    file_info['tokens'] = tokens
                stats['total_tokens'] += tokens
                stats['by_extension'][ext]['tokens'] += tokens

        return stats

    @staticmethod
    def _count_file_tokens(file_path: str, token_counter: TokenCounter) -> int:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return token_counter.count(f.read())
        except (OSError, UnicodeDecodeError):
            return 0

    @staticmethod
    def print_statistics(stats: Dict[str, any], show_tokens: bool = False) -> None:
        """統計情報を表示

        Args:
            stats: ``calculate()`` が返した辞書。
            show_tokens: True の時 tokens 列を表示する。
        """
        print("\n" + "=" * 50)
        print("Statistics")
        print("=" * 50)
        print(f"Total files:  {stats['total_files']:,}")
        print(f"Total lines:  {stats['total_lines']:,}")
        print(f"Total size:   {format_size(stats['total_size'])}")
        if show_tokens:
            print(f"Total tokens: {stats.get('total_tokens', 0):,}")

        if stats['by_extension']:
            print("\nBy extension:")
            sorted_exts = sorted(
                stats['by_extension'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )

            for ext, ext_stats in sorted_exts:
                line = (
                    f"  {ext:15} {ext_stats['count']:4} files  "
                    f"{ext_stats['lines']:6,} lines  "
                    f"{format_size(ext_stats['size']):>10}"
                )
                if show_tokens:
                    line += f"  {ext_stats.get('tokens', 0):>8,} tokens"
                print(line)
        print("=" * 50 + "\n")
