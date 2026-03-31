import streamlit as st
import requests


API_QUERY = "http://localhost:8000/api/v1/query"
API_UPLOAD = "http://localhost:8000/api/v1/admin/upload"

ADMIN_PASSWORD = "admin123"


st.set_page_config(page_title="RAG Assistant", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

[data-testid="stChatMessage"] {
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 1px solid #e5e7eb;
}

.stButton>button {
    border-radius: 8px;
    border: 1px solid #d1d5db;
    background-color: #ffffff;
    padding: 6px 14px;
}

.stButton>button:hover {
    border-color: #6366f1;
    color: #6366f1;
}

details {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 8px;
}

[data-testid="stFileUploader"] {
    border: 1px dashed #cbd5e1;
    padding: 12px;
    border-radius: 10px;
    background-color: #ffffff;
}

.small-text {
    color: #6b7280;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


if "role" not in st.session_state:
    st.session_state.role = None

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.markdown("### RAG Assistant")
    st.markdown("---")

    if st.session_state.role:
        st.markdown(f"Role: **{st.session_state.role.capitalize()}**")

        if st.button("Logout"):
            st.session_state.role = None
            st.session_state.messages = []
            st.rerun()


if st.session_state.role is None:
    st.title("Login")

    role = st.selectbox("Select Role", ["User", "Admin"])

    if role == "Admin":
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("Invalid password")
    else:
        if st.button("Continue"):
            st.session_state.role = "user"
            st.rerun()

    st.stop()


st.markdown("## Credit-Risk Assistant")
st.divider()

def format_insight(content):
    points = []

    if isinstance(content, list):
        content = " ".join([str(c) for c in content])

    if not isinstance(content, str):
        return []

    lines = content.split("Q:")

    for line in lines:
        if "A:" in line:
            try:
                _, a_part = line.split("A:")
                answer = a_part.strip().replace("\n", " ")
                answer = answer[:120]
                points.append(f"- {answer}")
            except:
                continue

    return points[:3]

if st.session_state.role == "admin":

    st.markdown("### Document Management")

    uploaded_file = st.file_uploader("Upload document", type=["pdf", "txt"])

    if uploaded_file:
        if st.button("Upload File"):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        uploaded_file.type
                    )
                }

                res = requests.post(API_UPLOAD, files=files)

                if res.status_code == 200:
                    st.success(f"{uploaded_file.name} uploaded successfully")
                else:
                    st.error(res.text)

            except:
                st.error("Upload failed")




elif st.session_state.role == "user":

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            if msg.get("insights"):
                with st.expander("View details"):
                    for insight in msg["insights"]:
                        st.markdown(insight)
                        st.markdown("---")


    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.chat_message("user").markdown(user_input)

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            res = requests.post(API_QUERY, json={"query": user_input})
            data = res.json()
        except:
            st.error("Backend connection failed")
            st.stop()

        raw_answer = data.get("answer", "")

        if isinstance(raw_answer, list):
            answer = raw_answer[0].get("text", "")
        else:
            answer = raw_answer

        answer = str(answer).strip()

     
        no_answer_phrases = [
            "i don't know",
            "i do not know",
            "not available",
            "no information",
            "cannot find",
            "not found"
        ]

        is_no_answer = any(p in answer.lower() for p in no_answer_phrases)

        if is_no_answer:
            answer = "I Don't Know."

       
        insights = []

        if not is_no_answer:
            for i, doc in enumerate(data.get("results", [])[:3]):
                content = doc.get("content", "")
                page = doc.get("metadata", {}).get("page", "N/A")

                if not isinstance(content, str):
                    content = str(content)

                formatted = format_insight(content)

                if formatted:
                    text = f"Snippet {i+1} (Page {page})\n" + "\n".join(formatted)
                    insights.append(text)

    
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""

            for word in answer.split():
                full += word + " "
                placeholder.markdown(full + "▌")

            placeholder.markdown(full)

            if insights:
                with st.expander("View details"):
                    for ins in insights:
                        st.markdown(ins)
                        st.markdown("---")

        
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "insights": insights
        })