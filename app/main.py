from fastapi import FastAPI
from app.api import health

app = FastAPI(title="MOEX Bonds Analytics")

app.include_router(health.router)     # /api/health