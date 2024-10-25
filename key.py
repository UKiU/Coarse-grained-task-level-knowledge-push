# -*- coding: utf-8 -*-
import time
import json
import openai
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)

# client = OpenAI(
#     api_key="sk-QW6tziEl8coNlGUifPQTiplw471zGUiudF6cgPgAzZMYifZ7",
#     base_url="https://api.moonshot.cn/v1",
# r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_dev.jsonl',
# )r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_dev_new.jsonl',

# 定义要读取和写入的 JSONL 文件
input_files = [
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_train.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_trial.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_dev.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_training.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_test.jsonl',
              r"D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\SQuAD\dev.jsonl",
              r"D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\SQuAD\train.jsonl"
              ]
output_files = [
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_train_new.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\CMRC\cmrc2018_trial_new.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_dev_new.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_training_new.jsonl',
               r'D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\DRCD\DRCD_test_new.jsonl',
               r"D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\SQuAD\dev_new.jsonl",
               r"D:\Program\Coarse-grained-task-level-knowledge-push\现有数据\SQuAD\train_new.jsonl"
               ]
for input_file, output_file in zip(input_files, output_files):

    # 读取 JSONL 文件并获取 query
    data_lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            query = data.get('query', '')
            if query:
                data_lines.append(data)


    # 函数：使用 OpenAI API 提取关键词
    def get_keywords_from_query(query):
        completion = client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": "你是一个能够提取关键词的助手。"},
                {"role": "user", "content": f"请提取以下问句的关键词: {query}"}, ],
            temperature=0.8,
            model='qwen2.5:7b',
        )

        # completion = client.chat.completions.create(
        #     model="moonshot-v1-8k",
        #     messages= [
        #     {"role": "system",
        #      "content": "你是一个能够提取关键词的助手。"},
        #     {"role": "user", "content": f"请提取以下问句的关键词: {query}"},],
        #     temperature=0.8,
        # )

        # 获取 OpenAI 的响应
        answer=completion.choices[0].message.content
        return answer


    # 处理每个 query，替换对应的 key 并重新写入文件
    with open(output_file, 'w', encoding='utf-8',indent=4) as f:
        for idx, data in enumerate(data_lines):
            query = data.get('query', '')
            if query:
                print(f"Processing Query {idx + 1}: {query}")
                # 获取关键词作为新的 key
                try:
                    # time.sleep(10)
                    new_key = get_keywords_from_query(query)
                    data['key'] = new_key  # 替换 key 字段
                except openai.RateLimitError:
                    print("Hit rate limit. Waiting for 3 seconds before retrying...")
                    # time.sleep(5)  # 增加等待时间
                    continue

            # 将修改后的行重新写入 JSONL 文件
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    print("处理完成，已将结果写入:", output_file)
    time.sleep(10)