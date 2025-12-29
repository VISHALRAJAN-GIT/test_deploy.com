from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(__file__))
from ai_engine import get_python_help

app = FastAPI(title="Python Syntax AI Assistant")

# Data model for chat requests
class ChatRequest(BaseModel):
    query: str
    dataset_context: str = ""

# API Endpoint for chat
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = get_python_help(request.query, request.dataset_context)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (Frontend)
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
frontend_dir = BASE_DIR / "frontend"

if not frontend_dir.exists():
    frontend_dir.mkdir(parents=True, exist_ok=True)

app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
