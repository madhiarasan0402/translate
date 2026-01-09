from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routers import translation
import uvicorn
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Video Language Translator",
    description="AI-powered video translation service",
    version="1.0.0"
)

# CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(translation.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok", 
        "time": time.strftime("%H:%M:%S"),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

if __name__ == "__main__":
    # Local development server
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0",  # Changed from 127.0.0.1 to work with Render
        port=port, 
        reload=True
    )
