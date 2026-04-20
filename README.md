# KASU

AI駆動開発におけるコードベースの抽象化と管理の支援ツール

## 主な機能

- **複数ファイルの統合** - ディレクトリ内のテキストファイルを1ファイルに結合
- **パス付きヘッダー** - 各ファイルの内容をパス付きで区切り
- **出力形式** - プレーンテキスト / Markdown / JSON
- **フィルタリング** - Globパターン、除外パターン、.gitignore対応
- **ディレクトリツリー表示** - プロジェクト構造の可視化
- **ファイル一覧表示** - 対象ファイルのリストアップ
- **部分的な内容抽出** - 各ファイルの先頭/末尾N行のみ抽出
- **機密情報のサニタイズ** - IP、メール、APIキー、クラウド認証、JWT、接続情報などの自動置換
- **設定ファイル対応** - コマンドラインオプションをYAMLで指定可能
- **表示ルート指定** - パス表示の基準ルートを指定可能
- **周辺抽出（grep）** - 検索語にヒットした周辺行のみ抽出
- **アウトライン抽出** - 関数/クラス/見出しなどのアウトラインを抽出
- **JSON出力** - JSON出力（schema_version "1.0" 固定）
- **トークン数カウント** - tiktoken 使用時は正確、未インストール時は近似値を返す
- **Git連携** - `--since <ref>` で変更ファイルのみ、`--diff <ref>` で差分セクションを埋め込み
- **dry-run** - ファイル内容を出さずにメタデータだけ確認
- **絶対パス出力** - エージェント向けに `path` を絶対パスで埋める
- **出力上限** - `--max-tokens` / `--max-bytes` でトータル出力量をファイル単位で切り詰め

## インストール

- pypiからインストール
    ```bash
    pip install kasu
    ```

- ソースからインストール
    ```bash
    git clone git@github.com:remokasu/kasu.git
    cd kasu
    pip install -e .
    ```

## クイックスタート

### 基本的な使い方（カレントディレクトリを結合）
``` bash
ks -i . -o output.txt
```
### Markdown形式で出力
``` bash
ks -i . -o output.md --format md
```
### Pythonファイルだけを対象に
``` bash
ks -i . -o output.md -g "*.py" --format md
```
### AIエージェント向け: JSON形式で出力
``` bash
ks -i . -o output.json -f json --token-count
```
### Git で変更したファイルだけを対象に
``` bash
ks -i . --stdout -f json --since HEAD~3
```
### トークン上限付きで出力（LLM context 向け）
``` bash
ks -i . --stdout -f json --max-tokens 100000
```

## 使い方

### 指定したディレクトリ以下のテキストファイルを結合して1ファイルに出力

- プレーンテキストで出力

    ```bash
    ks -i [DIR] -o [FILE]
    ``` 

- Markdown形式で出力

    ```bash
    ks -i [DIR] -o [FILE.md] --format md
    ```

    または

    ```bash
    ks -i [DIR] -o [FILE.md] -f md
    ```

- 標準出力に出力

    ```bash
    ks -i [DIR] --stdout
    ```

### tree 情報を出力

- 標準出力に出力
    ```bash
    ks -i [DIR] --tree
    ```
    または
    ```bash
    ks -i [DIR] -t
    ```

- `-o` で指定したファイルの先頭に出力
    ```bash
    ks -i [DIR] -o [FILE] --tree
    ```
    または
    ```bash
    ks -i [DIR] -o [FILE] -t
    ```
    - i で指定したディレクトリ以下のファイル内容が続きます。

- `-o` で指定したファイルにtree情報のみを出力
    ```bash
    ks -i [DIR] -o [FILE] --tree --no-merge
    ```
    `--no-merge`を指定することで、-iで指定したディレクトリ以下のファイル内容は出力されません。

- 出力例

    ```
    Auto-detected and using: ./.gitignore
    Scanning files...
    Found 5 files
    Ignored by patterns: 2 files/directories

    Directory tree:
    example-project/
    ├── docs/
    │   └── README.md
    ├── src/
    │   ├── config.json
    │   ├── main.py
    │   └── utils.py
    └── tests/
        └── test_main.py
    ```

