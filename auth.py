from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.user import UserCreate, UserOut
from app.repositories.user import user_repo
from app.core.security import create_access_token, verify_password
from app.database import get_session
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=UserOut)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    existing = await user_repo.get_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username exists")
    user = await user_repo.create(db, payload)
    token = create_access_token(user.id)
    return UserOut(**user.__dict__, access_token=token)


@router.post("/login", response_model=UserOut)
async def login(form: UserCreate, db: AsyncSession = Depends(get_session)):
    stmt = select(User).where(User.username == form.username)
    user: User | None = await db.scalar(stmt)
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")
    token = create_access_token(user.id)
    return UserOut(**user.__dict__, access_token=token)
