from sqlalchemy import create_engine
from llama_index import GPTSQLStructStoreIndex, SQLDatabase, ServiceContext, LLMPredictor
from langchain.chat_models import ChatOpenAI

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

    # データベースに接続
    database_url = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        **pgconfig)
    engine = create_engine(database_url)

    # LlamaIndexはデフォルトでtext-davinci-003を使うので、gpt-3.5-turboを使うよう設定
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
    service_context = ServiceContext.from_defaults(
        llm_predictor=LLMPredictor(llm=llm))

    # LlamaIndexのtext-to-SQLの準備
    sql_database = SQLDatabase(engine)
    index = GPTSQLStructStoreIndex(
        [],
        service_context=service_context,
        sql_database=sql_database,
    )

    # 問題の一覧を抽出
    questions = extract_questions()[:3]

    # text-to-SQLを実行
    for question in questions:
        print('=== question ===')
        print(question)

        response = index.query(question)
        print('=== answer ===')
        print(response.extra_info['sql_query'])


if __name__ == "__main__":
    main()
