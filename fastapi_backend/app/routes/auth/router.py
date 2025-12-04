from app.routes.schemas import UserCreate, UserRead
from app.services.users import auth_backend, fastapi_user_manager
from fastapi import APIRouter

router = APIRouter(tags=["auth"])

router.include_router(
    fastapi_user_manager.get_auth_router(auth_backend),
    prefix="/jwt",
)
router.include_router(
    fastapi_user_manager.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_user_manager.get_reset_password_router(),
)
router.include_router(
    fastapi_user_manager.get_verify_router(UserRead),
)
