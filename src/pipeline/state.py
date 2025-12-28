import operator
from typing import Annotated, List, Optional, Dict, Any
from typing_extensions import TypedDict
from pydantic import BaseModel

class ExtractionResult(BaseModel):
    """The structured result we want the final CSV to have."""
    value: Optional[float]
    unit: Optional[str]
    confidence: float
    source_page: int
    source_section: str
    notes: str

class AgentState(TypedDict):
    """The state of the graph for a single indicator extraction."""
    company: str
    year: int
    indicator: Any  # The Indicator dataclass object
    all_pages: Dict[int, str]  # Full document text
    
    # State that gets updated as we move through nodes
    candidate_pages: List[int]     # Pages selected by Router
    extraction_raw: Any            # <--- ADDED THIS (Intermediate LLM result)
    extraction_result: Optional[ExtractionResult] # Final validated output