# -*- coding: utf-8 -*-

import json

a= [    r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_dev.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_train.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_trial.json'
               
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\NewsQA\dev.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\NewsQA\train.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\QuAC\val.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\QuAC\train.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\Race\dev.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\Race\train.json',

               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\TriviaQA\dev.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\TriviaQA\train.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_trial.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\NewsQA\test.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\QuAC\test.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\Race\test.json',]

# 假设你的数据保存在 data.json 文件中
input_files = [r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_dev.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_train.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_trial.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_dev.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_training.json',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_test.json',
              r"D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\SQuAD\dev-v2.0.json",
              r"D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\SQuAD\train-v2.0.json"
               ]
output_files = [r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_dev.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_train.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_trial.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_dev.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_training.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_test.jsonl',
              r"D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\SQuAD\dev.jsonl",
              r"D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\SQuAD\train.jsonl"]

for input_file, output_file in zip(input_files, output_files):
    # 读取原始 JSON 数据
    with open(input_file, 'r',encoding="utf-8") as f:
        data = json.load(f)

    # 解析数据并转换为目标格式
    output_data = []
    for article in data.get("data", []):
        for paragraph in article.get("paragraphs", []):
            context = paragraph.get("context", "")
            for qa in paragraph.get("qas", []):
                query = qa.get("question", "")
                key = qa.get("id", "")
                # 获取答案文本，如果是 is_impossible = True，答案列表为空，则设为空字符串
                answers = [ans.get("text", "") for ans in qa.get("answers", [])] or [""]

                # 处理多个答案的情况，只保留第一个答案
                answer = answers[0]

                # 形成新的数据结构
                output_data.append({
                    "query": query,
                    "key": key,
                    "content": context,
                    "answer": answer
                })

    # 将结果保存为 JSONL 格式
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in output_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print("转换完成，输出文件为:", output_file)
