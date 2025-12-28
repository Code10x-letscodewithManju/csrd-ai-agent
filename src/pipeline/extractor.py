import os
import re
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field 

class LLMExtraction(BaseModel):
    value_raw: str = Field(description="The numeric value as text (e.g. '4,205' or '42.5'). Use '-1' if not found.")
    unit: str = Field(description="The unit found.")
    page_number: int = Field(description="Page number.")
    section_name: str = Field(description="Section name.")
    context_notes: str = Field(description="Brief notes.")

def _clean_value(raw_val: str) -> Optional[float]:
    if not raw_val or raw_val == "-1": return None
    clean = re.sub(r"[^\d\.-]", "", raw_val)
    try:
        return float(clean)
    except ValueError:
        return None

import time
def extract(state) -> dict:
    time.sleep(2)
    indicator = state["indicator"]
    candidate_pages = state["candidate_pages"]
    all_pages = state["all_pages"]

    # 1. Prepare Context (Top 8 pages)
    context_text = ""
    valid_pages = candidate_pages[:8]
    for p in valid_pages:
        context_text += f"\n--- PAGE {p} ---\n{all_pages.get(p, '')[:3000]}\n"

    # 2. Setup LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    
    # 3. Prompt
    system_prompt = """You are an ESG Analyst. Extract: "{indicator_name}" (Unit: {indicator_unit}).
    Target Year: {report_year} (or 2023 if 2024 is missing).
    
    RULES:
    - Look for DATA TABLES.
    - If value is '4,200', return '4,200'.
    - If not found, return '-1'.
    """

    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("user", "{context}")])
    extract_chain = prompt | llm.with_structured_output(LLMExtraction)

    try:
        response = extract_chain.invoke({
            "indicator_name": indicator.name,
            "indicator_unit": indicator.unit,
            "report_year": state["year"],
            "context": context_text
        })
        
        # --- DEBUG PRINT (This is what you need to see) ---
        print(f"   [LLM SAW] Value: {response.value_raw} | Page: {response.page_number}")
        # --------------------------------------------------

        cleaned_val = _clean_value(response.value_raw)
        
        if cleaned_val is None:
            result = None
        else:
            class TempResult:
                value = cleaned_val
                unit = response.unit
                page_number = response.page_number
                section_name = response.section_name
                context_notes = response.context_notes
            result = TempResult()

    except Exception as e:
        print(f"   [LLM Error] {e}")
        result = None

    return {"extraction_raw": result}