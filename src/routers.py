from fastapi import APIRouter, HTTPException
from src.schemas import TextRequest, TextResponse, KnowledgeRequest, QuestionRequest
import src.ai_engine as ai

router = APIRouter()

@router.post("/summarize", response_model=TextResponse)
async def summarize_endpoint(request: TextRequest):
    try:
        summary = ai.generate_summary(request.text)
        return TextResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-knowledge")
async def upload_endpoint(request: KnowledgeRequest):
    try:
        message = ai.save_to_vector_db(request.text, request.source_name)
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
async def ask_endpoint(request: QuestionRequest):
    try:
        result = ai.ask_rag_system(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))