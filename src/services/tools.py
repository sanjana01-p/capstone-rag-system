from langchain.tools import tool
from src.services.query_service import query_documents


@tool
def retrieve_hr_docs(query: str) -> str:
    """
    Retrieve relevant HR documents based on the user query.
    """
    docs = query_documents(query, k=5)

    if not docs:
        return "No relevant data found"

    results = []

    for i, doc in enumerate(docs):
        content = doc.get("content", "").strip()
        metadata = doc.get("metadata", {}) or {}

        source = metadata.get("source", "Unknown Document")
        page = metadata.get("page", "N/A")
        section = metadata.get("section", "General")

        results.append(
            f"Document {i+1}\n"
            f"Content: {content}\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Section: {section}"
        )

    return "\n\n".join(results)