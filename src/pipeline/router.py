def get_top_pages(indicator, pages: dict) -> list[int]:
    """
    Scoring logic to find the Data Tables, not just narrative text.
    """
    keywords = [k.lower() for k in indicator.keywords]
    unit = indicator.unit.lower()
    scored_pages = []

    for page_num, text in pages.items():
        text_lower = text.lower()
        score = 0
        
        # 1. Keyword Match (Base Score)
        for k in keywords:
            if k in text_lower: 
                score += 2
        
        # 2. Strong Signal: Unit Match (The page MUST have the unit)
        if unit in text_lower:
            score += 5  # Huge boost for finding "tCO2e" or "MWh"
            
        # 3. Year Match (Data tables always have the year)
        if "2024" in text_lower or "2023" in text_lower:
            score += 2
            
        # 4. Table Context (Words often found near ESG tables)
        if "performance" in text_lower or "table" in text_lower or "data" in text_lower:
            score += 1

        if score > 0:
            scored_pages.append((page_num, score))

    # Sort by score descending
    scored_pages.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 15 pages (Increased from 10 to catch buried tables)
    return [p for p, _ in scored_pages[:15]]

def route_node(state):
    top_pages = get_top_pages(state["indicator"], state["all_pages"])
    return {"candidate_pages": top_pages}