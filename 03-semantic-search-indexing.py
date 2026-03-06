## 索引
# 1. 读取PDF，按页管理，Document, List[Document]
# 2. 分割文本，文本段（chunk），Document, List[Document]
# 3. 向量化：文本段 <=> 向量，需要嵌入模型来辅助
# 4. 向量库：把多个文本段/向量存到向量库，OK了。

# pip install pypdf

# 1. 读取PDF，按页管理，Document, List[Document]
from langchain_community.document_loaders import PyPDFLoader

file_path = "2505.20829v2.pdf"

loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs)) # 18
print(type(docs[0])) # <class 'langchain_core.documents.base.Document'>
print(docs[0])
# page_content='...' 
# metadata={
# 'producer': 'pikepdf 8.15.1', 
# 'creator': 'arXiv GenPDF (tex2pdf:)', 
# 'creationdate': '', 
# 'author': 'Peiyuan Zhi; Peiyang Li; Jianqin Yin; Baoxiong Jia; Siyuan Huang', 
# 'doi': 'https://doi.org/10.48550/arXiv.2505.20829', 
# 'license': 'http://arxiv.org/licenses/nonexclusive-distrib/1.0/', 
# 'ptex.fullbanner': 'This is pdfTeX, Version 3.141592653-2.6-1.40.28 (TeX Live 2025) kpathsea version 6.4.1', 
# 'title': 'Learning a Unified Policy for Position and Force Control in Legged Loco-Manipulation', 
# 'trapped': '/False', 
# 'arxivid': 'https://arxiv.org/abs/2505.20829v2', 
# 'source': '2505.20829v2.pdf', 
# 'total_pages': 18, 
# 'page': 0, 
# 'page_label': '1'
# }