"""トークン数カウント

tiktoken が install されていれば正確なトークン数、
未 install 時は `len(text) / 4` の近似でフォールバックする。

See: docs/adr/0001-tokenizer-strategy.md
"""
import math
from typing import Optional


class TokenCounter:
    """トークン数を見積もるユーティリティ

    tiktoken を lazy import し、install されていれば ``cl100k_base``
    エンコーダを利用する。未 install 時は近似式で計算する。

    Attributes:
        method: 実際に利用した計算方式（``"tiktoken"`` or ``"approx"``）。
    """

    _DEFAULT_ENCODING = "cl100k_base"
    _APPROX_CHARS_PER_TOKEN = 4

    def __init__(self, encoding_name: str = _DEFAULT_ENCODING) -> None:
        """TokenCounter を初期化

        Args:
            encoding_name: tiktoken エンコーダ名。Phase 1 では
                ``"cl100k_base"`` 固定を推奨。
        """
        self._encoder = None
        self._method: str = "approx"
        try:
            import tiktoken  # noqa: PLC0415
            self._encoder = tiktoken.get_encoding(encoding_name)
            self._method = "tiktoken"
        except ImportError:
            self._encoder = None
            self._method = "approx"

    @property
    def method(self) -> str:
        """実際に利用した計算方式を返す"""
        return self._method

    def count(self, text: Optional[str]) -> int:
        """テキストのトークン数を返す

        Args:
            text: 対象文字列。``None`` または空文字列は 0 を返す。

        Returns:
            トークン数の見積もり値。
        """
        if not text:
            return 0
        if self._encoder is not None:
            return len(self._encoder.encode(text))
        return math.ceil(len(text) / self._APPROX_CHARS_PER_TOKEN)
