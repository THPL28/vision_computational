# app/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers import vision

app = FastAPI()

# Configuração diretório para arquivos estáticos (como HTML)
app.mount("/static", StaticFiles(directory="templates"), name="static")

# Configuração templates Jinja2
templates = Jinja2Templates(directory="templates")

# Roteamento da API
app.include_router(vision.router)

# Rota para servir o formulário HTML
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
