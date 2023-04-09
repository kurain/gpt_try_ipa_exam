import sys
import re
import glob
import json

def check(answers):
    res = []
    with open("ipa_answers.json") as io:
        correct = json.load(io)
    q_count = 0
    pass_count = 0
    correct_count = 0
    for i, ans in enumerate(answers):
        q_count += 1
        tmp = {}
        m = re.search(r'回答:\s*(ア|イ|ウ|エ)', ans["answer"])
        if m:
            a = m[1]
        else:
            a = ""
            print(f"answer {i} is not found")
        
        tmp["correct"] = correct[i]
        tmp["answer"] = a
        if ans["answer"] == "":
            tmp["check"] = "PASS"
            pass_count += 1
        elif a != correct[i]:
            tmp["check"] = "BAD"
        else:
            tmp["check"] = "OK"
            correct_count += 1
        res.append(tmp)
    result = "合格"
    if correct_count / q_count < 0.6:
        result = "不合格"
    return {
        "answers": res,
        "q_count": q_count,
        "pass_count": pass_count,
        "correct_count": correct_count,
        "result" : result
    }

model = sys.argv[1]
answers = []
for path in sorted(glob.glob(f"answers_{model}/*.json")):
    with open(path) as io:
        ans = json.load(io)
    answers.append(ans)

result = check(answers)

model_code = "gpt-4-0314"
if model == "gpt35":
    model_code = "gpt-3.5-turbo-0301"
text = f"""
# GPT による高度情報処理技術者試験の問題への回答

## 概要
令和4年(2023年)秋の午前1共通問題30問を GPT({model_code}) によって解答したものです。
解説も自動生成されたものですので、正しくない可能性があります。

## 結果
- 合否: {result['result']}
- 問題数: {result['q_count']}
- 正解数: {result['correct_count']}
- 正答率: {result['correct_count'] / result['q_count']}
- 図表問題など回答不可能問題数: {result['pass_count']}
- (参考) 回答可能問題の正答率: {result['correct_count'] / (result['q_count']- result['pass_count'])}

## 個別問題の解答
|No|正解|回答|判定|
| --- | --- | --- | --- |
"""
for i, a in enumerate(result['answers']):
    text += f"|{i}|{a['correct']}|{a['answer']}|{a['check']}|\n"
print(text)

for i, part in enumerate(answers):
    q = part["question"]
    a = part["answer"]
    if q == "":
        q = "図表読み取り問題のため skip"
        a = "図表読み取り問題のため skip"
    else:
        q = re.subn(r'\n\s*([アイウエ])\s', r'\n- \1', q)[0]
        q = re.sub(r'^問\d+', '', q)
        q = q

    text += f"""
## 問{i+1}
### 問題
{q}

### 回答
{a}

### 正解
{result['answers'][i]['correct']}
    """

with open(f"report_{model}.md", "w") as io:
    io.write(text)
