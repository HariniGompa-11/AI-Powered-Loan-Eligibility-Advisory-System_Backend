import contextlib
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Single shared Base for all models
Base = declarative_base()

# ---------------------------
# DATABASE URL CONFIGURATION
# ---------------------------

# If SQLALCHEMY_DATABASE_URI provided, it may already be async or sync.
# Build both sync and async forms explicitly.

# Build the async URL (runtime)
if settings.SQLALCHEMY_DATABASE_URI:
    ASYNC_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI.replace(
        "postgres://", "postgresql+asyncpg://"
    ).replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_SERVER}:5432/{settings.POSTGRES_DB}"
    )

# Build the sync URL (migrations)
if settings.SQLALCHEMY_DATABASE_URI:
    SYNC_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI.replace(
        "postgresql+asyncpg://", "postgresql://"
    ).replace("postgresql+asyncpg://", "postgresql://").replace("postgresql+asyncpg://", "postgresql://")
    # also ensure no postgres:// left
    SYNC_DATABASE_URL = SYNC_DATABASE_URL.replace("postgres://", "postgresql://")
else:
    SYNC_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:5432/{settings.POSTGRES_DB}"

# ---------------------------
# ENGINES
# ---------------------------

# Sync engine (for Alembic and scripts)
engine = create_engine(SYNC_DATABASE_URL, pool_pre_ping=True, echo=settings.DEBUG)

# Async engine (for FastAPI runtime)
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True)

# ---------------------------
# SESSIONMAKERS
# ---------------------------

# Async session (runtime)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Sync session (migrations / scripts)
SyncSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

# ---------------------------
# DEPENDENCIES
# ---------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@contextlib.contextmanager
def get_sync_db() -> Generator:
    db = SyncSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()