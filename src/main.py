from fastapi import FastAPI
from src.routers import router

app = FastAPI(title="Cloud AI RAG API - Modular Architecture")

# Include the endpoints from routers.py
app.include_router(router)