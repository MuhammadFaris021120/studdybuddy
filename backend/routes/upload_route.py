from fastapi import APIRouter, UploadFile, File,Request
from services.file_parser import extract_text_from_pdf, extract_text_from_image
from vectorstore.rag_handler import store_and_query_vector
from services.quiz_generator import generate_quiz
from db.mongo import documents_collection
from datetime import datetime
import os
from pydantic import BaseModel

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    contents = await file.read()
    
    # Save file temporarily
    file_path = f"temp_{filename}"
    with open(file_path, "wb") as f:
        f.write(contents)

    # Extract text
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        text = extract_text_from_image(file_path)
    else:
        return {"error": "Unsupported file type"}

    os.remove(file_path)

    # Store in vector and ask RAG
    rag_response = store_and_query_vector(text, "Summarize this file")
    quiz = generate_quiz(text)

    document_data = {
    "filename": file.filename,
    "text": text,
    "summary": rag_response,
    "quiz": quiz,
    "uploaded_at": datetime.utcnow()
    }

    documents_collection.insert_one(document_data)

    return {
        "summary": rag_response,
        "quiz": quiz
    }

class AskRequest(BaseModel):
    content: str  # the extracted file text
    question: str

@router.post("/ask")
async def ask_question(payload: AskRequest):
    response = store_and_query_vector(payload.content, payload.question)
    return {"answer": response}

@router.get("/documents")
def get_all_documents():
    docs = list(documents_collection.find({}, {"_id": 0}))
    return docs
