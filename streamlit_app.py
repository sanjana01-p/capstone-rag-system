import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1/query"

st.title("RAG Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask something")

if st.button("Send"):
    res = requests.post(API_URL, json={"query": user_input})

    st.write("Status Code:", res.status_code)
    st.write("Raw Response:", res.text)   # 👈 ADD THIS

    data = res.json()

    answer = data.get("answer")

    st.session_state.history.append((user_input, answer))

for q, a in st.session_state.history:
    st.write(f"**You:** {q}")
    st.write(f"**Bot:** {a}")