### 表示ルートを指定

`--root` を指定すると、`tree` / `list` / ファイルヘッダーのパス表示が指定ルート基準になります。

```bash
ks -i ./src -o output.txt --root .
```

### 検索語の周辺だけ抽出（grep）

`--grep` で検索語にヒットした前後行だけを出力します。必要に応じて `--context` を広げます。

```bash
ks -i . -o output.txt --grep "JWT" --context 3
```

複数指定:
```bash
ks -i . -o output.txt --grep "JWT" --grep "OAuth"
```

正規表現で検索する場合:
```bash
ks -i . -o output.txt --grep "token_[0-9a-f]{32}" --regex
```

大文字小文字を無視する場合:
```bash
ks -i . -o output.txt --grep "jwt" --ignore-case
```

### アウトライン抽出

関数/クラス/見出しなどを抽出して、コードの全体像を素早く把握できます。

```bash
ks -i . -o output.txt --outline
```

追加パターンを指定したい場合（YAML）:
```bash
ks -i . -o output.txt --outline --outline-config outline.yml
```

`outline.yml` 例:
```yaml
patterns:
  python:
    - '^class\s+\w+'
    - '^def\s+\w+'
  all:
    - '^TODO'
```

デフォルトのパターン定義は `outline.default.yml` にあります（必要ならコピーして編集して `--outline-config` で指定）。

### AIエージェント向けのJSON出力

`--format json` / `-f json` を指定すると、スキーマ固定の構造化 JSON を出力します。`schema_version: "1.0"` が必ず含まれ、各ファイルの `path` / `absolute_path` / `size` / `lines` / `tokens` / `encoding` / `language` / `content` / `truncated` を持ちます。

```bash
ks -i . -o output.json -f json
```

標準出力にそのまま流してパイプで LLM ツールに渡すこともできます:

```bash
ks -i . --stdout -f json --token-count | jq '.meta.total_tokens'
```

出力の主な構造:

```json
{
  "meta": {
    "schema_version": "1.0",
    "kasu_version": "0.0.8",
    "total_files": 10,
    "total_tokens": 12345,
    "token_method": "tiktoken",
    "truncated": false,
    "dry_run": false,
    "options": { "...": "CLIに渡されたオプション" }
  },
  "files": [
    {
      "path": "src/main.py",
      "absolute_path": "/abs/path/src/main.py",
      "size": 1024,
      "lines": 42,
      "tokens": 200,
      "encoding": "utf-8",
      "language": "python",
      "content": "...ファイル内容（--dry-run / --no-merge 時は null）...",
      "truncated": false
    }
  ]
}
```

### トークン数をカウント

`--token-count` を指定すると、各ファイルのトークン数と合計を算出します。

```bash
ks -i . -f json --token-count
```

- `tiktoken` がインストールされていれば `cl100k_base` で正確にカウント
- 未インストール時は `ceil(len(text) / 4)` の近似値にフォールバック（`meta.token_method: "approx"`）

tiktoken を使う場合:

```bash
pip install kasu[tokens]
```

### Git連携（--since / --diff）

`--since <ref>` で、指定した Git ref 以降に変更されたファイルのみを対象にします。

```bash
ks -i . -f json --since HEAD~3
ks -i . -f json --since main
```

`--diff <ref>` で、`git diff <ref>...HEAD` の内容を出力に差分セクションとして埋め込みます。

```bash
ks -i . -f markdown -o out.md --diff main -y
```

どちらも `git` コマンドが PATH になく、`-i` で指定したディレクトリが Git リポジトリでない場合は exit code 2 でエラー終了します。

### Dry-run

`--dry-run` を指定すると、ファイル内容を出力せずメタデータ（path / size / lines / tokens など）だけを出します。事前に対象ファイルの規模を把握するのに便利です。

```bash
ks -i . --stdout -f json --dry-run
```

JSON 出力の場合、`files[].content` は `null` になり、`meta.dry_run: true` が立ちます。`--sanitize` は dry-run 時には自動で無効化されます（`stderr` に info ログ）。

