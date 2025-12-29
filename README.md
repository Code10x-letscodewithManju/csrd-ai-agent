
# CSRD AI Agent: Sustainability Data Extraction System

**An Agentic RAG pipeline for extracting structured ESG data from corporate Annual Reports.**

## 📌 Project Overview
This project implements an intelligent **AI Agent** designed to automate the extraction of sustainability metrics (e.g., Scope 1 Emissions, Gender Pay Gap) from complex PDF reports in compliance with the **Corporate Sustainability Reporting Directive (CSRD)**.

Unlike simple "Chat with PDF" wrappers, this system utilizes a **LangGraph-orchestrated architecture** with a "Router-Retriever" pattern. It deterministically routes specific indicators to relevant pages, extracts data using **GPT-4o** with structured output enforcement, and validates the results with a confidence scoring engine.


![CSRD AI Agent Architecture](CSRD_Agentic_RAG_Architecture_diagram.png)


### 🚀 Key Features
* **Agentic Workflow:** Built on **LangGraph** to model the extraction process as a state machine (`Route` → `Extract` → `Validate`).
* **Smart Routing:** Heuristic scoring engine filters 500+ page documents down to the top 8-15 most relevant pages per indicator, reducing token costs by ~95%.
* **Structured Extraction:** Uses **Pydantic** models to enforce strict data schemas (Value, Unit, Page Citation).
* **Validation Logic:** Assigns a **Confidence Score (0-1.0)** based on unit alignment, page citation accuracy, and data presence.
* **Audit Trail:** Every data point is linked to its source page and section for human verification.

---

## 📂 Directory Structure

```text
csrd-ai-agent/
│
├── .env                     # Environment variables (OpenAI API Key)
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── run_pipeline.py          # Main execution entry point
├── README.md                # Project documentation
│
├── data/
│   ├── raw_pdfs/            # Input: Place PDF reports here
│   ├── page_index/          # Intermediate: JSON text indexes
│   └── outputs/             # Output: Final CSV & Logs
│
├── src/
│   ├── config/
│   │   └── indicators.py    # Configuration of 20 ESRS indicators
│   │
│   ├── parsing/
│   │   ├── pdf_parser.py    # PyMuPDF wrapper for text stripping
│   │   └── page_indexer.py  # Serializes PDFs to JSON
│   │
│   ├── pipeline/            # Core LangGraph Logic
│   │   ├── state.py         # AgentState definition
│   │   ├── graph.py         # DAG construction
│   │   ├── router.py        # Heuristic page selection logic
│   │   ├── extractor.py     # GPT-4o extraction agent
│   │   ├── validator.py     # Confidence scoring logic
│   │   └── exporter.py      # CSV export handler
│   │
│   └── db/                  # Database Layer
│       ├── schema.sql       # SQLite schema
│       └── sqlite_client.py # DB interaction methods

```

---

## 🛠️ Installation & Setup

### Prerequisites

* **Python 3.10+** installed on your machine.
* **OpenAI API Key** (with access to GPT-4o or GPT-3.5-Turbo).

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd csrd-ai-agent

```

### 2. Set Up Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

**On Windows:**

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

```

**On macOS / Linux:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Environment Variables

Create a file named `.env` in the root directory and add your OpenAI API key.
*(Note: Do not commit this file to version control)*

```ini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx

```

---

## 🏃 How to Run

### 1. Prepare Data

Ensure your target PDF reports are placed in the `data/raw_pdfs/` directory.
The default configuration expects the following files:

* `data/raw_pdfs/AIBG.L_2024_Annual_Financial_Report.pdf`
* `data/raw_pdfs/BBVA_Spain_2024_Consolidated_management_report.pdf`
* `data/raw_pdfs/bpce-urd-2024.pdf`

*(You can modify the filenames in `run_pipeline.py` if needed)*

### 2. Execute the Pipeline

Run the main script to start the extraction agent. The first run will take a few moments to index the PDFs.

```bash
python run_pipeline.py

```

### 3. View Results

* **Console Logs:** Real-time extraction logs will appear in your terminal.
* **Final Output:** The structured data is saved to:
`data/outputs/final_csrd_output.csv`

---

## 🧠 System Architecture

The pipeline follows a **Directed Acyclic Graph (DAG)** flow:

1. **Ingestion:** The PDF is stripped of text and indexed into a JSON dictionary `{Page_ID: Text}`.
2. **Route Node:** For a given indicator (e.g., "Scope 1 Emissions"), the router scores all pages based on keyword density and structural signals (tables, units). The top 8 pages are selected.
3. **Extract Node:** The selected pages are concatenated and sent to **GPT-4o**. A system prompt enforces a JSON schema extraction, prioritizing "Consolidated Group" data tables.
4. **Validate Node:** The output is scored.
* *Match Unit?* (+0.3)
* *Valid Page Citation?* (+0.2)
* *Value Found?* (+0.5)


5. **Persist:** High-confidence data is written to the CSV/Database.

---

## 🔮 Future Enhancements

While the current version prioritizes precision and cost-efficiency for tabular data, the following upgrades are planned for the production roadmap:

1. **Semantic Vector Search (RAG):**
* *Current:* Keyword-based heuristic routing.
* *Future:* Implement **ChromaDB** with OpenAI embeddings to enable semantic search. This will improve recall for indicators hidden in narrative text (e.g., "Net Zero Targets" buried in CEO letters).


2. **Vision-Language Models (VLM):**
* *Current:* Text-only extraction via PyMuPDF.
* *Future:* Integrate **GPT-4o-Vision** to parse data locked in images, pie charts, and complex infographics (common for Diversity & Inclusion metrics).


3. **Human-in-the-Loop (HITL) Interface:**
* *Future:* Build a **Streamlit** dashboard that flags low-confidence extractions (< 0.8) for manual review, allowing analysts to correct data and fine-tune the system.


4. **Containerization:**
* *Future:* Dockerize the application to ensure consistent deployment across environments.



---

## 📄 License

This project is for educational and recruitment evaluation purposes.

```

```
