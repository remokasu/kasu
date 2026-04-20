"""Merger._apply_limits の境界値テスト"""
import math

import pytest

from core.merger import Merger


class _FakeCounter:
    method = "approx"

    def count(self, text: str) -> int:
        return math.ceil(len(text) / 4)


def _files(*sizes_tokens):
    """``(size, tokens)`` のタプルから target_files 相当の dict リストを組む"""
    result = []
    for i, pair in enumerate(sizes_tokens):
        size, tokens = pair
        d = {"path": f"/tmp/f{i}.txt", "size": size, "lines": 1}
        if tokens is not None:
            d["tokens"] = tokens
        result.append(d)
    return result


class TestApplyLimitsBytes:
    def test_no_limits_returns_all(self):
        files = _files((10, None), (20, None), (30, None))
        out, truncated, reason = Merger._apply_limits(files, None, None, None)
        assert len(out) == 3
        assert truncated is False
        assert reason is None

    def test_max_bytes_not_reached(self):
        files = _files((10, None), (20, None))
        out, truncated, reason = Merger._apply_limits(files, 100, None, None)
        assert len(out) == 2
        assert truncated is False
        assert reason is None

    def test_max_bytes_exact_fit(self):
        """累計がちょうど max と等しい場合は全件採択"""
        files = _files((10, None), (20, None))  # total 30
        out, truncated, reason = Merger._apply_limits(files, 30, None, None)
        assert len(out) == 2
        assert truncated is False

    def test_max_bytes_exceeded_excludes_file(self):
        files = _files((10, None), (25, None), (5, None))  # 10, 35, 40
        out, truncated, reason = Merger._apply_limits(files, 30, None, None)
        assert len(out) == 1  # 1 個目 (10) だけ、2 個目 (35) で超過
        assert truncated is True
        assert reason == "max_bytes"

    def test_first_file_over_limit_returns_empty(self):
        files = _files((100, None), (10, None))
        out, truncated, reason = Merger._apply_limits(files, 50, None, None)
        assert out == []
        assert truncated is True
        assert reason == "max_bytes"


class TestApplyLimitsTokens:
    def test_max_tokens_uses_counter(self):
        counter = _FakeCounter()
        files = _files((10, 5), (20, 5), (30, 5))  # tokens 5, 10, 15
        out, truncated, reason = Merger._apply_limits(files, None, 10, counter)
        assert len(out) == 2
        assert truncated is True
        assert reason == "max_tokens"

    def test_max_tokens_with_pre_computed_tokens(self):
        counter = _FakeCounter()
        files = _files((10, 3), (20, 3))
        out, truncated, reason = Merger._apply_limits(files, None, 100, counter)
        assert len(out) == 2
        assert truncated is False

    def test_max_tokens_without_counter_does_not_enforce(self):
        """token_counter が None の場合、max_tokens だけでは truncate しない"""
        files = _files((10, None), (20, None))
        out, truncated, reason = Merger._apply_limits(files, None, 1, None)
        assert len(out) == 2
        assert truncated is False


class TestApplyLimitsCombined:
    def test_bytes_limit_hits_first(self):
        counter = _FakeCounter()
        files = _files((100, 1), (100, 1), (100, 1))
        out, truncated, reason = Merger._apply_limits(files, 150, 1000, counter)
        assert len(out) == 1
        assert reason == "max_bytes"

    def test_tokens_limit_hits_first(self):
        counter = _FakeCounter()
        files = _files((10, 50), (10, 50), (10, 50))
        out, truncated, reason = Merger._apply_limits(files, 10000, 60, counter)
        assert len(out) == 1
        assert reason == "max_tokens"
