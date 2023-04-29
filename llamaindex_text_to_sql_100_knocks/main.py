from sqlalchemy import create_engine
from llama_index import GPTSQLStructStoreIndex, SQLDatabase, GPTSimpleVectorIndex
from llama_index.indices.struct_store import SQLContextContainerBuilder

import logging
import sys
import langchain


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
    langchain.verbose = True

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
        'レシート明細データ（receipt）と店舗データ（store）を内部結合し、レシート明細データの全項目と店舗データの店舗名（store_name）を10件表示せよ。')
    print(response.extra_info['sql_query'])
    print(response)


if __name__ == "__main__":
    main()
