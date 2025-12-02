from typing import List, Optional
from uuid import UUID

from app.db.models.items import Item
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ItemDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id: UUID, user_id: UUID) -> Optional[Item]:
        result = await self.session.execute(select(Item).where(Item.id == item_id, Item.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: UUID) -> List[Item]:
        result = await self.session.execute(select(Item).where(Item.user_id == user_id))
        return result.scalars().all()

    async def create(
        self,
        name: str,
        description: Optional[str],
        quantity: Optional[int],
        user_id,
    ) -> Item:
        item = Item(
            name=name,
            description=description,
            quantity=quantity,
            user_id=user_id,
        )
        self.session.add(item)
        await self.session.flush()
        return item

    async def delete(self, item_id, user_id: UUID) -> None:
        item = await self.get_by_id(item_id=item_id, user_id=user_id)
        if item:
            await self.session.delete(item)
