from fastapi import APIRouter

from .auth import router as auth_router
from .items import router as items_router
from .users import router as users_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(items_router, prefix="/items")
router.include_router(users_router, prefix="/users")
