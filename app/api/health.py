from fastapi import APIRouter
router = APIRouter(prefix="/api", tags=["health"])

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}           # критерий готовности Этапа 0: /health отвечает