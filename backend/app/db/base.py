from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr

from app.db.session import Base  # import shared Base from session.py


class NotFoundError(Exception):
    """Raised when a database record is not found."""
    pass


class BaseModel(Base):
    """Abstract base model with common fields and helpers."""
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    async def get(cls, db, id: Any) -> Optional["BaseModel"]:
        return await db.get(cls, id)

    @classmethod
    async def get_or_404(cls, db, id: Any) -> "BaseModel":
        result = await cls.get(db, id)
        if not result:
            raise NotFoundError(f"{cls.__name__} with id {id} not found")
        return result

    async def save(self, db) -> None:
        db.add(self)
        await db.commit()
        await db.refresh(self)

    async def delete(self, db) -> None:
        await db.delete(self)
        await db.commit()