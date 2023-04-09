import sys
import openai
import json
import os

def answer(question_text, model):
    order = """
あなたは、高度情報処理技術者試験の問題を解くことになりました。解説付きで問に回答してください。
回答はまず、ア、イ、ウ、エのいずれかの選択肢から選び、次に、その選択肢に対する解説を書いてください。
以下は問題と回答例です。

問題
#######
問0 秋期の情報処理技術者試験が実施される月はどれか。 
ア 8 
イ 9 
ウ 10 
エ 11 
#######

回答: ウ
解説: 秋期の情報処理技術者試験は10月実施と告示されているため。
"""

    question_template = """
問題
#######
{question}
#######

"""
    model_code = "gpt-4-0314"
    if model == "gpt35":
        model_code = "gpt-3.5-turbo-0301"
    question = question_template.format(question=question_text)
    completion = openai.ChatCompletion.create(
        model=model_code,
        messages=[
            {"role": "system", "content": order},
            {"role": "user", "content": question},
        ],
        temperature=0
    )    
    return {
        "question": question_text,
        "answer": completion.choices[0].message.content,
        "usage": completion.usage
    }

def main(path,model="gpt4"):
    name = os.path.basename(path).split(".")[0]
    ans_file = f"answers_{model}/{name}.json"
    if os.path.exists(ans_file):
        print(f"{ans_file} already exists")
        return

    with open(path) as io:
        q = io.read()
        if len(q) == 0:
            print(f"{path} is empty")
            a = {"question": "", "answer": ""}
        else:
            a = answer(q, model)
        print(a)
    
    with open(ans_file, 'w') as io:
        json.dump(a, io, ensure_ascii=False, indent=2)
    

if __name__ == "__main__":
    path = sys.argv[1]
    model = sys.argv[2]
    main(path, model)
