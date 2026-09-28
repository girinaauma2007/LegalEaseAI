from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routes import router

app = FastAPI(title=settings.app_name, version="1.0.0", description="AI-powered legal document drafting API.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def root():
    return {"app": settings.app_name, "status": "running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
