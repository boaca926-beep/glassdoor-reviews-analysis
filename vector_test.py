"""
    Test if retriever works
"""
print("Step 1: Importing retriever ...")
try: 
    from vector import retriever
    print("✓ Retriever imported successfully")
except Exception as e:
    print(f"✗ Failed to import retriever: {e}")
    exit(1)

print("\nStep 2: Invoking retriever...")
try:
    results = retriever.invoke(
        "work life balance company culture",
        filter={"company": "Google"}) # Only specific company: Google
    print(f"✓ Got {len(results)} results")
except Exception as e:
    print(f"✗ Query failed: {e}")
    exit(1)

print("Step 2: Printing results ...")
for i, doc in enumerate(results, 1):
    print(f"\n--- Result {i} ---")
    if hasattr(doc, 'metadata') and doc.metadata:
        print(f"Company: {doc.metadata.get('company', 'N/A')}")
        print(f"Rating: {doc.metadata.get('rating', 'N/A')}/5.0")
        print(f"Date: {doc.metadata.get('date', 'N/A')}")
    print(f"\nFull Review Text:")
    print("-" * 40)
    print(doc.page_content)  # Full content, not truncated
    print("-" * 40)
    #print(f"Content: {doc.page_content[:200]}...")