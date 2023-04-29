from sqlalchemy import create_engine
from llama_index import GPTSQLStructStoreIndex, SQLDatabase

import logging
import sys


pgconfig = {
    'host': 'localhost',
    'port': 5432,
    'database': 'dsdojo_db',
    'user': 'padawan',
    'password': 'padawan12345',
}


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    database_url = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        **pgconfig)
    engine = create_engine(database_url)

    sql_database = SQLDatabase(engine, include_tables=["receipt"])

    index = GPTSQLStructStoreIndex(
        [],
        sql_database=sql_database,
        table_name="receipt",
    )

    response = index.query(
        "レシート明細データ（receipt）から全項目の先頭10件を表示し、どのようなデータを保有しているか目視で確認せよ。")
    print(response)

    print(response.extra_info['sql_query'])


if __name__ == "__main__":
    main()
