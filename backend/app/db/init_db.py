from app.db.session import async_engine
from app.db.base import Base

async def init_db():
    """
    Create DB tables (async). Call this from startup event.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)