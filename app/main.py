from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx
from app.api import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # START: creating long-lived resources
    app.state.http = httpx.AsyncClient(timeout=10.0)
    yield
    # STOP: closing
    await app.state.http.aclose()

app = FastAPI(title="MOEX Bonds Analytics", lifespan=lifespan)

app.include_router(health.router)     # /api/health