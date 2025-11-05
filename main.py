# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from api.qna import router as qna_router

# === PATHS ===
PROJECT_ROOT = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=PROJECT_ROOT / "templates")

app = FastAPI(
    title="LYZR Clinic QnA",
    description="AI-powered clinic assistant",
    version="1.0.0"
)

app.include_router(qna_router, prefix="/qna")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})