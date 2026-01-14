import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import vision

# Setup Professional Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VisionAI")

app = FastAPI(
    title="Vision AI Pro Enterprise",
    description="Computer Vision Suite featuring YOLOv3 & MediaPipe",
    version="2.0.0",
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redoc"
)

# Professional Health Check
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "engine": "Vision AI Pro", "version": "2.0.0"}

# Certificar que os diretórios existem
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount Static and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include Router with API versioning (simulated prefix)
app.include_router(vision.router)

@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal Server Error Level Google - Consult Logs"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
