import json
import os
from .pdf_parser import extract_pages

def build_index(pdf_path: str, output_path: str):
    print(f"Indexing {pdf_path}...")
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return

    # Extract text
    raw_pages = extract_pages(pdf_path)
    
    # Clean whitespace
    indexed_pages = {k: " ".join(v.split()) for k, v in raw_pages.items()}

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(indexed_pages, f, indent=2, ensure_ascii=False)
        
    print(f"Index saved to {output_path}")