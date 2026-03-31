from langchain.tools import tool
from src.services.query_service import query_documents


@tool
def retrieve_hr_docs(query: str) -> str:
    """
    Search HR policy documents.
    Automatically performs keyword, hybrid, or vector search.
    Returns formatted document chunks with source and page.
    """

    docs = query_documents(query, k=5)

    if not docs:
        return "No relevant data found"

    results = []

    for i, doc in enumerate(docs):
        content = doc.get("content", "").strip()
        metadata = doc.get("metadata", {}) or {}

        source = metadata.get("source", "unknown")
        page = metadata.get("page", "N/A")

        results.append(
            f"[Document {i+1}]\n"
            f"Content: {content}\n"
            f"Source: {source}\n"
            f"Page: {page}"
        )

    return "\n\n".join(results)