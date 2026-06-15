from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx
from app.api import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # СТАРТ: создаём долгоживущие ресурсы
    app.state.http = httpx.AsyncClient(timeout=10.0)
    yield
    # ОСТАНОВКА: закрываем
    await app.state.http.aclose()

app = FastAPI(title="MOEX Bonds Analytics", lifespan=lifespan)

app.include_router(health.router)     # /api/health