from fastapi import APIRouter

from backend.app.api.routes import auth, dashboard, items

router = APIRouter(prefix="/api")
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
