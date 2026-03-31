import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from src.services.tools import retrieve_hr_docs

load_dotenv()

# ------------------- LLM -------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

# ------------------- SYSTEM PROMPT -------------------
system_prompt = """
You are an HR assistant.

You have access to a tool:
- retrieve_hr_docs → searches HR documents

STRICT RULES:

1. ALWAYS call the tool before answering
2. NEVER answer without tool data
3. Use ONLY tool output
4. If tool returns "No relevant data found", return that

5. Extract:
   - document_name from Source
   - page_no from Page

6. FINAL OUTPUT MUST BE JSON:

{
  "query": "<user_query>",
  "answer": "<final answer>",
  "Policy_citations": [
    {
      "document_name": "<source>",
      "page_no": "<page>"
    }
  ]
}

7. Include ALL relevant citations
8. Do NOT hallucinate
9. Output ONLY JSON

Steps:
- Call tool
- Read documents
- Answer
"""

# ------------------- AGENT -------------------
agent = create_agent(
    model=llm,
    tools=[retrieve_hr_docs],
    system_prompt=system_prompt
)

# ------------------- QUERY FUNCTION -------------------
def query_rag(user_query: str):
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_query}
        ]
    })

    return response