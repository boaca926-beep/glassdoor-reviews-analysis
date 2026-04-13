"""
    Import all relevant data
"""
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
import shutil
import chromadb
from chromadb.config import Settings

# Add this function to truncate text
def truncate_text(text, max_chars=1000):  # Adjust based on your needs
    """Truncate text to avoid exceeding model's context length"""
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text

"""
    Bring in json file
"""
jsonf_file = "./Glassdoor-dataset-samples/glassdoor_review.json"
df = pd.read_json(jsonf_file)

"""
    Check ollama models: ollama list
"""
#embeddings = OllamaEmbeddings(model="mxbai-embed-large") # 512 tokens, not natively support GPU acceleration
embeddings = OllamaEmbeddings(model="nomic-embed-text") # 8192 tokens, supports GPU
#embeddings = OllamaEmbeddings(model="all-minilm") # very fast, GPU support



"""
    Check if the database location is already exist in chrome,
    convert it into documents
"""
db_location = "./chroma_langchain_db"
if os.path.exists(db_location):
    print(f"Deleting existing database at {db_location}")
    shutil.rmtree(db_location)
    print("Old database deleted")

add_documents = not os.path.exists(db_location)


if add_documents:
    documents = []
    ids = []

    for i,row in df.iterrows():
        company_name = row.get("company_name", "Unknown Company")
        review_pros = row.get("review_pros", "No pros listed")

        # Truncate the review if it's too long
        #review_pros = truncate_text(review_pros, max_chars=800) # needed if using embeddings mxbai-embed-large

        page_content = f"{company_name} {review_pros}"

        document = Document(       
            page_content=page_content,
            metadata={
                "company": company_name,
                "rating": row.get("rating_overall", "N/A"), 
                "date": row.get("rating_date", "Unknown")
            },
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

"""
    Initialize the vectorization
"""
vector_store = Chroma(
    collection_name="job_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

"""
    Add the data into the vector store only if data base location exists.
"""
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

"""
    Inspect chroma_langchain_db
"""
# Get collection info
print(f"Collection name: {vector_store._collection.name}")
print(f"Number of documents: {vector_store._collection.count()}")

# Get all documents (returns list of IDs)
all_ids = vector_store.get()['ids']
print(f"All document IDs: {all_ids[:5]}...") # first 5 IDs

# Get specific documents with metadata
results = vector_store.get(limit=10) # Get first 10 documents
print(f"\nRetrieved {len(results['ids'])} documents")
for i, (doc_id, metadata, doc) in enumerate(zip(results['ids'], results['metadatas'], results['documents'])):
    print(f"\nDocument {i+1}:")
    print(f"    ID: {doc_id}")
    print(f"    Content: {doc[:500]}..." if len(doc) > 100 else f" Content: {doc}")
    print(f"    Metadata: {metadata}")

# Query by metada
google_docs = vector_store._collection.get(
    where={"company": "Google"},
    limit=20
)
print(f"\nGoogle documents: {len(google_docs['ids'])}")

# Full Google documents
if len(google_docs['ids']) > 0:
    print("\nSample Google document:")
    for i in range(min(3, len(google_docs['ids']))):
        print(f"    ID: {google_docs['ids'][i]}")
        print(f"    Content: {google_docs['documents'][i][:500]}...")
        print(f"    Metadata: {google_docs['metadatas'][i]}")
        print()

