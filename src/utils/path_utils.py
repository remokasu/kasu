"""パス表示用のユーティリティ"""
import os
from typing import Optional


def _to_unix_path(path: str) -> str:
    return path.replace(os.sep, '/')


def format_relative_path(file_path: str, base_dir: str) -> str:
    """
    base_dir からの相対パスを取得（Unixスタイル）
    """
    try:
        rel_path = os.path.relpath(file_path, base_dir)
    except ValueError:
        return file_path
    return _to_unix_path(rel_path)


def format_display_path(
    file_path: str,
    target_dir: str,
    root_dir: Optional[str] = None,
    leading_slash: bool = False,
) -> str:
    """
    表示用パスを生成

    - root_dir が指定されている場合: root_dir 基準で "root_name/relpath"
    - root_dir がない場合: target_dir 基準で相対パス（必要なら先頭スラッシュ）
    """
    if root_dir:
        rel_path = format_relative_path(file_path, root_dir)
        if rel_path.startswith('..'):
            return file_path
        root_name = os.path.basename(os.path.abspath(root_dir)) or root_dir
        if rel_path in ('.', ''):
            return f"{root_name}/"
        return f"{root_name}/{rel_path}"

    rel_path = format_relative_path(file_path, target_dir)
    if leading_slash:
        return '/' + rel_path
    return rel_path
