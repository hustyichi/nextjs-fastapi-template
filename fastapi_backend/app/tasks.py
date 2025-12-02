import taskiq_fastapi
from app.config import settings
from app.db.base import get_async_session
from app.db.dao.items import ItemDAO
from app.db.dao.user import get_user_db
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

result_backend: RedisAsyncResultBackend = RedisAsyncResultBackend(
    redis_url=settings.REDIS_URL,
)

broker = RedisStreamBroker(
    url=settings.REDIS_URL,
).with_result_backend(result_backend)

taskiq_fastapi.init(broker, "app.main:app")


@broker.task
async def hello_world_task(session: AsyncSession = TaskiqDepends(get_async_session)):
    """异步解析简历任务"""
    user_dao = get_user_db(session)
    users = await user_dao.get_all()
    print(f"Got {len(users)} users from db")
    dao = ItemDAO(session)
    items = await dao.get_all()
    print(f"Got {len(items)} items from db")
    print("Hello World")
