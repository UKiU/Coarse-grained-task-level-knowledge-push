from sentence_transformers import SentenceTransformer
# 联网下载
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
# 本地加载 
model = SentenceTransformer('/home/Work/00.Work_muyu/langchain/bge-large-zh-v1.5')
query = "早睡早起到底是不是保持身体健康的标准？"
sentences = ["早睡早起确实是保持身体健康的重要因素之一。它有助于同步我们的生物钟，并提高睡眠质量。", 
             "早睡早起可以帮助人们更好地适应自然光周期，从而优化褪黑激素的产生，这种激素是调节睡眠和觉醒的关键。",
             "关于提高工作效率，确保在日常饮食中包含充足的蛋白质、复合碳水化合物和健康脂肪非常关键。"
           ]
sen_embeddings = model.encode(sentences)
query_embedding = model.encode(query)

from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings_model = HuggingFaceEmbeddings(model_name="/home/Work/00.Work_muyu/langchain/bge-large-zh-v1.5")
query =…
sentences =…
sentence_embeddings = embeddings_model.embed_documents(sentences)
embedded_query = embeddings_model.embed_query(query)

