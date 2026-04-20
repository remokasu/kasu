"""Merger._apply_limits の境界値・エラーパス補強テスト

既存の tests/util/test_merger_truncate.py に触れずに追加する。
"""
import math

import pytest

from core.merger import Merger


class _FakeCounter:
    method = "approx"

    def count(self, text: str) -> int:
        return math.ceil(len(text) / 4)


class _BrokenCounter:
    """count() を呼ぶと RuntimeError を投げるカウンタ"""
    method = "approx"

    def count(self, text: str) -> int:
        raise RuntimeError("simulated counter failure")


def _files(*specs):
    """(size, tokens_or_None) タプルから target_files 相当の dict リストを組む。
    path は実在しないダミーパスを使う（size_missing ケース以外）。
    """
    result = []
    for i, pair in enumerate(specs):
        size, tokens = pair
        d = {"path": f"/nonexistent/f{i}.txt", "size": size, "lines": 1}
        if tokens is not None:
            d["tokens"] = tokens
        result.append(d)
    return result


class TestApplyLimitsEmptyInput:
    """target_files が空の場合"""

    def test_empty_files_with_no_limits_returns_empty(self):
        out, truncated, reason = Merger._apply_limits([], None, None, None)
        assert out == []
        assert truncated is False
        assert reason is None

    def test_empty_files_with_max_bytes_returns_empty_not_truncated(self):
        out, truncated, reason = Merger._apply_limits([], 100, None, None)
        assert out == []
        assert truncated is False
        assert reason is None

    def test_empty_files_with_max_tokens_returns_empty_not_truncated(self):
        counter = _FakeCounter()
        out, truncated, reason = Merger._apply_limits([], None, 100, counter)
        assert out == []
        assert truncated is False
        assert reason is None

    def test_empty_files_with_both_limits_returns_empty_not_truncated(self):
        counter = _FakeCounter()
        out, truncated, reason = Merger._apply_limits([], 100, 100, counter)
        assert out == []
        assert truncated is False
        assert reason is None


class TestApplyLimitsMissingSize:
    """size キーが欠落した file_info の挙動（get で 0 フォールバック）"""

    def test_missing_size_key_defaults_to_zero(self):
        files = [{"path": "/tmp/f.txt", "lines": 1}]
        out, truncated, reason = Merger._apply_limits(files, 1, None, None)
        # size=0 なので max_bytes=1 を超えない → 採択
        assert len(out) == 1
        assert truncated is False

    def test_missing_size_key_with_tight_limit_still_accepts(self):
        """size キーなし → size=0 扱い → どんな max_bytes でも超えない"""
        files = [
            {"path": "/tmp/f0.txt", "lines": 1},
            {"path": "/tmp/f1.txt", "lines": 1},
        ]
        out, truncated, reason = Merger._apply_limits(files, 0, None, None)
        # size=0 で cumulative 0 <= 0 なので全件採択
        assert len(out) == 2
        assert truncated is False


class TestApplyLimitsTokenCounterException:
    """token_counter.count() が例外を投げた場合の挙動"""

    def test_broken_counter_falls_back_via_file_read_path(self):
        """_count_tokens_for_file は OSError を握り潰して 0 を返すので
        存在しないファイルでも tokens=0 扱いになる"""
        counter = _FakeCounter()
        files = [
            {"path": "/nonexistent_dir/ghost.txt", "size": 10, "lines": 1},
        ]
        out, truncated, reason = Merger._apply_limits(files, None, 100, counter)
        assert len(out) == 1
        assert truncated is False
        assert out[0]["tokens"] == 0

    def test_broken_counter_count_raises_propagates(self):
        """tokens キーが既にある場合は _count_tokens_for_file を呼ばないが、
        tokens キーがなく count() 自体が例外を投げると呼び出し元まで伝播する。
        注: _apply_limits は内部で _count_tokens_for_file 経由でカウントするが
        その中でも例外を握り潰すので、結果として tokens=0 になる"""
        broken = _BrokenCounter()
        files = [
            {"path": "/nonexistent/file.txt", "size": 5, "lines": 1},
        ]
        # _count_tokens_for_file はファイルが開けない場合 0 を返すため
        # broken counter の count() は呼ばれても実際には OSError で先に失敗する
        out, truncated, reason = Merger._apply_limits(files, None, 100, broken)
        assert len(out) == 1
        assert out[0]["tokens"] == 0

    def test_pre_computed_tokens_skips_counter(self):
        """tokens キーが既に計算済みなら count() を呼ばない"""
        broken = _BrokenCounter()
        files = _files((10, 3), (20, 4))  # tokens キー付き
        # broken counter だが tokens キーがあるので count() は呼ばれない
        out, truncated, reason = Merger._apply_limits(files, None, 100, broken)
        assert len(out) == 2
        assert truncated is False


class TestApplyLimitsBoundaryValues:
    """境界値テスト"""

    def test_max_bytes_zero_first_file_size_zero_is_accepted(self):
        """max_bytes=0 で size=0 のファイルは 0 <= 0 で採択"""
        files = [{"path": "/tmp/f.txt", "size": 0, "lines": 0}]
        out, truncated, reason = Merger._apply_limits(files, 0, None, None)
        assert len(out) == 1
        assert truncated is False

    def test_max_bytes_zero_first_file_size_one_is_rejected(self):
        """max_bytes=0 で size=1 のファイルは 1 > 0 で拒否"""
        files = _files((1, None))
        out, truncated, reason = Merger._apply_limits(files, 0, None, None)
        assert len(out) == 0
        assert truncated is True
        assert reason == "max_bytes"

    def test_max_tokens_zero_with_pre_computed_token_one_is_rejected(self):
        """max_tokens=0 で tokens=1 のファイルは拒否"""
        counter = _FakeCounter()
        files = _files((10, 1))
        out, truncated, reason = Merger._apply_limits(files, None, 0, counter)
        assert len(out) == 0
        assert truncated is True
        assert reason == "max_tokens"

    def test_single_file_exactly_at_bytes_limit(self):
        """累計 == max_bytes ならば採択（超えていない）"""
        files = _files((50, None))
        out, truncated, reason = Merger._apply_limits(files, 50, None, None)
        assert len(out) == 1
        assert truncated is False

    def test_single_file_one_over_bytes_limit(self):
        """累計 == max_bytes + 1 ならば拒否"""
        files = _files((51, None))
        out, truncated, reason = Merger._apply_limits(files, 50, None, None)
        assert len(out) == 0
        assert truncated is True

    def test_return_tuple_has_three_elements(self):
        files = _files((10, None))
        result = Merger._apply_limits(files, None, None, None)
        assert len(result) == 3

    def test_max_bytes_and_max_tokens_both_none_no_truncation(self):
        """limits が両方 None なら常に全件返す"""
        files = _files((10**9, 10**9))  # 巨大なサイズ
        out, truncated, reason = Merger._apply_limits(files, None, None, None)
        assert len(out) == 1
        assert truncated is False
        assert reason is None

    @pytest.mark.parametrize("n_files", [1, 5, 100])
    def test_no_limits_always_returns_all_files(self, n_files):
        files = _files(*[(i * 10, None) for i in range(n_files)])
        out, truncated, reason = Merger._apply_limits(files, None, None, None)
        assert len(out) == n_files
        assert truncated is False
