"""
    Vectorize unstructured data: pdf example
"""

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter  # ✅ New wayfrom langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import pandas as pd
import shutil
import os
import re # for text cleaning

# Change 3: Add simple cleaning function
def clean_text(text):
    """Minimal cleaning for PDF artifacts"""
    text = text.replace(']\n', '\n')  # Remove stray brackets with newlines
    text = text.replace('] ', ' ')    # Remove stray brackets with spaces
    text = re.sub(r'(\w)\n(\w)', r'\1 \2', text)  # Fix line breaks in words
    return text.strip()

# Load with enhanced metadata
pdf_path = "/home/bo_ml/Downloads/CV_Bo.pdf"
#loader = PyPDFLoader(pdf_path)
loader = PyMuPDFLoader(pdf_path)
pages = loader.load()
print(f"Loaded {len(pages)} pages")

# Enhance metadata
for i, page in enumerate(pages):
    page.page_content = clean_text(page.page_content)

    page.metadata.update({
        "author": "Bo",
        "doc_type": "resume",
        "department": "AI Research",
        "loaded_at": str(pd.Timestamp.now()),
        "reviewed": False,
        "filename": pdf_path.split('/')[-1]
    })

# Split into chunks (metadata automatically preserved!)


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

'''
# Sentence-aware splitting
text_splitter = SentenceTransformersTokenTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    model_name="sentence-transformers/all-mpnet-base-v2"
)
'''

chunks = text_splitter.split_documents(pages)
print(f"Created {len(chunks)} chunks")

# Print metadata of first chunk
print("\nFirst chunk metadata:")
print(chunks[0].metadata)

# Initialize embeddings and vector store
embeddings = OllamaEmbeddings(model="nomic-embed-text")  # or "mxbai-embed-large"

# Setup database location
db_location = "./chroma_cv_db"

# Delete existing database if you want fresh start
if os.path.exists(db_location):
    print(f"\nDeleting existing database at {db_location}")
    shutil.rmtree(db_location)

# Create vector store
vector_store = Chroma(
    collection_name="cv_documents",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Add chunks to vector store
print(f"\nAdding {len(chunks)} chunks to vector store...")
vector_store.add_documents(documents=chunks)
print("Documents added successfully!")

# Now you can do filtered searches
print("\n" + "="*50)
print("SEARCHING FOR BO'S EDUCATIONAL BACKGROUND")
print("="*50)

results = vector_store.similarity_search(
    "What is Bo's educational background?",
    filter={"$and": [{"author": "Bo"}, {"doc_type": "resume"}]},
    k=3
)

# Results include metadata for citation
print(f"\nFound {len(results)} results:\n")
for i, doc in enumerate(results):
    print(f"Result {i+1}:")
    print(f"  Source: {doc.metadata.get('filename', 'Unknown')}")
    print(f"  Page: {doc.metadata.get('page', doc.metadata.get('page_number', 'Unknown'))}")
    print(f"  Author: {doc.metadata.get('author', 'Unknown')}")
    print(f"  Department: {doc.metadata.get('department', 'Unknown')}")
    print(f"  Content: {doc.page_content[:150]}...")
    print()

# Optional: Search for other topics
print("\n" + "="*50)
print("SEARCHING FOR TECHNICAL SKILLS")
print("="*50)

skills_results = vector_store.similarity_search(
    "What programming languages and technical skills does Bo have?",
    k=3
)

for i, doc in enumerate(skills_results):
    print(f"\nResult {i+1}:")
    print(f"  Page: {doc.metadata.get('page_label', 'Unknown')}")
    print(f"  Content: {doc.page_content[:150]}...")