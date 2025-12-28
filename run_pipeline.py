import json
import os
from dotenv import load_dotenv
from src.config.indicators import INDICATORS
from src.pipeline.graph import build_graph
from src.pipeline import exporter
from src.parsing.page_indexer import build_index 

load_dotenv() 

def run_company(company, year, page_index_path, output_csv):
    # 1. Load Data
    if not os.path.exists(page_index_path):
        print(f"Skipping {company}: Index not found.")
        return

    with open(page_index_path, "r", encoding="utf-8") as f:
        pages = {int(k): v for k, v in json.load(f).items()}

    # 2. Build Agent
    app = build_graph()
    rows = []

    print(f"\n🚀 PROCESSING: {company} ({year})")

    for ind in INDICATORS:
        initial_state = {
            "company": company,
            "year": year,
            "indicator": ind,
            "all_pages": pages,
            "candidate_pages": [],
            "extraction_result": None
        }

        try:
            final_state = app.invoke(initial_state)
            result = final_state["extraction_result"]
            
            # Print result to console
            val_str = f"{result.value}" if result and result.value is not None else "NOT FOUND"
            conf_str = f"{result.confidence}" if result else "0.0"
            print(f"   🔹 {ind.name[:35]:<35} -> {val_str:<10} (Conf: {conf_str})")
            
            if result:
                rows.append({
                    "company": company,
                    "report_year": year,
                    "indicator_name": ind.name,
                    "value": result.value,
                    "unit": result.unit,
                    "confidence": result.confidence,
                    "source_page": result.source_page,
                    "source_section": result.source_section,
                    "notes": result.notes,
                })
            
        except Exception as e:
            print(f"   ❌ ERROR on {ind.name}: {e}")

    exporter.export(rows, output_csv)
    print(f"✅ Completed {company}")


if __name__ == "__main__":
    # CONFIGURATION
    output_csv = "data/outputs/final_csrd_output.csv"
    
    # Define jobs exactly matching your filenames
    jobs = [
        {
            "name": "AIB", 
            "pdf": "data/raw_pdfs/AIBG.L_2024_Annual_Financial_Report.pdf", 
            "json": "data/page_index/aib_2024.json"
        },
        {
            "name": "BBVA", 
            "pdf": "data/raw_pdfs/BBVA_Spain_2024_Consolidated_management_report.pdf", 
            "json": "data/page_index/bbva_2024.json"
        },
        {
            "name": "BPCE", 
            "pdf": "data/raw_pdfs/bpce-urd-2024.pdf", 
            "json": "data/page_index/bpce_2024.json"
        }
    ]

    for job in jobs:
        # 1. Check PDF
        if not os.path.exists(job["pdf"]):
            print(f"❌ Missing PDF: {job['pdf']}")
            continue
            
        # 2. Re-Index (Force rebuild if missing)
        if not os.path.exists(job["json"]):
            print(f"Creating Index for {job['name']}...")
            build_index(job["pdf"], job["json"])
            
        # 3. Run Pipeline
        run_company(job["name"], 2024, job["json"], output_csv)