### 絶対パスで出力

`--absolute-paths` を指定すると、`path` 表示を絶対パスにします（エージェントが後から直接ファイルを開く用途向け）。`--root` とは排他です。

```bash
ks -i . -o output.txt --absolute-paths
```

### 出力上限でトリミング

`--max-tokens N` / `--max-bytes N` で、累計トークン数またはバイト数がしきい値を超えた時点で **ファイル単位** で出力を打ち切ります（ファイル途中では切りません）。

```bash
ks -i . -f json --max-tokens 100000
ks -i . -f json --max-bytes 500000
```

上限到達時は `stderr` に警告を出し、`meta.truncated: true` / `meta.truncate_reason: "max_tokens"` を立てます。

### ファイル一覧を標準出力に出力

- 標準出力に出力

    ```bash
    ks -i [DIR] --list
    ```
    または
    ```bash
    ks -i [DIR] -l
    ```
- `-o`で指定したファイルの先頭に出力
    ```bash
    ks -i [DIR] -o [FILE] --list
    ```
    または
    ```bash
    ks -i [DIR] -o [FILE] -l
    ```
    `-i` で指定したディレクトリ以下のファイル内容が続きます。

- `-o` で指定したファイルにファイル一覧のみを出力
    ```bash
    ks -i [DIR] -o [FILE] --list --no-merge
    ```
    `--no-merge`を指定することで、`-i`で指定したディレクトリ以下のファイル内容は出力されません。

- 出力例
    ```
    Auto-detected and using: ./.gitignore
    Scanning files...
    Found 5 files
    Ignored by patterns: 2 files/directories

    File list:
    tests/test_main.py
    src/utils.py
    src/config.json
    src/main.py
    docs/README.md
    ```

### 条件を指定して対象ファイルを絞り込み

- `-g`で含めるファイルパターンを指定します。

    例: `-g "*.py"` で拡張子が.pyのファイルのみ対象にします。

    ```bash
    ks -i [DIR] -o [FILE] -g "*.py"
    ```

    複数指定
    ```bash
    ks -i [DIR] -o [FILE] -g "*.py" "*.md"
    ```

### 対象から特定のファイルを除外
- `-i`で指定したディレクトリ以下に.gitignoreがあれば自動的に.gitignoreの内容を除外します。

- `--ignore`で、除去対象を記載したファイルを指定できます。

    このファイルは.gitignoreと同じ書き方ができます。

    `--ignore` を指定した時は`.gitignore` は無視されます。

- `--no-auto-ignore`で.gitignoreの自動検出を無効化できます。

- `-x`で指定したパターンを除外します。

    もし対象に.gitignoreがあり、かつREADME.mdを除外したい場合、以下のようにします。
    ```bash
    ks -i [DIR] -o [FILE] -x "README.md"
    ```

### サニタイズ

- コンフィデンシャルな情報を自動的に検出して置換します。

- ただし、確実に検出できるわけではありません。

- `--sanitize`を指定します。

    ```bash
    ks -i [DIR] -o [FILE] --sanitize
    ```
    または
    ```bash
    ks -i [DIR] -o [FILE] -s
    ```


- 検出するパターン
    1. APIキー: api_key=, apikey=, api-secret= などの後に続く20文字以上の英数字を検出
        ```
        置換形式: [REDACTED_API_KEY_1], [REDACTED_API_KEY_2], ...
        ```

    2. パスワード: password=, passwd=, pwd= などの後に続く6文字以上の値を検出
        ```
        置換形式: [REDACTED_PASSWORD_1], [REDACTED_PASSWORD_2], ...
        ```

    3. AWSキー - AKIA で始まる16文字の英数字を検出
        ```
        置換形式: [REDACTED_AWS_KEY_1], [REDACTED_AWS_KEY_2], ...
        ```

    4. メールアドレス - 標準的なメール形式を検出
        ```
        置換形式: [REDACTED_EMAIL_1], [REDACTED_EMAIL_2], ...
        ```

    5. IPアドレス - パブリックIPのみ検出（ローカルIP 127., 192.168., 10. は除外）
        ```
        置換形式: [REDACTED_IP_1], [REDACTED_IP_2], ...
        ```

    6. 秘密鍵 - PEM形式の秘密鍵全体を検出
        ```
        置換形式: [REDACTED_PRIVATE_KEY]
        ```

