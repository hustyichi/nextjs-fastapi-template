from uuid import UUID

from app.db.base import get_async_session
from app.db.dao.items import ItemDAO
from app.db.models.user import User
from app.routes.schemas import ItemCreate, ItemRead
from app.services.users import current_active_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["item"])


@router.get("/", response_model=list[ItemRead])
async def read_item(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    dao = ItemDAO(db)
    items = await dao.get_all(user_id=user.id)
    return [ItemRead.model_validate(item) for item in items]


@router.post("/", response_model=ItemRead)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    dao = ItemDAO(db)
    db_item = await dao.create(
        name=item.name,
        description=item.description,
        quantity=item.quantity,
        user_id=user.id,
    )
    return db_item


@router.delete("/{item_id}")
async def delete_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    dao = ItemDAO(db)
    item = await dao.get_by_id(item_id=item_id, user_id=user.id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")

    await dao.delete(item_id=item_id, user_id=user.id)

    return {"message": "Item successfully deleted"}
