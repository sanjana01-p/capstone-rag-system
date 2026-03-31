from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Request ---
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="User query")
    category: Optional[str] = Field(
        default=None,
        description="Optional metadata filter"
    )

# --- Retrieved Chunk ---
class QueryResult(BaseModel):
    content: str
    metadata: Dict[str, Any]

# --- Response (UPDATED) ---
class QueryResponse(BaseModel):
    query: str
    answer: List[Dict[str, Any]]   
    results: List[QueryResult] 
