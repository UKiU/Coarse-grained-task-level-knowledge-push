from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np
from sentence_transformers import SentenceTransformer
from utils import *

loader = CustomJSONLoader(
    file_path='./data/cn_test_set.json',
    jq_schema='."Session-3"."对话历史"',)

data = loader.load()


# # 本地加载
# model = SentenceTransformer('./model')
query = "早睡早起到底是不是保持身体健康的标准？"
sentences = ["早睡早起确实是保持身体健康的重要因素之一。它有助于同步我们的生物钟，并提高睡眠质量。",
             "早睡早起可以帮助人们更好地适应自然光周期，从而优化褪黑激素的产生，这种激素是调节睡眠和觉醒的关键。",
             "关于提高工作效率，确保在日常饮食中包含充足的蛋白质、复合碳水化合物和健康脂肪非常关键。"
           ]
# sen_embeddings = model.encode(sentences)
# query_embedding = model.encode(query)


embeddings_model = HuggingFaceEmbeddings(model_name="./model")
sentence_embeddings = embeddings_model.embed_documents(sentences)
query_embedding = embeddings_model.embed_query(query)

similarities = [cosine_similarity(query_embedding, emb) for emb in sentence_embeddings]
max_index = np.argmax(similarities)  # 找到最高相似性的索引
# 打印最相似的文档块
print(f"The most similar chunk is Chunk {max_index + 1} with similarity {similarities[max_index]}:")
print(sentences[max_index])