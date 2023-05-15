import logging
import sys

import langchain
from extract_100knocks_qa import extract_questions
from langchain.chat_models import ChatOpenAI
from llama_index import (GPTSQLStructStoreIndex, LLMPredictor, ServiceContext,
                         SQLDatabase)
from ruamel.yaml import YAML
from sqlalchemy import create_engine

verbose = True

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
    predictor = LLMPredictor(llm)
    service_context = ServiceContext.from_defaults(llm_predictor=predictor)

    # LlamaIndexのtext-to-SQLの準備
    sql_database = SQLDatabase(engine)
    index = GPTSQLStructStoreIndex(
        [],
        service_context=service_context,
        sql_database=sql_database,
    )

    # 問題の一覧を抽出
    questions = extract_questions()[:50]

    # text-to-SQLを実行
    qa_list = []
    for question in questions:
        response = index.query(question)
        answer = response.extra_info['sql_query']

        qa = {
            'question': question,
            'answer': answer,
        }
        qa_list.append(qa)

    # 実行結果を保存
    yaml = YAML()
    yaml.default_style = '|'
    with open('out/result.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(qa_list, f)


if __name__ == "__main__":
    main()
