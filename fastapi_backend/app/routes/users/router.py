from app.routes.schemas import UserRead, UserUpdate
from app.services.users import fastapi_user_manager
from fastapi import APIRouter

router = APIRouter(tags=["users"])


router.include_router(
    fastapi_user_manager.get_users_router(UserRead, UserUpdate),
)
