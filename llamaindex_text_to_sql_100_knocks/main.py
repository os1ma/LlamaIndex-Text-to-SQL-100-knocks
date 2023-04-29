from sqlalchemy import create_engine
from llama_index import GPTSQLStructStoreIndex, SQLDatabase

import logging
import sys
import langchain

from extract_100knocks_qa import extract_questions

verbose = False

pgconfig = {
    'host': 'localhost',
    'port': 5432,
    'database': 'dsdojo_db',
    'user': 'padawan',
    'password': 'padawan12345',
}


def main():
    if verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
        langchain.verbose = True

    database_url = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        **pgconfig)
    engine = create_engine(database_url)

    sql_database = SQLDatabase(engine)
    index = GPTSQLStructStoreIndex(
        [],
        sql_database=sql_database,
    )

    questions = extract_questions()[:3]

    for question in questions:
        print('=== question ===')
        print(question)

        response = index.query(question)
        print('=== answer ===')
        print(response.extra_info['sql_query'])


if __name__ == "__main__":
    main()