### 置換パターンを指定
    
パターンファイルを指定して、カスタム置換を行うことができます。

- パターンファイルフォーマット
    - pattern_file.txt(名前は任意)
        ```
        tanaka.ichiro@group.go.jp hoge@hoge.com
        田中一郎 ほげ山ほげ男
        Company Inc. ほげほげ会社
        ```

    - 左側が置換対象、右側が置換後の文字列です。上記の例では以下の置換が行われます。
        - tanaka.ichiro@group.go.jp → hoge@hoge.com
        - 田中一郎 → ほげ山ほげ男
        - Company Inc. → ほげほげ会社

- 指定方法
    ```bash
    ks -i [DIR] -o [FILE] --replace [PATTERN_FILE]
    ```
    または
    ```bash
    ks -i [DIR] -o [FILE] -r [PATTERN_FILE]
    ```

### 各ファイルの先頭/末尾N行のみ出力

- 先頭N行
    ```bash
    ks -i [DIR] -o [FILE] --head N
    ```
- 末尾N行
    ```bash
    ks -i [DIR] -o [FILE] --tail N
    ```

### 設定ファイルを指定

- `--config [FILE]`, または `-c [FILE]`で設定ファイルを指定できます。

    ``` bash
    ks --config config.yaml
    ```

- config.yaml
    ```yaml
    input: .
    output: output.md
    format: md
    glob:
    - "*.py"
    - "*.md"
    exclude:
    - "tests/"
    - "docs/"
    head: 50
    sanitize: true
    # Phase 1 で追加されたキー
    token_count: true
    max_tokens: 100000
    max_bytes: 500000
    dry_run: false
    absolute_paths: false
    since: HEAD~3
    diff: main
    ```


## コマンドラインオプション一覧

| オプション | 短縮形 | 説明 |
|-----------|--------|------|
| `--input DIR` | `-i` | 入力ディレクトリ（デフォルト: `.`） |
| `--output FILE` | `-o` | 出力ファイルパス |
| `--stdout` | - | 標準出力に出力 |
| `--format FORMAT` | `-f` | 出力形式（`text`/`markdown`/`md`/`json`） |
| `--absolute-paths` | - | `path` を絶対パスで出力（`--root` と排他） |
| `--glob PATTERN` | `-g` | 含めるファイルパターン |
| `--exclude PATTERN` | `-x` | 除外パターン |
| `--ignore FILE` | - | ignoreファイルを指定 |
| `--no-auto-ignore` | - | .gitignore自動検出を無効化 |
| `--head N` | - | 各ファイルの先頭N行のみ |
| `--tail N` | - | 各ファイルの末尾N行のみ |
| `--tree` | `-t` | ディレクトリツリーを表示 |
| `--list` | `-l` | ファイル一覧を表示 |
| `--stats` | - | 統計情報を表示 |
| `--outline` | - | 関数/クラス等のアウトラインを抽出 |
| `--token-count` | - | トークン数を算出（tiktoken 未導入時は近似値） |
| `--since REF` | - | 指定 Git ref 以降に変更されたファイルのみ対象 |
| `--diff REF` | - | `git diff <REF>...HEAD` を出力に埋め込む |
| `--max-tokens N` | - | 累計トークン数で出力をファイル単位に切り詰め |
| `--max-bytes N` | - | 累計バイト数で出力をファイル単位に切り詰め |
| `--dry-run` | - | ファイル内容を出さずメタデータのみ出力 |
| `--sanitize` | `-s` | 機密情報を自動サニタイズ |
| `--replace FILE` | `-r` | カスタム置換パターンファイル |
| `--yes` | `-y` | 確認プロンプトをスキップ |
| `--debug` | `-d` | デバッグ情報を表示 |
| `--config FILE` | `-c` | 設定ファイルを指定 |

