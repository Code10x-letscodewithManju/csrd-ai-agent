from .state import ExtractionResult

def validate(state) -> dict:
    """
    Node: Validation
    Input: Raw extraction from LLM (via extraction_raw state key)
    Output: Final confidence score and clean object
    """
    raw = state.get("extraction_raw")
    indicator = state["indicator"]
    
    # DEBUG PRINT: Verify data arrival
    # print(f"   [Validator Received] {raw.value if raw else 'None'}")

    if not raw or raw.value == -1:
        # Fallback empty result
        return {"extraction_result": ExtractionResult(
            value=None, unit=indicator.unit, confidence=0.0, 
            source_page=0, source_section="", notes="Not found by AI Agent"
        )}

    # Calculate Confidence
    score = 0.5 # Base score for LLM finding something
    
    # 1. Unit Check
    if raw.unit and indicator.unit.lower() in raw.unit.lower():
        score += 0.3
    
    # 2. Page Check (Did it cite a page we actually passed?)
    if raw.page_number in state["candidate_pages"]:
        score += 0.2
        
    final_score = min(score, 1.0)

    # Create Final Result
    clean_result = ExtractionResult(
        value=raw.value,
        unit=raw.unit,
        confidence=final_score,
        source_page=raw.page_number,
        source_section=raw.section_name,
        notes=raw.context_notes
    )

    return {"extraction_result": clean_result}