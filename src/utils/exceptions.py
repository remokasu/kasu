"""KASU ドメイン固有の例外階層

Raises:
    KasuError: すべての KASU 独自例外の基底クラス。
"""


class KasuError(Exception):
    """KASU の全独自例外の基底クラス"""


class KasuGitNotFoundError(KasuError):
    """git コマンドが PATH に見つからない時に送出

    `--since` / `--diff` 指定時に `git` 実行ファイルが PATH に存在しない場合。
    """


class KasuNotAGitRepoError(KasuError):
    """target directory が git repository でない時に送出

    `--since` / `--diff` 指定時に `target_dir` が git リポジトリ外の場合。
    """


class KasuInvalidGitRefError(KasuError):
    """指定された git ref が解決できない時に送出

    `--since <ref>` / `--diff <ref>` の `<ref>` が
    `git rev-parse` で解決できない場合。
    """


class KasuTokenizerError(KasuError):
    """トークナイザ層の予期せぬエラー時に送出（将来拡張用）

    Phase 1 では raise しないが、`--tokenizer` フラグ追加時などに
    encoder 選択エラー等で使う想定。
    """
