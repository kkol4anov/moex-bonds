from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}           # Stage 0 is ready if /health responds