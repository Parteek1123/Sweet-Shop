import uuid
from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import mapped_column
from app.database import Base


class Sweet(Base):
    __tablename__ = "sweets"

    id = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = mapped_column(String(100), unique=True, nullable=False)
    category = mapped_column(String(50), nullable=False)
    price_cents = mapped_column(Integer, nullable=False)
    quantity = mapped_column(Integer, nullable=False, default=0)
