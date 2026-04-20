"""TokenCounter の境界値・エッジケース補強テスト

既存の tests/util/test_tokenizer.py に触れずに追加する。
"""
import builtins
import math

import pytest

from utils.tokenizer import TokenCounter


def _force_tiktoken_import_error(monkeypatch):
    """tiktoken の import を失敗させる"""
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "tiktoken":
            raise ImportError("no tiktoken")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)


class TestTokenCounterNoneInput:
    """None 入力の挙動"""

    def test_none_returns_zero_in_approx_mode(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        assert counter.count(None) == 0

    def test_none_returns_zero_in_tiktoken_mode(self):
        pytest.importorskip("tiktoken")
        counter = TokenCounter()
        assert counter.count(None) == 0


class TestTokenCounterNonAscii:
    """非 ASCII 文字（日本語・絵文字）の挙動"""

    def test_japanese_text_approx_uses_char_length(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        text = "日本語テスト"  # 6 文字
        result = counter.count(text)
        expected = math.ceil(len(text) / 4)
        assert result == expected

    def test_emoji_approx_uses_char_length(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        text = "hello 👋🌍"
        result = counter.count(text)
        expected = math.ceil(len(text) / 4)
        assert result == expected

    def test_mixed_ascii_japanese_approx(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        text = "ABC あいう 123"
        result = counter.count(text)
        expected = math.ceil(len(text) / 4)
        assert result == expected

    def test_japanese_text_tiktoken_returns_positive(self):
        pytest.importorskip("tiktoken")
        counter = TokenCounter()
        text = "日本語テスト"
        result = counter.count(text)
        assert result > 0

    def test_emoji_tiktoken_returns_positive(self):
        pytest.importorskip("tiktoken")
        counter = TokenCounter()
        text = "hello 👋"
        result = counter.count(text)
        assert result > 0


class TestTokenCounterLongText:
    """超長文字列の挙動"""

    def test_very_long_ascii_string_approx(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        text = "a" * 100_000
        result = counter.count(text)
        expected = math.ceil(100_000 / 4)
        assert result == expected

    def test_very_long_string_returns_integer(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        text = "x" * 1_000_000
        result = counter.count(text)
        assert isinstance(result, int)
        assert result > 0


class TestTokenCounterEdgeCases:
    """境界値と特殊文字列"""

    def test_whitespace_only_string_approx(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        # whitespace only は truthy なので count される
        text = "   "
        result = counter.count(text)
        assert result == math.ceil(len(text) / 4)

    def test_newlines_only_approx(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        text = "\n\n\n\n"
        result = counter.count(text)
        assert result == math.ceil(len(text) / 4)

    def test_control_characters_approx(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        text = "\x00\x01\x02\x03"  # null bytes etc.
        result = counter.count(text)
        assert isinstance(result, int)
        assert result >= 0

    def test_single_character_approx(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        result = counter.count("a")
        assert result == 1  # ceil(1/4) = 1

    def test_four_characters_approx(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        result = counter.count("abcd")
        assert result == 1  # ceil(4/4) = 1

    def test_five_characters_approx(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        result = counter.count("abcde")
        assert result == 2  # ceil(5/4) = 2


class TestTokenCounterMethod:
    """method プロパティが正しく返る"""

    def test_method_is_approx_when_tiktoken_unavailable(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        assert counter.method == "approx"

    def test_method_is_tiktoken_when_available(self):
        pytest.importorskip("tiktoken")
        counter = TokenCounter()
        assert counter.method == "tiktoken"
