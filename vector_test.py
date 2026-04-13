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
    results = retriever.invoke("Show Google reviews")
    print(f"✓ Got {len(results)} results")
except Exception as e:
    print(f"✗ Query failed: {e}")
    exit(1)

print("Step 2: Printing results ...")
for i, doc in enumerate(results, 1):
    print(f"\n--- Result {i} ---")
    print(f"Content: {doc.page_content[:200]}...")