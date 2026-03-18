## 索引
# 1. 读取网页，Document, List[Document]
# 2. 分割文本，文本段（chunk），Document, List[Document]
# 3. 向量化：文本段 <=> 向量，需要嵌入模型来辅助
# 4. 向量库：把多个文本段/向量存到向量库，OK了。

# pip install bs4

# 1. 读取网页，Document, List[Document]
from langchain_community.document_loaders import WebBaseLoader
import bs4, os, shutil

if os.path.exists("./chroma_rag_db"):
  shutil.rmtree("./chroma_rag_db")

page_url = "https://developer.aliyun.com/article/1716726"

bs4_strainer = bs4.SoupStrainer()

loader = WebBaseLoader(
  web_path=(page_url),
  bs_kwargs={"parse_only": bs4_strainer}
)

docs = loader.load()

print(len(docs))
print(type(docs[0]))
print(docs[0])

# 2. 分割文本，文本段（chunk），Document, List[Document]
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size = 1000,
  chunk_overlap = 200,
  add_start_index = True
)

all_splits = text_splitter.split_documents(docs)

print(len(all_splits))
print(all_splits[0])

# 3. 向量化：文本段 <=> 向量，需要嵌入模型来辅助
from langchain_ollama import OllamaEmbeddings

embedding = OllamaEmbeddings(model='nomic-embed-text:latest')

# 4. 文本块/向量存储
from langchain_chroma import Chroma
vector_store = Chroma(
  collection_name = "rag_collection",
  embedding_function = embedding,
  persist_directory = "./chroma_rag_db"
)

ids = vector_store.add_documents(documents=all_splits)

print(len(ids))
print(ids)