# LlamaIndex で Text-to-SQL 100 本ノック！

LlamaIndex の Text-to-SQL で SQL 100 本ノックに挑戦するコードと実行結果です。

「データサイエンティスト協会スキル定義委員」の「[データサイエンス 100 本ノック（構造化データ加工編）](https://github.com/The-Japan-DataScientist-Society/100knocks-preprocess)」を使用しています。

## このリポジトリに含まれるファイル

LlamaIndex の Text-to-SQL は、プロンプトに context としてデータベースのスキーマ情報を自動で埋め込みます。

- context にスキーマ情報を埋め込む場合 (つまり LlamaIndex の Text-to-SQL を使う場合)
- context にスキーマ情報を埋め込まない場合 (つまり LLM に単に問題文だけを与えて SQL を生成させる場合)

で生成される SQL がどのように異なるのかを比較するため、ソースコードと実行結果のファイルは 2 つずつあります。

- context にスキーマ情報を埋め込む場合
  - ソースコード: [main.py](./llamaindex_text_to_sql_100_knocks/main.py)
  - 実行結果: [result.yaml](./results/result.yaml)
- context にスキーマ情報を埋め込まない場合
  - ソースコード: [main_without_schema.py](./llamaindex_text_to_sql_100_knocks/main_without_schema.py)
  - 実行結果: [result_without_schema.yaml](./results/result_without_schema.yaml)

## 手元で実行したい場合

手元で実行したい場合の依存関係と実行手順は以下の通りです。

### 依存関係

- Python
- Poetry
- Docker
- Docker Compose

Python と Poetry のバージョンは [.tool-verisons](.tool-versions) に書かれています。

> **Note**
> .tool-verisons は [asdf](https://asdf-vm.com/) の設定ファイルです。

### 実行手順

以下のコマンドで、「[データサイエンス 100 本ノック（構造化データ加工編）](https://github.com/The-Japan-DataScientist-Society/100knocks-preprocess)」のソースコードを準備します。

```console
git submodule update --init
```

以下のコマンドで、データベースを起動します。

```console
cd 100knocks-preprocess
docker-compose up -d db
cd ..
```

Python のパッケージは Poetry で管理しています。
以下のコマンドでインストールしてください。

```console
poetry install
```

以下のコマンドで、Python のコードを実行します。

```console
export OPENAI_API_KEY=your-openai-api-key
poetry run python llamaindex_text_to_sql_100_knocks/main.py
poetry run python llamaindex_text_to_sql_100_knocks/main_without_schema.py
```
