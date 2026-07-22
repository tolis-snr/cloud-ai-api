from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    summary: str

class KnowledgeRequest(BaseModel):
    text: str
    source_name: str

class QuestionRequest(BaseModel):
    question: str