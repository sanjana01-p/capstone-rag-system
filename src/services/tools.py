from langchain.tools import tool
from src.core.db import get_vector_store

@tool
def retrieve_docs(query: str) -> str:
    """
    Use this tool to search documents from the knowledge base.
    """
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant documents found."

    context = "\n\n".join([doc.page_content for doc in docs])
    return context