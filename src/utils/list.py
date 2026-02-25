"""ファイル一覧表示機能"""
from typing import List, Dict, Optional

from utils.path_utils import format_display_path

class ListBuilder:
    """ファイル一覧を生成"""

    def __init__(self, base_dir: str, root_dir: Optional[str] = None):
        """
        Args:
            base_dir: ベースディレクトリ
            root_dir: 表示用ルートディレクトリ
        """
        self.base_dir = base_dir
        self.root_dir = root_dir

    def build(self, target_files: List[Dict[str, any]]) -> str:
        """
        ファイル一覧を文字列として生成

        Args:
            target_files: ファイル情報のリスト

        Returns:
            ファイル一覧の文字列
        """
        lines = []
        
        for file_info in target_files:
            file_path = file_info['path']
            display_path = format_display_path(
                file_path,
                self.base_dir,
                root_dir=self.root_dir,
                leading_slash=False
            )

            lines.append(display_path)

        return "\n".join(lines)

    def build_with_stats(self, target_files: List[Dict[str, any]]) -> str:
        """
        ファイル一覧を統計情報付きで生成

        Args:
            target_files: ファイル情報のリスト

        Returns:
            統計情報付きファイル一覧の文字列
        """
        from .format_utils import format_size
        
        lines = []
        
        for file_info in target_files:
            file_path = file_info['path']
            size = file_info['size']
            line_count = file_info['lines']

            display_path = format_display_path(
                file_path,
                self.base_dir,
                root_dir=self.root_dir,
                leading_slash=False
            )

            # フォーマット: "path (size, lines lines)"
            lines.append(f"{display_path} ({format_size(size)}, {line_count:,} lines)")

        return "\n".join(lines)
