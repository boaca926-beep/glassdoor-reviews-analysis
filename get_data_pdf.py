from langchain_community.document_loaders import PyPDFLoader
import re
import pandas as pd

def load_pdf_with_enhanced_metadata(pdf_path, custom_metadata=None):
    """Load PDF and enhance metadata automatically"""
    
    # Load the PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    # Auto-extract from filename
    filename = pdf_path.split('/')[-1]
    name_without_ext = filename.replace('.pdf', '')
    
    # Try to guess document type from filename
    doc_type = "unknown"
    if "CV" in name_without_ext or "resume" in name_without_ext.lower():
        doc_type = "resume"
    elif "report" in name_without_ext.lower():
        doc_type = "report"
    elif "paper" in name_without_ext.lower():
        doc_type = "academic_paper"
    
    # Apply to all pages
    for page in pages:
        page.metadata.update({
            "filename": filename,
            "doc_type": doc_type,
            "loaded_at": str(pd.Timestamp.now()),  # When it was loaded
        })
        
        # Add any custom metadata passed in
        if custom_metadata:
            page.metadata.update(custom_metadata)
    
    return pages

# Usage - automatic with optional manual overrides
pages = load_pdf_with_enhanced_metadata(
    "/home/bo_ml/Downloads/CV_Bo.pdf",
    custom_metadata={
        "author": "Bo",
        "department": "AI Research",
        "reviewed": False
    }
)

# Check the enhanced metadata
for page in pages:
    print(f"Loaded {len(pages)} pages")
    print(page.page_content[:100])  # First 100 chars of the first page
    print(page.metadata)  # Metadata like {'source': './my_document.pdf', 'page': 0}

