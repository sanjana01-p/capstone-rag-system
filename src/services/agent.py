from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.db import get_vector_store

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   # use latest
    temperature=0.3
)

# Vector store 
vector_store = get_vector_store()

def query_rag(user_query: str):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Step 1: Retrieve docs
    docs = retriever.invoke(user_query)

    # Step 2: Build context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Step 3: Prompt
    prompt = f"""
You are an HR assistant.

Answer ONLY from the context.
If not found, say "I don't know".

Context:
{context}

Question:
{user_query}
"""

    # Step 4: LLM call
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "documents": docs
    }