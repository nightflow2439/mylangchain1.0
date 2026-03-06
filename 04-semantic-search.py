from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# 嵌入模型
embedding = OllamaEmbeddings(model="nomic-embed-text")

# 向量库（知识库）
vector_store = Chroma(
  collection_name = "example_collection",
  embedding_function = embedding,
  persist_directory = "./chroma_langchain_db"
)

# 相似度查询
results = vector_store.similarity_search(
  "What immitations does Force-aware have?"
)

for index, result in enumerate(results):
  print(index)
  print(result.page_content[:100])