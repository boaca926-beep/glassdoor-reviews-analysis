"""
    Inspect csv file and convert it into json file
"""

import pandas as pd
import json

# Read the CSV file
cvs_file='Glassdoor-dataset-samples/glassdoor-companies-reviews.csv'
df = pd.read_csv(cvs_file)

# Display first 5 rows
print(df.head(5))

# Convert to JSON and save
json_file='Glassdoor-dataset-samples/glassdoor_review.json'
df.to_json(json_file, orient='records', indent=2)

print("Successfully converted to glassdoor_revies.json")

# Inspect josn file
# Load the JSON file
if json_file:
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

# See the type and structure
print(f"Type of data: {type(data)}")
print(f"Number of items: {len(data) if isinstance(data, list) else 'N/A'}")

# Print the ENTIRE first review (all fileds)
sample = data[0]
print(json.dumps(sample, indent=2))

# Sample filed inspection
print("Fileds in your Glassdoor data:")
for field in sample.keys():
    value = sample[field]
    print(f"    *{field}: {type(value).__name__} = {str(value)[:50]}...")

# View first 2 items (if it's a list)
if isinstance(data, list): # True if the object matches the list, False otherwise
    print("\n=== First 2 reviews ===\n")
    for i, item in enumerate(data[:2]):
        print(f"--- Review {i+1} ---")
        print(json.dumps(item, indent=2)[:500]) # First 500 chars 
        print("...\n")

