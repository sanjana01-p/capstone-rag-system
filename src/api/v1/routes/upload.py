from fastapi import APIRouter, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.db import get_vector_store
import tempfile

router = APIRouter()

@router.post("/admin/upload")
async def upload_file(file: UploadFile = File(...)):
    print("🔥 Upload started")

    suffix = file.filename.split('.')[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    print("✅ File saved")

    if suffix == "pdf":
        loader = PyPDFLoader(tmp_path)
    elif suffix == "txt":
        loader = TextLoader(tmp_path)
    else:
        return {"error": "Only PDF and TXT supported"}

    docs = loader.load()
    print(f"📄 Loaded {len(docs)} docs")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)
    print(f"✂️ Created {len(chunks)} chunks")

    vector_store = get_vector_store()
    print("⚙️ Adding to vector DB...")

    vector_store.add_documents(chunks)

    print("✅ Done storing")

    return {"message": "File processed and stored successfully"}