# LlamaIndex で Text-to-SQL 100 本ノック！

LlamaIndex の Text-to-SQL 機能のサンプルコードです。

「データサイエンティスト協会スキル定義委員」の「[データサイエンス 100 本ノック（構造化データ加工編）](https://github.com/The-Japan-DataScientist-Society/100knocks-preprocess)」を使用しています。

## 依存関係

- Python
- Poetry
- Docker
- Docker Compose

バージョンは [.tool-verisons](.tool-versions) に書かれています。

> **Note**
> .tool-verisons は [asdf](https://asdf-vm.com/) の設定ファイルです。

## 実行手順

以下のコマンドで、「[データサイエンス 100 本ノック（構造化データ加工編）](https://github.com/The-Japan-DataScientist-Society/100knocks-preprocess)」のソースコードを準備します。

```console
git submodule update --init
```

以下のコマンドで、データベースを起動します。

```console
cd 100knocks-preprocess
docker-compose up -d db
```

Python のパッケージは Poetry で管理しています。
以下のコマンドでインストールしてください。

```console
poetry install
```

以下のコマンドで、Python のコードを実行します。

```console
export OPENAI_API_KEY=...
poetry run python llamaindex_text_to_sql_100_knocks/main.py
poetry run python llamaindex_text_to_sql_100_knocks/main_without_schema.py
```
