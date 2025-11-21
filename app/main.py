# ============= app/main.py =============
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import jobs

app = FastAPI(
    title="Job Scraper API",
    description="API para recolectar y consultar ofertas de trabajo para prácticas profesionales",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos
@app.on_event("startup")
def on_startup():
    init_db()

# Incluir routers
app.include_router(jobs.router)

@app.get("/")
def read_root():
    return {
        "message": "Job Scraper API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}