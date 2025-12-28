import fitz  # PyMuPDF

def extract_pages(pdf_path: str) -> dict:
    """
    Opens PDF and extracts text page by page.
    Returns: { 1: "text on page 1", 2: "text on page 2"... }
    """
    pages = {}
    
    try:
        with fitz.open(pdf_path) as doc:
            for i, page in enumerate(doc):
                # Extract text preserving physical layout (good for tables)
                text = page.get_text("text") or ""
                
                # If page is empty, try extracting blocks
                if len(text.strip()) < 10:
                    blocks = page.get_text("blocks")
                    text = "\n".join([b[4] for b in blocks])
                
                # Store with 1-based index
                pages[i + 1] = text
    except Exception as e:
        print(f"Error parsing PDF {pdf_path}: {e}")
        return {}

    return pages