"""アウトライン抽出ユーティリティ"""
from __future__ import annotations

import os
import re
from typing import Dict, List, Tuple, Optional

import yaml
from utils.language_map import LanguageMapper


class OutlineExtractor:
    """各言語のアウトラインを正規表現で抽出"""

    DEFAULT_RESOURCE = "outline_default.yml"

    @classmethod
    def _load_yaml(cls, path: str) -> Dict[str, List[str]]:
        if not path or not os.path.exists(path):
            return {}

        with open(path, 'r', encoding='utf-8') as f:
            loaded = yaml.safe_load(f) or {}

        return cls._normalize_loaded_patterns(loaded)

    @classmethod
    def _normalize_loaded_patterns(cls, loaded: object) -> Dict[str, List[str]]:
        if isinstance(loaded, dict) and 'patterns' in loaded and isinstance(loaded['patterns'], dict):
            loaded = loaded['patterns']

        patterns: Dict[str, List[str]] = {}
        if isinstance(loaded, dict):
            for lang, value in loaded.items():
                if isinstance(value, str):
                    patterns[lang] = [value]
                elif isinstance(value, list):
                    patterns[lang] = [v for v in value if isinstance(v, str)]

        return patterns

    @classmethod
    def load_default_patterns(cls) -> Dict[str, List[str]]:
        try:
            base_dir = os.path.dirname(__file__)
            default_path = os.path.join(base_dir, cls.DEFAULT_RESOURCE)
            return cls._load_yaml(default_path)
        except Exception:
            return {}

    @classmethod
    def load_patterns(cls, config_path: str) -> Dict[str, List[str]]:
        return cls._load_yaml(config_path)

    @classmethod
    def _collect_patterns(
        cls,
        language: str,
        default_patterns: Dict[str, List[str]],
        custom_patterns: Optional[Dict[str, List[str]]] = None
    ) -> List[str]:
        patterns = list(default_patterns.get(language, []))
        if custom_patterns:
            patterns.extend(custom_patterns.get('all', []))
            patterns.extend(custom_patterns.get(language, []))
        return patterns

    @classmethod
    def extract(
        cls,
        file_path: str,
        lines: List[str],
        default_patterns: Optional[Dict[str, List[str]]] = None,
        custom_patterns: Optional[Dict[str, List[str]]] = None
    ) -> List[Tuple[int, str]]:
        language = LanguageMapper.get_language(file_path)
        base_patterns = default_patterns or {}
        patterns = cls._collect_patterns(language, base_patterns, custom_patterns)
        if not patterns:
            return []

        regexes = [re.compile(p) for p in patterns]
        results: List[Tuple[int, str]] = []
        for idx, line in enumerate(lines, start=1):
            for regex in regexes:
                if regex.search(line):
                    results.append((idx, line.rstrip()))
                    break

        return results
