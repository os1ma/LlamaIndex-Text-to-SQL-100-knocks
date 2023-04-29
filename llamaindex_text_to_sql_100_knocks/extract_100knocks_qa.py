import json


def extract_questions():
    with open('100knocks-preprocess/docker/work/answer/ans_preprocess_knock_SQL.ipynb') as f:
        data = json.load(f)
        cells = data['cells']

        markdown_cell_sources = []
        for cell in cells:
            if cell['cell_type'] == 'markdown':
                source = ''.join(cell['source'])
                markdown_cell_sources.append(source)

        # 最初の4つと最後の1つは問題ではないので除外
        questions = markdown_cell_sources[4:-1]

        return questions


def main():
    questions = extract_questions()
    print(questions)
    print(len(questions))


if __name__ == "__main__":
    main()
