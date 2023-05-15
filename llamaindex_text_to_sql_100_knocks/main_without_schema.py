import langchain
from extract_100knocks_qa import extract_questions
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate)
from ruamel.yaml import YAML

verbose = True

# LlamaIndexが内部で使用しているプロンプトから、以下の2行を削除したプロンプト
#
# Only use the tables listed below.
# {schema}
#
# 参考: https://github.com/jerryjliu/llama_index/blob/c60b9420b67cff3b07d483dda96544992d298c6f/gpt_index/prompts/default_prompts.py#L173
template = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Pay attention to which column is in which table. Also, qualify column names with the table name when needed.
Use the following format:
Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Question: {query_str}
SQLQuery: """


def main():
    if verbose:
        langchain.verbose = True

    # LlamaIndexはデフォルトでtext-davinci-003を使うので、gpt-3.5-turboを使うよう設定
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)

    # https://github.com/jerryjliu/llama_index/blob/c60b9420b67cff3b07d483dda96544992d298c6f/gpt_index/prompts/default_prompts.py#L173
    prompt = PromptTemplate(
        template=template,
        input_variables=['dialect', 'query_str'],
    )
    chat_prompt_template = ChatPromptTemplate.from_messages(
        [HumanMessagePromptTemplate(prompt=prompt)])

    chain = LLMChain(llm=llm, prompt=chat_prompt_template)

    chain(inputs={
        "dialect": "postgresql",
        "query_str": ""
    })

    # 問題の一覧を抽出
    questions = extract_questions()[:1]

    # text-to-SQLを実行
    qa_list = []
    for question in questions:
        chain_result = chain(inputs={
            "dialect": "postgresql",
            "query_str": question
        })
        text = chain_result['text']

        stop_token = "\nSQLResult:"
        stop_token_index = text.find(stop_token)

        answer = text[:stop_token_index]

        qa = {
            'question': question,
            'answer': answer,
        }
        qa_list.append(qa)

    # 実行結果を保存
    yaml = YAML()
    yaml.default_style = '|'
    with open('tmp/result_without_schema.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(qa_list, f)


if __name__ == "__main__":
    main()
