from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.config import settings
from app import migrate
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc"
)

migrate.run()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

@app.get("/")
async def read_root():
    return RedirectResponse(url=f"{settings.API_PREFIX}/docs")

@app.get("/health")
async def health_check():
    db_status = "ok" if migrate.check_db() else "error"
    return {"status": db_status}