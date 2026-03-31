import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from src.services.tools import retrieve_hr_docs

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

system_prompt = """
You are an HR assistant.

You have access to a tool:
- retrieve_hr_docs

STRICT RULES:

1. ALWAYS call the tool before answering
2. Use ONLY tool output
3. If tool returns "No relevant data found", return that

Extract:
- document_name from Source
- page_no from Page
- section from Section

FINAL OUTPUT MUST BE JSON:

{
  "query": "<user_query>",
  "answer": "<final answer>",
  "document_name": "<source>",
  "page_no": "<page>",
  "section": "<section>"
}

Include ALL citations.
Do NOT hallucinate.
Output ONLY JSON.
"""

agent = create_agent(
    model=llm,
    tools=[retrieve_hr_docs],
    system_prompt=system_prompt
)

def query_rag(user_query: str):
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_query}
        ]
    })

    return response