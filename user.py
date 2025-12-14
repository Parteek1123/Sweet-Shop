import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = mapped_column(String(50), unique=True, nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    password_hash = mapped_column(String(255), nullable=False)
    is_admin = mapped_column(Boolean, default=False)
