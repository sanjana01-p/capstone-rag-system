from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    query: str


class Citation(BaseModel):
    document_name: str
    page_no: str


class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: List[Citation]