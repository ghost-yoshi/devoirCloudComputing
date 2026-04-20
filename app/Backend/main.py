from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

try:
    from .api.routes import router
    from .db import Base, engine
except ImportError:
    from api.routes import router
    from db import Base, engine


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend" / "src"

app = FastAPI(
    title="Devoir Cloud Computing",
    description="CRUD minimal FastAPI + PostgreSQL",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.on_event("startup")
def on_startup() -> None:
    # For a school project, auto-creating tables keeps the setup short.
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["root"])
async def root() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api", tags=["root"])
async def api_root() -> dict:
    return {
        "name": "devoir cloud computing",
        "version": "1.0.0",
        "docs": "/docs",
    }