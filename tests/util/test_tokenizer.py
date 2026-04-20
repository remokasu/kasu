"""TokenCounter のユニットテスト"""
import builtins
import math

import pytest

from utils.tokenizer import TokenCounter


def _force_tiktoken_import_error(monkeypatch):
    """tiktoken の import を失敗させる"""
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == 'tiktoken':
            raise ImportError('no tiktoken')
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', fake_import)


class TestTokenCounterApprox:
    """tiktoken が無い想定で approx fallback を検証"""

    def test_empty_string_is_zero(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        assert counter.method == 'approx'
        assert counter.count('') == 0

    def test_approx_counts_ceil_len_div_4(self, monkeypatch):
        _force_tiktoken_import_error(monkeypatch)
        counter = TokenCounter()
        assert counter.method == 'approx'
        assert counter.count('abcd') == math.ceil(4 / 4)
        assert counter.count('abcde') == math.ceil(5 / 4)
        assert counter.count('hello, world!') == math.ceil(13 / 4)


class TestTokenCounterTiktoken:
    """tiktoken がインストールされている時のみ動く"""

    def test_tiktoken_method_when_available(self):
        pytest.importorskip('tiktoken')
        counter = TokenCounter()
        assert counter.method == 'tiktoken'
        assert counter.count('hello world') > 0
