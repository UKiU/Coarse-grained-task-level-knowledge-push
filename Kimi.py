from openai import OpenAI

# client = OpenAI(
#     api_key="sk-QW6tziEl8coNlGUifPQTiplw471zGUiudF6cgPgAzZMYifZ7",
#     base_url="https://api.moonshot.cn/v1",
# )
client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)
n=0
for i in range(100):
    messages = [
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "请生成新的10个用于训练embedding模型的问答对，问题是关于体育的。"},
        {"role": "user", "content": "问答对格式请参考：（问题，关键信息，答案）,要求答案比问题长非常多。"},
    ]
    answer=[]
    for j in range(5):
        n+=1
        print("第{}个伦茨".format(n))
        completion = client.chat.completions.create(
            model='qwen2.5:7b',
            messages=messages,
            temperature=0.8,
        )
        answer.append(completion.choices[0].message.content)
        messages.append({"role": "user", "content": completion.choices[0].message.content})
        messages.append({"role": "user", "content": "请生成新的10个用于训练embedding模型的问答对,问答对格式请参考：（问题，关键信息，答案）,要求答案比问题长非常多。"},)
    with open("纯生成/体育.txt", "a", encoding="utf-8") as f:
        for content in answer:
            f.write(content)
            f.write("\n")
print(completion.choices[0].message.content)