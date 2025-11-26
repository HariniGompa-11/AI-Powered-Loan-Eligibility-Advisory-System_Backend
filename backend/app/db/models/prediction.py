import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    input_json = Column(JSONB, nullable=False)
    eligible = Column(Boolean, nullable=False)
    probability = Column(Float, nullable=False)
    shap_json = Column(JSONB, nullable=True)
    recommendation_text = Column(Text, nullable=True)
    bank_name = Column(String(100), default="Unknown", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="predictions")
