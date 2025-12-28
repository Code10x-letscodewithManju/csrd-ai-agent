import csv
import os

FIELDS = [
    "company", "report_year", "indicator_name", 
    "value", "unit", "confidence", 
    "source_page", "source_section", "notes"
]

def export(rows, output_path):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    file_exists = os.path.exists(output_path)
    
    with open(output_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        
        # Write header if new file
        if not file_exists:
            writer.writeheader()
            
        # Clean rows before writing
        clean_rows = []
        for r in rows:
            # Handle None values gracefully
            clean_r = r.copy()
            if clean_r.get("value") is None:
                clean_r["value"] = ""
            if clean_r.get("confidence") is None:
                clean_r["confidence"] = 0.0
            clean_rows.append(clean_r)

        writer.writerows(clean_rows)
    
    print(f"Results appended to {output_path}")