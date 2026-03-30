from fastapi import APIRouter
from src.api.v1.schemas.query_schema import QueryRequest, QueryResponse, QueryResult
from src.services.agent import query_rag

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_api(request: QueryRequest):

    if not request.query or len(request.query) < 3:
        return {"error": "Invalid query"}

    result = query_rag(request.query)

    docs = result["documents"]

    results = [
        QueryResult(
            content=doc.page_content,
            metadata=doc.metadata
        )
        for doc in docs
    ]

    return QueryResponse(
        query=request.query,
        answer=result["answer"],
        results=results
    )